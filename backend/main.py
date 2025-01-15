getir_ranges = [
    (2500, 25000, 2500, 47.5),
    (25001, 50000, 5000, 47.5),
    (50001, 100000, 7500, 47.5),
    (100001, 500000, 20000, 47.5),
    (500001, 1000000, 40000, 47.5),
    (1000001, 2000000, 75000, 47.5),
    (2000001, 2100000, 100000, 47.5),
    (2100001, 5100000, 100000, 30),
]

enpara_ranges = [
    (0, 100000, 32.00),
    (100001, 500000, 35.00),
    (500001, 1000000, 38.00),
    (1000001, float('inf'), 41.00)
]

odeabank_hosgeldin = [
    (7500, 50000, 7500, 51.0),
    (50001, 100000, 10000, 51.0),
    (100001, 250000, 20000, 51.0),
    (250001, 500000, 40000, 51.0),
    (500001, 750000, 75000, 51.0),
    (750001, 1000000, 125000, 51.0),
    (1000001, 2000000, 200000, 51.0),
    (2000001, 5000000, 300000, 51.0),
    (5000001, 10000000, 500000, 13.5)
]

odeabank_devam = [
    (7500, 50000, 7500, 43.0),
    (50001, 100000, 10000, 43.0),
    (100001, 250000, 20000, 43.0),
    (250001, 500000, 40000, 41.0),
    (500001, 750000, 75000, 40.0),
    (750001, 1000000, 125000, 40.0),
    (1000001, 2000000, 200000, 40.0),
    (2000001, 5000000, 300000, 35.0),
    (5000001, 10000000, 500000, 13.0)
]

bank_rates = {
    "enpara": enpara_ranges,
    "getir": getir_ranges,
    "odeabank_hosgeldin": odeabank_hosgeldin,
    "odeabank_devam": odeabank_devam
}



def calculate_effective_rate_helper(deposit, ranges):
    """
    Returns the effective annual interest rate (%) given the deposit
    and the bracket definitions in 'ranges'.
    """
    for min_limit, max_limit, alt_limit, rate in ranges:
        if min_limit <= deposit <= max_limit:
            interest_eligible = deposit - alt_limit
            if interest_eligible > 0:
                annual_interest = interest_eligible * (rate / 100)
                return (annual_interest / deposit) * 100
            return 0.0
    return 0.0


def one_day_return(deposit, bank):
    bank_ranges = bank_rates[bank]
    if len(bank_ranges[0]) == 4:
        bank_rate = calculate_effective_rate_helper(deposit, bank_ranges)
        return bank_rate * deposit / 100 / 365
    else:
        bank_rate = 0
        for min_limit, max_limit, rate in bank_rates[bank]:
            if min_limit <= deposit <= max_limit:
                bank_rate = rate
                break
        return bank_rate * deposit / 100 / 365


def split_return(bank1_deposit, total_deposit, bank1, bank2):
    return one_day_return(bank1_deposit, bank1) + one_day_return(total_deposit - bank1_deposit, bank2)


def single_return(total_deposit, bank):
    return one_day_return(total_deposit, bank)


def find_juicy_point():
    main_bank = "odeabank_hosgeldin"  # The main bank for single_return comparison
    diff_th = 0.1  # Default tolerance for difference
    step = 1  # Default step size

    for i, (min_limit, max_limit, alt_limit, rate) in enumerate(bank_rates[main_bank]):
        if max_limit == float('inf') or max_limit > 1_000_000:
            continue  # Skip the infinite upper bound

        print(f"\nFor max_limit = {max_limit} in {main_bank}:")
        next_max_limit = bank_rates[main_bank][i + 1][1] if i + 1 < len(bank_rates[main_bank]) else float('inf')

        for bank in bank_rates.keys():
            if bank == main_bank:
                continue  # Skip the main bank

            D = max_limit
            match = ()
            for D in range(D + 50, int(next_max_limit), step):

                sr = single_return(D, main_bank)
                split = split_return(D - max_limit, D, bank, main_bank)
                diff = sr - split
                # Allow a small tolerance
                if abs(diff) < diff_th:
                    match = (D - max_limit, split)
                    break

            if match:
                print(f"  - Possible deposit in {bank} that satisfies single = split: {match[0]} (split_return = {round(match[1],2)})")
            else:
                print(f"  - No deposit found in {bank} that satisfies single = split (max_limit = {max_limit}).")


if __name__ == "__main__":
    find_juicy_point()


