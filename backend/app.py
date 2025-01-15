from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes

# Existing rate ranges
getir_ranges = [
    (0, 2500, 2500, 0),
    (2500, 25000, 2500, 47.5),
    (25001, 50000, 5000, 47.5),
    (50001, 100000, 7500, 47.5),
    (100001, 500000, 20000, 47.5),
    (500001, 1000000, 40000, 47.5),
    (1000001, 2000000, 75000, 47.5),
    (2000001, 2100000, 100000, 47.5),
    (2100001, 5100000, 100000, 30),
    (5100001, float('inf'), 100000, 30)
]

enpara_ranges = [
    (0, 100000, 32.00),
    (100001, 500000, 35.00),
    (500001, 1000000, 38.00),
    (1000001, float('inf'), 41.00)
]

odeabank_hosgeldin = [
    (0, 7500, 7500, 0),
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

odeabank_hosgeldin_splits = [
    (50000, "enpara", 7426),
    (100000, "enpara", 26651),
    (250000, "odeabank_devam", 73294),
    (500000, "getir", 237529),
    (750000, "odeabank_devam", 210794),
    (1000000, "getir", 548958)
]

getir_splits = [
    (25000, "enpara", 7426),
    (50000, "enpara", 7426),
    (100000, "odeabank_hosgeldin", 120743),
    (500000, "odeabank_hosgeldin", 310386),
    (1000000, "odeabank_hosgeldin", 616815)
]

odeabank_devam = [
    (0, 7500, 7500, 43.0),
    (7500, 50000, 7500, 43.0),
    (50001, 100000, 10000, 43.0),
    (100001, 250000, 20000, 43.0),
    (250001, 500000, 40000, 41.0),
    (500501, 750000, 75000, 40.0),
    (750001, 1000000, 125000, 40.0),
    (1000001, 2000000, 200000, 40.0),
    (2000001, 5000000, 300000, 35.0),
    (5000001, 10000000, 500000, 13.0)
]

bank_ranges = {
    "enpara": enpara_ranges,
    "getir": getir_ranges,
    "odeabank_hosgeldin": odeabank_hosgeldin,
    "odeabank_devam": odeabank_devam
}

# Split dictionaries for easier access
split_dict = {
    "odeabank_hosgeldin": odeabank_hosgeldin_splits,
    "getir_finans": getir_splits,
    # "odeabank_devam": odeabank_devam_splits,  # Uncomment and adjust if applicable
}


@app.route('/')
def index():
    # Serve the index.html file when visiting the root URL
    return send_from_directory('..', 'index.html')


@app.route('/calculate', methods=['POST'])
def calculate_effective_rate():
    data = request.json
    deposit = data.get('deposit', 0)

    # Call the helper function to calculate effective rate
    effective_rate = calculate_effective_rate_helper(deposit, getir_ranges)
    return jsonify({"effective_rate": round(effective_rate, 2)})


# Helper function to calculate effective rate for a given deposit
def calculate_effective_rate_helper(deposit, ranges):
    for min_limit, max_limit, alt_limit, rate in ranges:
        if min_limit <= deposit <= max_limit:
            interest_eligible = deposit - alt_limit
            if interest_eligible > 0:
                annual_interest = interest_eligible * (rate / 100)
                return (annual_interest / deposit) * 100
            return 0.0
    return 0.0


@app.route('/graph-data', methods=['GET'])
def graph_data():
    labels = []
    getir_rates = []
    odeabank_hosgeldin_rates = []
    odeabank_devam_rates = []
    enpara_rates = []

    # Generate log-spaced deposits
    fixed_min = 2500  # Minimum deposit
    fixed_max = 6000000  # Maximum deposit
    num_points = 100  # Number of points in the graph
    deposits = np.logspace(np.log10(fixed_min), np.log10(fixed_max), num=num_points)

    for deposit in deposits:
        deposit = int(deposit)  # Convert to integer for simplicity
        labels.append(f'{deposit:,} TL')

        # Calculate Getir Finans effective rate
        getir_rates.append(round(calculate_effective_rate_helper(deposit, getir_ranges), 2))
        odeabank_devam_rates.append(round(calculate_effective_rate_helper(deposit, odeabank_devam), 2))
        odeabank_hosgeldin_rates.append(round(calculate_effective_rate_helper(deposit, odeabank_hosgeldin), 2))
        # Calculate Enpara flat rate
        enpara_rate = 0
        for min_limit, max_limit, rate in enpara_ranges:
            if min_limit <= deposit <= max_limit:
                enpara_rate = rate
                break
        enpara_rates.append(enpara_rate)

    return jsonify({
        "labels": labels,
        "getir_finans_rates": getir_rates,
        "odea_bank_hosgeldin_rates": odeabank_hosgeldin_rates,
        "odea_bank_devam_rates": odeabank_devam_rates,
        "enpara_rates": enpara_rates
    })


def calculate_one_day_return(deposit, effective_rate):
    """
    Calculate the 1-day return based on the effective annual rate.
    """
    return deposit * (effective_rate / 100) / 365


def calculate_effective_rate_after_split(deposit, best_bank, split_info):
    """
    Calculate the effective interest rate and 1-day return after splitting the deposit between two banks.

    Parameters:
        deposit (float): The total deposit amount.
        best_bank (str): The bank with the highest effective rate.
        split_info (dict): Information about the split strategy.

    Returns:
        dict: Contains the effective rate after split and the 1-day return after split.
    """
    best_deposit = split_info['recommended_best_deposit']
    alternative_deposit = split_info['recommended_alternative_deposit']
    alternative_bank = split_info['alternative_bank']

    # Initialize returns
    best_bank_return = 0.0
    alternative_bank_return = 0.0

    # Calculate return for the best bank
    if len(bank_ranges[best_bank][0]) == 4:
        best_rate = calculate_effective_rate_helper(best_deposit, bank_ranges[best_bank])
        best_bank_return = best_deposit * (best_rate / 100) / 365
    else:
        # Handle cases where the best bank's range tuples don't have 4 elements
        best_rate = 0.0
        for min_limit, max_limit, rate in enpara_ranges:
            if min_limit <= best_deposit <= max_limit:
                best_rate = rate
                break
        best_bank_return = best_deposit * (best_rate / 100) / 365
    alternative_rate = 0.0
    if alternative_bank in bank_ranges:
        if len(bank_ranges[alternative_bank][0]) == 4:
            alternative_rate = calculate_effective_rate_helper(best_deposit, bank_ranges[best_bank])
            alternative_bank_return = alternative_deposit * (alternative_rate / 100) / 365
        else:
            for min_limit, max_limit, rate in enpara_ranges:
                if min_limit <= best_deposit <= max_limit:
                    alternative_rate = rate
                    break
            alternative_bank_return = alternative_deposit * (alternative_rate / 100) / 365

    # Calculate total 1-day return after splitting
    total_one_day_return_after_split = best_bank_return + alternative_bank_return

    # Calculate effective rate after splitting
    effective_rate_after_split = (total_one_day_return_after_split * 365) / deposit * 100

    return {
        "effective_rate_after_split": round(effective_rate_after_split, 2),
        "one_day_return_after_split": round(total_one_day_return_after_split, 2)
    }


@app.route('/calculate-best', methods=['POST'])
def calculate_best():
    data = request.json
    deposit = data.get('deposit', 0)

    # Calculate rates for all banks
    getir_rate = calculate_effective_rate_helper(deposit, getir_ranges)
    odeabank_hosgeldin_rate = calculate_effective_rate_helper(deposit, odeabank_hosgeldin)
    odeabank_devam_rate = calculate_effective_rate_helper(deposit, odeabank_devam)

    # Enpara flat rate calculation
    enpara_rate = 0
    for min_limit, max_limit, rate in enpara_ranges:
        if min_limit <= deposit <= max_limit:
            enpara_rate = rate
            break

    # Determine the best rate
    rates = {
        "getir": getir_rate,
        "odeabank_hosgeldin": odeabank_hosgeldin_rate,
        "odeabank_devam": odeabank_devam_rate,
        "enpara": enpara_rate
    }

    best_bank = max(rates, key=rates.get)
    best_rate = rates[best_bank]

    response = {
        "best_bank": best_bank,
        "best_rate": round(best_rate, 2)
    }

    # Calculate 1-day return for the best rate
    one_day_return = calculate_one_day_return(deposit, best_rate)
    response["one_day_return"] = round(one_day_return, 2)

    # Check if split strategy is needed
    split_needed, split_info = check_split_strategy(deposit, best_bank)
    if split_needed:
        # Calculate effective rate after splitting
        val = calculate_effective_rate_after_split(deposit, best_bank, split_info)
        # Calculate 1-day return after splitting
        split_one_day_return = val["one_day_return_after_split"]
        effective_rate_after_split = val["effective_rate_after_split"]

        # Add split information to the response
        response["split_strategy"] = split_info
        response["effective_rate_after_split"] = effective_rate_after_split
        response["one_day_return_after_split"] = round(split_one_day_return, 2)
        print(response)
    return jsonify(response)


def check_split_strategy(deposit, best_bank):
    """
    Check if a split strategy is needed for the best bank.
    Returns a tuple (split_needed: bool, split_info: dict)
    """
    # Define which banks have split configurations
    split_configurations = {
        "odeabank_hosgeldin": odeabank_hosgeldin_splits,
        "getir": getir_splits,
        # Add other banks if they have split configurations
    }

    if best_bank not in split_configurations:
        return False, {}

    splits = split_configurations[best_bank]

    # Iterate through the splits to find the applicable range
    for split in splits:
        split_min_limit, alternative_bank, split_amount = split

        # Determine the current range for the best bank
        best_bank_ranges = {
            "odeabank_hosgeldin": odeabank_hosgeldin,
            "getir": getir_ranges,
            # Add other banks if needed
        }

        current_range = None
        for range_item in best_bank_ranges.get(best_bank, []):
            if range_item[0] <= deposit <= range_item[1]:
                current_range = range_item
                break

        if not current_range:
            continue  # No applicable range found

        min_limit_current, max_limit_current, alt_limit_current, rate_current = current_range
        print(deposit, min_limit_current, split_amount)
        if deposit > min_limit_current - 1 + split_amount:
            continue
        # If deposit is less than or equal to max_limit, recommend splitting
        recommended_best_deposit = min_limit_current - 1
        recommended_alternative_deposit = deposit - recommended_best_deposit

        return True, {
            "recommended_best_deposit": recommended_best_deposit,
            "best_bank": best_bank,
            "alternative_bank": alternative_bank,
            "recommended_alternative_deposit": recommended_alternative_deposit
        }

    return False, {}


if __name__ == "__main__":
    app.run(debug=True)
