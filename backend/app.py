import json
from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes

# Load bank data from JSON file
try:
    with open('banks.json', 'r') as f:
        banks = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("The 'banks.json' file is missing. Please ensure it's in the same directory as 'app.py'.")

# Define split configurations separately or within banks.json
split_dict = {
    "odeabank_hosgeldin": [
        (50000, "enpara", 7426),
        (100000, "enpara", 26651),
        (250000, "odeabank_devam", 73294),
        (500000, "getir_finans", 237529),
        (750000, "odeabank_devam", 210794),
        (1000000, "getir_finans", 548958)
    ],
    "getir_finans": [
        (25000, "enpara", 7426),
        (50000, "enpara", 7426),
        (100000, "odeabank_hosgeldin", 120743),
        (500000, "odeabank_hosgeldin", 310386),
        (1000000, "odeabank_hosgeldin", 616815)
    ]
}


def calculate_effective_rate_helper(deposit, ranges):
    """
    Helper function to calculate the effective rate for a given deposit and range.
    """
    for range_item in ranges:
        min_limit = range_item.get("min")
        max_limit = range_item.get("max")
        min_balance = range_item.get("min_balance", 0)
        rate = range_item.get("rate", 0)

        if min_limit <= deposit <= max_limit:
            interest_eligible = deposit - min_balance
            if interest_eligible > 0:
                annual_interest = interest_eligible * (rate / 100)
                return (annual_interest / deposit) * 100
            return 0.0
    return 0.0


@app.route('/')
def index():
    """
    Serve the index.html file.
    """
    return send_from_directory('..', 'index.html')


@app.route('/calculate', methods=['POST'])
def calculate_effective_rate():
    """
    Route to calculate the effective interest rate for a given deposit.
    """
    data = request.json
    deposit = data.get('deposit', 0)
    bank_name = data.get('bank_name', 'getir_finans')  # Default to 'getir_finans'

    if bank_name not in banks:
        return jsonify({"error": "Invalid bank name."}), 400

    # Call the helper function to calculate the effective rate
    effective_rate = calculate_effective_rate_helper(deposit, banks[bank_name]['ranges'])
    return jsonify({"effective_rate": round(effective_rate, 2)})


@app.route('/graph-data', methods=['GET'])
def graph_data():
    """
    Endpoint to provide graph data for all banks.
    Returns deposit labels and corresponding rates for each bank.
    """
    labels = []
    graph_rates = {key: [] for key in banks.keys()}

    # Generate log-spaced deposits
    fixed_min = 2500  # Minimum deposit
    fixed_max = 6000000  # Maximum deposit
    num_points = 100  # Number of points in the graph
    deposits = np.logspace(np.log10(fixed_min), np.log10(fixed_max), num=num_points)

    for deposit in deposits:
        deposit = int(deposit)  # Convert to integer for simplicity
        labels.append(f'{deposit:,} TL')

        for bank_key, bank_info in banks.items():
            rate = calculate_effective_rate_helper(deposit, bank_info['ranges'])
            graph_rates[bank_key].append(round(rate, 2))

    return jsonify({
        "labels": labels,
        **{f"{key}_rates": rates for key, rates in graph_rates.items()}
    })


@app.route('/calculate-best', methods=['POST'])
def calculate_best():
    """
    Route to calculate the best bank for a given deposit.
    """
    data = request.json
    deposit = data.get('deposit', 0)

    if not isinstance(deposit, (int, float)) or deposit <= 0:
        return jsonify({"error": "Invalid deposit amount."}), 400

    rates = {}
    for bank_key, bank_info in banks.items():
        rate = calculate_effective_rate_helper(deposit, bank_info['ranges'])
        rates[bank_key] = rate

    best_bank = max(rates, key=rates.get)
    best_rate = rates[best_bank]

    response = {
        "best_bank": best_bank,
        "best_rate": round(best_rate, 2)
    }

    one_day_return = calculate_one_day_return(deposit, best_rate)
    response["one_day_return"] = round(one_day_return, 2)

    split_needed, split_info = check_split_strategy(deposit, best_bank)
    if split_needed:
        val = calculate_effective_rate_after_split(deposit, best_bank, split_info)
        response["split_strategy"] = split_info
        response["effective_rate_after_split"] = val["effective_rate_after_split"]
        response["one_day_return_after_split"] = val["one_day_return_after_split"]

    return jsonify(response)


def calculate_one_day_return(deposit, effective_rate):
    """
    Calculate the 1-day return based on the effective annual rate.
    """
    return deposit * (effective_rate / 100) / 365


def calculate_effective_rate_after_split(deposit, best_bank, split_info):
    """
    Calculate the effective interest rate and 1-day return after splitting the deposit between two banks.
    """
    best_deposit = split_info['recommended_best_deposit']
    alternative_deposit = split_info['recommended_alternative_deposit']
    alternative_bank = split_info['alternative_bank']

    best_bank_info = banks.get(best_bank)
    alternative_bank_info = banks.get(alternative_bank)

    if not best_bank_info or not alternative_bank_info:
        return {
            "effective_rate_after_split": 0.0,
            "one_day_return_after_split": 0.0
        }

    best_rate = calculate_effective_rate_helper(best_deposit, best_bank_info['ranges'])
    alternative_rate = calculate_effective_rate_helper(alternative_deposit, alternative_bank_info['ranges'])

    best_bank_return = calculate_one_day_return(best_deposit, best_rate)
    alternative_bank_return = calculate_one_day_return(alternative_deposit, alternative_rate)

    total_one_day_return_after_split = best_bank_return + alternative_bank_return
    effective_rate_after_split = (total_one_day_return_after_split * 365) / deposit * 100

    return {
        "effective_rate_after_split": round(effective_rate_after_split, 2),
        "one_day_return_after_split": round(total_one_day_return_after_split, 2)
    }


def check_split_strategy(deposit, best_bank):
    """
    Check if a split strategy is needed for the best bank.
    Returns a tuple (split_needed: bool, split_info: dict)
    """
    if best_bank not in split_dict:
        return False, {}

    splits = split_dict[best_bank]

    for split in splits:
        split_min_limit, alternative_bank, split_amount = split
        best_bank_info = banks.get(best_bank)

        if not best_bank_info:
            continue

        applicable_range = None
        for range_item in best_bank_info['ranges']:
            if range_item['min'] <= deposit <= range_item['max']:
                applicable_range = range_item
                break

        if not applicable_range:
            continue

        min_balance = applicable_range.get('min_balance', 0)
        if deposit >= min_balance + split_amount:
            recommended_best_deposit = min_balance
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