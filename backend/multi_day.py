import pulp
import json
import sys
import pulp
import sys
from typing import Dict, Any, Tuple


def load_banks(file_path='banks.json', total_deposit=0, exclude_banks=None):
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
    for bank_key in list(banks.keys()):
        if exclude_banks and bank_key in exclude_banks:
            del banks[bank_key]

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


def build_single_day_model(total_deposit: float, banks: Dict[str, Any], debug: bool = False) -> Tuple[
    pulp.LpProblem, Dict[Tuple[str, int], pulp.LpVariable], Dict[Tuple[str, int], pulp.LpVariable], Dict[
        Tuple[str, int], pulp.LpVariable]]:
    """
    Builds a single-day PuLP model for maximizing daily interest.

    Parameters:
        total_deposit (float): Total amount to deposit across all banks for the day.
        banks (dict): Dictionary containing bank information.
        debug (bool): If True, prints detailed debug information.

    Returns:
        Tuple containing:
            - PuLP problem instance.
            - Dictionary of deposit variables.
            - Dictionary of interest variables.
            - Dictionary of range selection variables.
    """

    # Initialize the problem as a maximization problem
    prob = pulp.LpProblem("Maximize_Interest_One_Day", pulp.LpMaximize)

    # Big-M for linearization (set to total_deposit * 2 to ensure feasibility)
    M = total_deposit * 2

    # Dictionaries to hold variables
    deposit_vars: Dict[Tuple[str, int], pulp.LpVariable] = {}
    interest_vars: Dict[Tuple[str, int], pulp.LpVariable] = {}
    range_vars: Dict[Tuple[str, int], pulp.LpVariable] = {}

    # Define variables for each bank and its ranges
    for bank_key, bank_info in banks.items():
        for idx, rng in enumerate(bank_info['ranges']):
            # Deposit variable: amount deposited in this range
            deposit_var = pulp.LpVariable(
                f"deposit_{bank_key}_{idx}",
                lowBound=0,
                upBound=min(rng['max'], total_deposit),
                cat='Continuous'
            )
            deposit_vars[(bank_key, idx)] = deposit_var

            # Interest variable: interest earned from this range
            interest_var = pulp.LpVariable(
                f"interest_{bank_key}_{idx}",
                lowBound=0,
                cat='Continuous'
            )
            interest_vars[(bank_key, idx)] = interest_var

            # Range selection variable: whether this range is selected
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
        # Function to print all constraints
        def print_constraints(prob: pulp.LpProblem):
            print("\n--- Constraints ---")
            for name, constraint in prob.constraints.items():
                print(f"{name}: {constraint}")

        # Function to print all variables
        def print_variables(prob: pulp.LpProblem):
            print("\n--- Variables ---")
            for var in prob.variables():
                print(f"{var.name} = {var.varValue}")

        print_constraints(prob)
        print_variables(prob)

    return prob, deposit_vars, interest_vars, range_vars


def solve_single_day(total_deposit, banks, debug=False):
    """
    Builds & solves the single-day model, returns:
       (daily_interest, status, allocations)
    Where 'allocations' is a dict summarizing each bank's chosen range and deposit.
    """
    prob, deposit_vars, interest_vars, range_vars = build_single_day_model(total_deposit, banks)

    if debug:
        print("--- Single-Day Model (Before Solve) ---")
        print(prob)

    solver = pulp.PULP_CBC_CMD(msg=debug)
    prob.solve(solver)
    status = pulp.LpStatus[prob.status]

    daily_interest = 0.0
    allocations = {}  # { bank_key: { 'range_idx': idx, 'deposit': X, 'interest': Y } }

    if status == 'Optimal':
        daily_interest = pulp.value(prob.objective)

        # For each bank, find which range_idx is chosen & deposit/interest
        for bank_key, bank_data in banks.items():
            chosen_idx = None
            chosen_dep = 0.0
            chosen_int = 0.0
            for idx in range(len(bank_data['ranges'])):
                if pulp.value(range_vars[(bank_key, idx)]) > 0.5:
                    chosen_idx = idx
                    chosen_dep = pulp.value(deposit_vars[(bank_key, idx)])
                    chosen_int = pulp.value(interest_vars[(bank_key, idx)])
                    break
            allocations[bank_key] = {
                'range_idx': chosen_idx,
                'deposit': chosen_dep,
                'interest': chosen_int
            }

        if debug:
            print("--- Single-Day Model (Solution) ---")
            print(f"Objective (Daily Interest): {daily_interest:.4f}")

    return daily_interest, status, allocations


def run_multi_day_opt(initial_deposit, banks, days, debug=False):
    """
    Iteratively run the single-day optimization for 'days' days,
    compounding deposit day by day.

    Returns a list of day-by-day records:
      [ {
         'day': i,
         'start_deposit': ...,
         'interest': ...,
         'end_deposit': ...,
         'splits': { bank_key: { 'range_idx': idx, 'deposit': X, 'interest': Y } }
      }, ... ]
    """
    results = []
    current_deposit = initial_deposit

    for day in range(1, days + 1):
        if debug:
            print(f"\n=== Day {day} ===")
            print(f"Starting deposit: {current_deposit:.2f}")

        daily_interest, status, allocations = solve_single_day(current_deposit, banks, debug=debug)

        if status != 'Optimal':
            print(f"Day {day} => Not optimal (status={status}), stopping iteration.")
            break

        new_deposit = current_deposit + daily_interest
        day_record = {
            'day': day,
            'start_deposit': current_deposit,
            'interest': daily_interest,
            'end_deposit': new_deposit,
            'splits': allocations
        }
        results.append(day_record)

        if debug:
            print(f"Day {day} interest: {daily_interest:.2f}")
            print(f"Day {day} end deposit: {new_deposit:.2f}")

        # For the next day
        current_deposit = new_deposit

    return results


def print_multi_day_opt_results(results):
    print("\n=== Multi-Day Allocation Results ===")
    if not results:
        print("No feasible solution on Day 1, or solver stopped early.")
        return

    for r in results:
        print(
            f"\nDay {r['day']}: start={r['start_deposit']:.2f}, interest={r['interest']:.2f}, end={r['end_deposit']:.2f}")
        # Print how deposit was allocated across banks
        print(" Bank Splits:")
        for bank_key, info in r['splits'].items():
            if info['range_idx'] is not None and info['deposit'] > 0:
                print(
                    f"   {bank_key}: range_idx={info['range_idx']}, deposit={info['deposit']:.2f}")

    final_day = results[-1]['day']
    final_deposit = results[-1]['end_deposit']
    total_interest = sum(r['interest'] for r in results)
    print(f"\nAfter {final_day} days, total interest earned: {total_interest:.2f}")
    print(f"Final deposit: {final_deposit:.2f}")


def main():
    """
    Usage:
        python multi_day_opt.py <initial_deposit> <days> [--debug]
    Example:
        python multi_day_opt.py 55000 30 --debug
    """
    if len(sys.argv) < 3:
        print("Usage: python multi_day_opt.py <initial_deposit> <days> [--debug]")
        sys.exit(1)

    initial_deposit = float(sys.argv[1])
    days = int(sys.argv[2])
    debug = False
    if len(sys.argv) > 3 and sys.argv[3] == '--debug':
        debug = True

    # Load banks
    banks = load_banks('banks.json', total_deposit=initial_deposit)

    # Optionally filter out obviously infeasible ranges if min_balance>initial_deposit, etc.
    # We'll skip that for brevity, but you can adapt from prior solutions.

    # Run multi-day iterative approach
    results = run_multi_day_opt(initial_deposit, banks, days, debug=debug)

    print_multi_day_opt_results(results)


if __name__ == "__main__":
    results = run_multi_day_opt(55000, load_banks('banks.json', 55000, ['enpara', 'onhesap']), 3)
    print_multi_day_opt_results(results)
