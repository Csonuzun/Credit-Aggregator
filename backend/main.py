import pulp
import json
import sys


def load_banks(file_path='banks.json'):
    with open(file_path, 'r') as file:
        return json.load(file)


def maximize_interest(total_deposit, banks):
    # Initialize the problem
    prob = pulp.LpProblem("Maximize_Interest", pulp.LpMaximize)

    # Create dictionaries to hold variables
    deposit_vars = {}
    range_vars = {}
    interest_vars = {}

    # Large constant for linearization (M)
    # It should be larger than the maximum possible deposit in any range
    M = total_deposit  # Set M to the total deposit for flexibility

    # Iterate over each bank and its ranges to create variables
    for bank_key, bank_info in banks.items():
        # Continuous variable for deposit amount in each bank
        deposit_vars[bank_key] = pulp.LpVariable(
            f"deposit_{bank_key}", lowBound=0, upBound=total_deposit, cat='Continuous'
        )

        for idx, range_item in enumerate(bank_info['ranges']):
            # Binary variable indicating if a range is selected for the bank
            range_vars[(bank_key, idx)] = pulp.LpVariable(
                f"range_{bank_key}_{idx}", cat='Binary'
            )
            # Auxiliary variable for interest calculation
            interest_vars[(bank_key, idx)] = pulp.LpVariable(
                f"interest_{bank_key}_{idx}", lowBound=0, cat='Continuous'
            )

    # Objective Function: Maximize total interest
    objective = []
    for bank_key, bank_info in banks.items():
        for idx, range_item in enumerate(bank_info['ranges']):
            rate = range_item['rate']
            # The objective is to maximize the sum of daily interests
            # interest_vars[(bank_key, idx)] represents (deposit - min_balance) * range_vars
            # Multiply by rate and adjust for daily interest
            daily_interest = (rate / 365) / 100  # Convert annual rate to daily decimal
            objective.append(interest_vars[(bank_key, idx)] * daily_interest)

    prob += pulp.lpSum(objective), "Total_Daily_Interest"

    # Constraint 1: Total deposits must equal the specified total_deposit
    prob += (
        pulp.lpSum([deposit_vars[bank_key] for bank_key in banks.keys()]) == total_deposit,
        "Total_Deposit",
    )

    # Constraint 2: Each bank's deposit must fall into exactly one range
    for bank_key, bank_info in banks.items():
        prob += (
            pulp.lpSum([range_vars[(bank_key, idx)] for idx in range(len(bank_info['ranges']))]) == 1,
            f"One_Range_{bank_key}",
        )

    # Constraint 3: Deposit within selected range and Linearization Constraints
    for bank_key, bank_info in banks.items():
        for idx, range_item in enumerate(bank_info['ranges']):
            min_limit = range_item['min']
            max_limit = range_item['max']
            min_balance = range_item['min_balance']

            # Ensure that max_limit does not exceed total_deposit
            # If 'max' is set to a very high number (e.g., 999999999), it's already handled by the variable's upper bound
            # So, no need to adjust 'max_limit' unless it exceeds total_deposit
            if max_limit > total_deposit:
                max_limit = total_deposit

            # Ensure deposit is within the selected range
            prob += (
                deposit_vars[bank_key] >= min_limit * range_vars[(bank_key, idx)],
                f"Min_Limit_{bank_key}_{idx}",
            )
            prob += (
                deposit_vars[bank_key] <= max_limit * range_vars[(bank_key, idx)],
                f"Max_Limit_{bank_key}_{idx}",
            )

            # Additional Constraint: deposit >= min_balance * range_var
            prob += (
                deposit_vars[bank_key] >= min_balance * range_vars[(bank_key, idx)],
                f"Min_Balance_Constraint_{bank_key}_{idx}",
            )

            # Linearization Constraints for interest_vars
            # interest_vars = (deposit_vars - min_balance) * range_vars
            # Which is equivalent to:
            # interest_vars <= deposit_vars - min_balance
            prob += (
                interest_vars[(bank_key, idx)] <= deposit_vars[bank_key] - min_balance,
                f"Interest_Upper1_{bank_key}_{idx}",
            )
            # interest_vars <= (max_limit - min_balance) * range_vars
            prob += (
                interest_vars[(bank_key, idx)] <= (max_limit - min_balance) * range_vars[(bank_key, idx)],
                f"Interest_Upper2_{bank_key}_{idx}",
            )
            # interest_vars >= (deposit_vars - min_balance) - (M * (1 - range_vars))
            prob += (
                interest_vars[(bank_key, idx)] >= (deposit_vars[bank_key] - min_balance) - M * (
                            1 - range_vars[(bank_key, idx)]),
                f"Interest_Lower_{bank_key}_{idx}",
            )
            # interest_vars >= 0 is already handled by lowBound=0

    # Optional: Write the LP file for inspection
    prob.writeLP("Maximize_Interest.lp")

    # Solve the problem with verbose output
    prob.solve(pulp.PULP_CBC_CMD(msg=True))

    # Check if the problem has an optimal solution
    if pulp.LpStatus[prob.status] != 'Optimal':
        print("No optimal solution found.")
    else:
        # Display the results
        total_daily_interest = 0
        for bank_key in banks.keys():
            deposit = deposit_vars[bank_key].varValue
            selected_range = None
            for idx, range_item in enumerate(banks[bank_key]['ranges']):
                if range_vars[(bank_key, idx)].varValue == 1:
                    selected_range = range_item
                    break
            if selected_range:
                interest_eligible = deposit - selected_range['min_balance']
                if interest_eligible > 0:
                    daily_interest = (interest_eligible * selected_range['rate'] / 100) / 365
                else:
                    daily_interest = 0
                total_daily_interest += daily_interest
                print(f"Bank: {banks[bank_key]['name']}")
                print(f"  Deposit: {deposit:.2f} TL")
                print(
                    f"  Selected Range: {selected_range['min']} - {selected_range['max']} TL at {selected_range['rate']}%"
                )
                print(f"  Eligible for Interest: {interest_eligible:.2f} TL")
                print(f"  Daily Interest: {daily_interest:.2f} TL\n")

        print(f"Total Daily Interest: {total_daily_interest:.2f} TL")


if __name__ == "__main__":
    # Example usage:
    # Pass the total deposit as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python main.py <total_deposit>")
        sys.exit(1)

    try:
        total_deposit = float(sys.argv[1])
        if total_deposit <= 0:
            raise ValueError
    except ValueError:
        print("Please provide a positive numeric value for total_deposit.")
        sys.exit(1)

    banks = load_banks()
    maximize_interest(total_deposit, banks)