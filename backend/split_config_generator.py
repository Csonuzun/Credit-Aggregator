# split_config_generator.py

import json
import math

# 1) Load bank data from the same banks.json used by server.py:
with open("banks.json", "r") as f:
    banks_data = json.load(f)

# 2) Convert your banks_data to the 4-tuple bracket format (min_limit, max_limit, alt_limit, rate)
#    if your code expects that structure. If not, adapt accordingly.
bank_rates = {}
for bank_name, info in banks_data.items():
    tuple_ranges = []
    for bracket in info["ranges"]:
        min_limit = bracket.get("min", 0)
        max_limit = bracket.get("max", float("inf"))
        # Check if 'alt_limit' exists; if not, set to 0
        alt_limit = bracket.get("alt_limit", bracket.get("min_balance", 0))
        rate = bracket.get("rate", 0)
        tuple_ranges.append((min_limit, max_limit, alt_limit, rate))
    bank_rates[bank_name] = tuple_ranges


def calculate_effective_rate_helper(deposit, ranges):
    """
    Returns the effective annual interest rate (%) given the deposit
    and bracket definitions in 'ranges': (min_limit, max_limit, alt_limit, rate).
    """
    for (min_limit, max_limit, alt_limit, rate) in ranges:
        if min_limit <= deposit <= max_limit:
            interest_eligible = deposit - alt_limit
            if interest_eligible > 0:
                annual_interest = interest_eligible * (rate / 100)
                return (annual_interest / deposit) * 100
            return 0.0
    return 0.0


def one_day_return(deposit, bank):
    """
    Calculates the 1-day return for a given deposit and bank, using bank_rates.
    """
    ranges = bank_rates[bank]
    # If the first tuple is 4-length, we have alt_limit
    if len(ranges[0]) == 4:
        eff_rate = calculate_effective_rate_helper(deposit, ranges)
        return eff_rate * deposit / 100 / 365
    else:
        # Otherwise, assume 3-tuple: (min_limit, max_limit, rate)
        brate = 0
        for (min_limit, max_limit, rate) in ranges:
            if min_limit <= deposit <= max_limit:
                brate = rate
                break
        return brate * deposit / 100 / 365


def split_return(bank1_deposit, total_deposit, bank1, bank2):
    """
    1-day return if deposit is split between bank1_deposit in bank1
    and (total_deposit - bank1_deposit) in bank2.
    """
    return (one_day_return(bank1_deposit, bank1) +
            one_day_return(total_deposit - bank1_deposit, bank2))


def single_return(total_deposit, bank):
    """
    1-day return if the entire deposit is in one bank.
    """
    return one_day_return(total_deposit, bank)


def generate_split_configs():
    """
    Generates split configurations by selecting, for each main_bank's bracket,
    the split that provides the maximum split_return among all alternative banks.

    Returns:
        split_configs (dict): {
            "main_bank": [
                {
                    "max_limit": ...,
                    "alternative_bank": ...,
                    "split_upper_limit": ...,
                    "split_return": ...
                },
                ...
            ],
            ...
        }
    """
    split_configs = {}
    diff_th = 0.1  # Default tolerance for difference
    step = 1  # Default step size

    for main_bank in bank_rates:
        main_bank_brackets = bank_rates[main_bank]
        bank_splits = []  # List to store the best split per bracket
        print(f"\nFor main bank: {main_bank}")

        # Iterate over each bracket in main_bank
        for i, (min_limit, max_limit, alt_limit, rate) in enumerate(main_bank_brackets):
            if max_limit == float('inf') or max_limit > 1_000_000:
                continue  # Skip the infinite upper bound or too-large bounds

            print(f'Max limit: {max_limit}')

            # Next bracket's max to limit the search
            next_max_limit = (main_bank_brackets[i + 1][1]
                              if (i + 1 < len(main_bank_brackets))
                              else float('inf'))
            if next_max_limit > 1_000_000:
                print("Next max limit exceeds 1,000,000. Skipping search.")
                continue

            best_split = None
            best_split_return = -math.inf  # Initialize with negative infinity

            for alt_bank in bank_rates:
                if alt_bank == main_bank:
                    continue  # Skip the same bank

                # We start from max_limit + 50 up to next_max_limit
                for D in range(max_limit + 50, int(next_max_limit), step):
                    sr = single_return(D, main_bank)
                    sp = split_return(D - max_limit, D, alt_bank, main_bank)
                    diff = sr - sp
                    if abs(diff) < diff_th:
                        # Calculate split_return for comparison
                        current_split_return = sp
                        if current_split_return > best_split_return:
                            best_split_return = current_split_return
                            best_split = {
                                "max_limit": max_limit,
                                "alternative_bank": alt_bank,
                                "split_upper_limit": D - max_limit,
                            }
                        break  # Found a valid split for this alt_bank

            if best_split:
                bank_splits.append(best_split)
                print(f"  - Best split for {max_limit} in {main_bank}:")
                print(f"    Alternative Bank: {best_split['alternative_bank']}")
                print(f"    Recommended Split Amount: {best_split['split_upper_limit']}")
            else:
                print(f"  - No suitable split found for max_limit = {max_limit} in {main_bank}.")

            print('-----------------------------------')

        if bank_splits:
            split_configs[main_bank] = bank_splits
            print(f"Best splits for {main_bank}:")
            for split in bank_splits:
                print(split)

    return split_configs


if __name__ == "__main__":
    # Generate splits
    splits = generate_split_configs()

    # Save to JSON (e.g., split_config.json) so server.py can load it
    with open("split_config.json", "w") as f:
        json.dump(splits, f, indent=2)

    print("Generated split configurations saved to split_config.json")