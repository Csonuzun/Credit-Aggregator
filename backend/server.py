# server.py

import json
from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from flask_cors import CORS
import math

# Import your new split logic
# (Adjust the import to match your real function/module name)
from split_maximizer import compute_best_split

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Enable CORS for a specific route
# Load bank data from JSON
try:
    with open('banks.json', 'r') as f:
        banks = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(
        "The 'banks.json' file is missing. Please ensure it's in the same directory as 'server.py'."
    )


def calculate_effective_rate_helper(deposit, ranges):
    """
    Helper function to calculate the effective rate for a given deposit and range.
    """
    for range_item in ranges:
        min_limit = range_item.get("min", 0)
        max_limit = range_item.get("max", float('inf'))
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
    return send_from_directory('.', 'index.html')


@app.route('/graph-data', methods=['GET'])
def graph_data():
    """
    Endpoint to provide graph data for all banks.
    Returns deposit labels, deposit values, and corresponding rates for each bank.
    """
    labels = []
    deposit_values = []
    graph_rates = {key: [] for key in banks.keys()}

    # Generate log-spaced deposits
    fixed_min = 2500  # Minimum deposit
    fixed_max = 6000000  # Maximum deposit
    num_points = 500  # Number of points
    logspace_deposits = np.logspace(np.log10(fixed_min), np.log10(fixed_max), num=num_points)
    logspace_deposits = set(int(d) for d in logspace_deposits)  # convert to int & set

    # Collect deposit values from each bank's ranges
    range_deposits = set()
    for bank_key, bank_info in banks.items():
        for rng in bank_info['ranges']:
            min_limit = rng.get("min", 0)
            max_limit = rng.get("max", float('inf'))
            if max_limit != float('inf'):
                range_deposits.add(int(max_limit))

    # Combine
    combined_deposits = logspace_deposits.union(range_deposits)
    deposits_sorted = sorted(combined_deposits)

    # Build data
    for deposit in deposits_sorted:
        deposit_values.append(deposit)
        labels.append(f'{deposit:,} TL')
        for bank_key, bank_info in banks.items():
            rate = calculate_effective_rate_helper(deposit, bank_info['ranges'])
            graph_rates[bank_key].append(round(rate, 2))

    return jsonify({
        "labels": labels,
        "depositValues": deposit_values,
        **{f"{key}_rates": rates for key, rates in graph_rates.items()}
    })


@app.route('/banks', methods=['GET'])
def get_banks():
    """
    Endpoint to return the list of available banks.
    """
    return jsonify({"banks": list(banks.keys())})


@app.route('/calculate-best', methods=['POST'])
def calculate_best():
    """
    Route to calculate:
      1) The best bank for a given deposit and selected banks.
      2) The daily balances if 'days' is provided.
      3) The recommended split from our new 'split_maximizer.py' logic.
    """
    data = request.json
    deposit = data.get('deposit', 0)
    selected_banks = data.get('banks', [])
    days = data.get('days', 0)  # how many days user wants

    # Validate deposit
    if not isinstance(deposit, (int, float)) or deposit <= 0:
        return jsonify({"error": "Invalid deposit amount."}), 400

    # Validate selected banks
    if not isinstance(selected_banks, list) or not all(isinstance(bank, str) for bank in selected_banks):
        return jsonify({"error": "Invalid banks list."}), 400
    if not selected_banks:
        return jsonify({"error": "No banks selected."}), 400

    # Ensure all selected banks exist
    invalid_banks = [bank for bank in selected_banks if bank not in banks]
    if invalid_banks:
        return jsonify({"error": f"Invalid bank names: {', '.join(invalid_banks)}."}), 400

    # Calculate effective rates only for selected banks
    rates = {}
    for bank_key in selected_banks:
        bank_info = banks.get(bank_key)
        if bank_info:
            rate = calculate_effective_rate_helper(deposit, bank_info['ranges'])
            rates[bank_key] = rate

    if not rates:
        return jsonify({"error": "No valid banks found for calculation."}), 400

    # 1) Identify best bank among selected
    best_bank = max(rates, key=rates.get)
    best_rate = rates[best_bank]

    response = {
        "best_bank": best_bank,
        "best_rate": round(best_rate, 2)
    }

    # 2) Calculate one day return
    one_day_return_value = calculate_one_day_return(deposit, best_rate)
    response["one_day_return"] = round(one_day_return_value, 2)

    # 3) NEW SPLIT LOGIC from 'split_maximizer.py'
    split_result = compute_best_split(deposit, selected_banks, days=days)

    if split_result:
        response['split_strategy'] = split_result['split_strategy']
        response['daily_balances'] = split_result['daily_balances']
    else:
        response['split_strategy'] = {}
        response['daily_balances'] = []

    # 4) If 'days' > 0, compute daily balances +on the backend
    if isinstance(days, int) and days > 0:
        daily_balances = compute_daily_balances_helper(deposit, best_rate, days)
        response["daily_balances"] = daily_balances
    else:
        response["daily_balances"] = []

    return jsonify(response)


def calculate_one_day_return(deposit, effective_rate):
    """
    Calculate the 1-day return based on the effective annual rate.
    """
    return deposit * (effective_rate / 100) / 365


def compute_daily_balances_helper(initial_deposit, best_rate, days):
    """
    Compute daily balances for 'days' days, using best_rate (annual %).
    dailyRate = best_rate/100/365.
    Return a list of floats, day 0..day X.
    """
    daily_rate = (best_rate / 100.0) / 365.0
    balance = float(initial_deposit)
    balances = [balance]

    for _ in range(days):
        interest = balance * daily_rate
        balance += interest
        balances.append(balance)
    return balances


if __name__ == "__main__":
    app.run(debug=True)