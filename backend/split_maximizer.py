import pulp
import json
import sys
import os


def load_banks(file_path='banks.json', total_deposit=0):
    """
    Loads bank data from a JSON file, pre-filters infeasible ranges, and returns it as a dictionary.

    Parameters:
        file_path (str): Path to the banks JSON file.
        total_deposit (float): Total deposit amount to filter out infeasible ranges.

    Returns:
        dict: Parsed and filtered bank data.
    """
    try:
        with open(file_path, 'r') as file:
            banks = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: The file '{file_path}' contains invalid JSON.\n{e}")
        sys.exit(1)

    # Validate and pre-filter ranges
    for bank_key, bank_info in banks.items():
        original_range_count = len(bank_info['ranges'])
        # Pre-filter: Remove ranges where min_balance > total_deposit or min > total_deposit
        feasible_ranges = [
            rng for rng in bank_info['ranges']
            if rng.get('min_balance', 0) <= total_deposit and rng.get('min', 0) <= total_deposit
        ]
        removed_ranges = original_range_count - len(feasible_ranges)
        if removed_ranges > 0:
            print(f"Info: Removed {removed_ranges} infeasible range(s) from '{bank_key}' based on total deposit.")

        # Update the bank's ranges
        bank_info['ranges'] = feasible_ranges

        # Validate that each bank has at least one feasible range
        if not feasible_ranges:
            print(
                f"Error: Bank '{bank_key}' has no feasible ranges after filtering. Please adjust the ranges or increase the total deposit.")
            sys.exit(1)

        # Further validate that each remaining range has min_balance <= min
        for idx, rng in enumerate(bank_info['ranges']):
            if rng['min_balance'] > rng['min']:
                print(
                    f"Error in '{bank_key}', Range {idx}: 'min_balance' ({rng['min_balance']}) > 'min' ({rng['min']})."
                )
                sys.exit(1)

    return banks


def calculate_min_sum(banks):
    """
    Calculates the sum of the smallest min_balance from each bank.

    Parameters:
        banks (dict): Dictionary containing bank information.

    Returns:
        float: Sum of the smallest min_balance across all banks.
    """
    min_sum = 0
    for bank_info in banks.values():
        min_balance = min(rng.get('min_balance', 0) for rng in bank_info['ranges'])
        min_sum += min_balance
    return min_sum


def dump_lp_file(prob, filename='model.lp'):
    """
    Dumps the LP model to a file for external inspection.

    Parameters:
        prob (pulp.LpProblem): The LP problem.
        filename (str): The name of the file to dump the LP model.
    """
    prob.writeLP(filename)
    print(f"\nModel has been written to '{filename}' for further inspection.")


def print_constraints(prob):
    """
    Prints all constraints in the LP problem.

    Parameters:
        prob (pulp.LpProblem): The LP problem.
    """
    print("\n--- All Constraints ---")
    for name, constraint in prob.constraints.items():
        print(f"{name}: {constraint}")


def print_variables(prob):
    """
    Prints all variables in the LP problem along with their categories and bounds.

    Parameters:
        prob (pulp.LpProblem): The LP problem.
    """
    print("\n--- All Variables ---")
    for var in prob.variables():
        print(f"{var.name}: Category={var.cat}, Bounds=({var.lowBound}, {var.upBound})")


def print_solution(prob, deposit_vars, interest_vars, range_vars, banks):
    """
    Prints the solution of the LP problem.

    Parameters:
        prob (pulp.LpProblem): The LP problem.
        deposit_vars (dict): Deposit variables.
        interest_vars (dict): Interest variables.
        range_vars (dict): Range selection variables.
        banks (dict): Bank data.
    """
    status = pulp.LpStatus[prob.status]
    if status != 'Optimal':
        print(f"\nSolver Status: {status}")
        print("No optimal solution found.")
        return

    total_daily_interest = pulp.value(prob.objective)
    print(f"\nStatus: {status}")
    print(f"Objective (Total Daily Interest): {total_daily_interest:.4f} TL")

    for bank_key, bank_info in banks.items():
        chosen_range = None
        for idx, rng in enumerate(bank_info['ranges']):
            if pulp.value(range_vars[(bank_key, idx)]) == 1:
                chosen_range = idx
                break
        print(f"\n=== {bank_info['name']} ===")
        if chosen_range is not None:
            deposit_amount = pulp.value(deposit_vars[(bank_key, chosen_range)])
            interest_eligible = pulp.value(interest_vars[(bank_key, chosen_range)])
            selected_range = bank_info['ranges'][chosen_range]
            daily_rate_percentage = (selected_range['rate'] / 100.0) / 365.0 * 100  # Convert to percentage

            print(f"  Selected Range: {selected_range['min']} - {selected_range['max']} TL")
            print(f"  Deposit: {deposit_amount:.2f} TL")
            print(f"  Rate: {selected_range['rate']}% annually → ~ {daily_rate_percentage:.4f}% daily")
            print(f"  Interest-Earning Portion: {interest_eligible:.2f} TL")
        else:
            print("  No range selected (unexpected).")


def maximize_interest(total_deposit, banks, debug=False):
    """
    Define and solve the optimization problem to maximize daily interest.

    Parameters:
        total_deposit (float): Total amount to deposit across all banks.
        banks (dict): Dictionary containing bank information.
        debug (bool): If True, prints detailed debugging information.

    Returns:
        None
    """
    # Preliminary Feasibility Check: Sum of smallest min_balance per bank <= total_deposit
    min_sum = calculate_min_sum(banks)
    if min_sum > total_deposit:
        print(
            f"Infeasible: Sum of smallest min_balance across all banks ({min_sum}) exceeds total deposit ({total_deposit})."
        )
        sys.exit(1)

    # Initialize the problem as a maximization problem
    prob = pulp.LpProblem("Maximize_Interest", pulp.LpMaximize)

    # Create dictionaries to hold variables
    deposit_vars = {}  # (bank_key, range_idx) -> deposit variable
    interest_vars = {}  # (bank_key, range_idx) -> interest variable
    range_vars = {}  # (bank_key, range_idx) -> binary range selection variable

    # Big-M for linearization (set to total_deposit to keep it tight)
    M = total_deposit

    # Define variables for each bank and its ranges
    for bank_key, bank_info in banks.items():
        for idx, rng in enumerate(bank_info['ranges']):
            # Deposit variable for the range
            deposit_var = pulp.LpVariable(
                f"deposit_{bank_key}_{idx}",
                lowBound=0,
                upBound=min(rng['max'], total_deposit),
                cat='Continuous'
            )
            deposit_vars[(bank_key, idx)] = deposit_var

            # Interest variable for the range
            interest_var = pulp.LpVariable(
                f"interest_{bank_key}_{idx}",
                lowBound=0,
                cat='Continuous'
            )
            interest_vars[(bank_key, idx)] = interest_var

            # Binary variable to indicate if the range is selected
            range_var = pulp.LpVariable(
                f"range_{bank_key}_{idx}",
                cat='Binary'
            )
            range_vars[(bank_key, idx)] = range_var

    # Objective Function: Maximize total daily interest
    objective_terms = []
    for bank_key, bank_info in banks.items():
        for idx, rng in enumerate(bank_info['ranges']):
            daily_rate = (rng['rate'] / 100.0) / 365.0  # Convert annual rate to daily decimal
            objective_terms.append(interest_vars[(bank_key, idx)] * daily_rate)

    prob += pulp.lpSum(objective_terms), "Total_Daily_Interest"

    # Constraint 1: Total deposits across all banks and ranges must equal total_deposit
    prob += (
        pulp.lpSum(deposit_vars.values()) == total_deposit,
        "Total_Deposit"
    )

    # Constraint 2: Exactly one range must be selected per bank
    for bank_key, bank_info in banks.items():
        prob += (
            pulp.lpSum(range_vars[(bank_key, idx)] for idx in range(len(bank_info['ranges']))) == 1,
            f"ExactlyOneRange_{bank_key}"
        )

    # Constraint 3: Range-specific constraints with fixed Interest_Upper1 using Big-M to linearize
    for bank_key, bank_info in banks.items():
        for idx, rng in enumerate(bank_info['ranges']):
            dvar = deposit_vars[(bank_key, idx)]
            ivar = interest_vars[(bank_key, idx)]
            rvar = range_vars[(bank_key, idx)]

            min_limit = rng['min']
            max_limit = min(rng['max'], total_deposit)
            min_balance = rng.get('min_balance', 0)

            # Ensure deposit is within [min, max] if the range is selected
            prob += (
                dvar >= min_limit * rvar,
                f"Min_Deposit_{bank_key}_{idx}"
            )
            prob += (
                dvar <= max_limit * rvar,
                f"Max_Deposit_{bank_key}_{idx}"
            )
            prob += (
                dvar >= min_balance * rvar,
                f"Min_Balance_{bank_key}_{idx}"
            )

            # Fixed Interest_Upper1 Constraint using Big-M to linearize
            prob += (
                ivar <= (dvar - min_balance) + M * (1 - rvar),
                f"Interest_Upper1_{bank_key}_{idx}"
            )
            prob += (
                ivar >= (dvar - min_balance) - M * (1 - rvar),
                f"Interest_Lower_{bank_key}_{idx}"
            )
            prob += (
                ivar <= M * rvar,
                f"Interest_Upper2_{bank_key}_{idx}"
            )
            prob += (
                ivar >= 0,
                f"Interest_NonNeg_{bank_key}_{idx}"
            )

    if debug:
        # Print all constraints and variables before solving
        print_constraints(prob)
        print_variables(prob)

    # Solve the problem using the default CBC solver with verbose output
    solver = pulp.PULP_CBC_CMD(msg=True)
    prob.solve(solver)

    if debug:
        # Print all constraints and variables after solving
        print_constraints(prob)
        print_variables(prob)

    # Handle the solution
    if pulp.LpStatus[prob.status] == 'Optimal':
        print_solution(prob, deposit_vars, interest_vars, range_vars, banks)
    else:
        print(f"\nSolver Status: {pulp.LpStatus[prob.status]}")
        print("No optimal solution found.")
        # Optionally, dump the model to an LP file for further inspection
        dump_lp_file(prob)


def main():
    """
    Main execution function.

    Usage:
        python split_maximizer.py <total_deposit> [--debug]
    """
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: python {sys.argv[0]} <total_deposit> [--debug]")
        print("Example: python split_maximizer.py 55000 --debug")
        sys.exit(1)

    # Parse the total deposit amount
    try:
        total_deposit = float(sys.argv[1])
        if total_deposit <= 0:
            raise ValueError
    except ValueError:
        print("Error: Please provide a positive numeric value for <total_deposit>.")
        sys.exit(1)

    # Check for debug flag
    debug = False
    if len(sys.argv) == 3 and sys.argv[2] == '--debug':
        debug = True

    # Load and validate bank data with pre-filtering
    banks = load_banks("banks.json", total_deposit=total_deposit)

    # Solve the optimization problem
    maximize_interest(total_deposit, banks, debug=debug)


if __name__ == "__main__":
    main()