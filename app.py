from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__, static_folder='.')


@app.route('/')
def index():
    # Serve the index.html file when visiting the root URL
    return send_from_directory('.', 'index.html')


@app.route('/calculate', methods=['POST'])
def calculate_effective_rate():
    data = request.json
    deposit = data.get('deposit', 0)

    # Updated ranges with alt limits and interest rates for Getir Finans
    ranges = [
        (2500, 25000, 2500, 50),
        (25001, 50000, 5000, 50),
        (50001, 100000, 7500, 50),
        (100001, 500000, 20000, 50),
        (500001, 1000000, 40000, 50),
        (1000001, 2000000, 75000, 50),
        (2000001, 2100000, 100000, 50),
        (2100001, 5100000, 100000, 30),
        (5100001, float('inf'), 100000, 30)  # For values above 5,100,000
    ]

    # Call the helper function to calculate effective rate
    effective_rate = calculate_effective_rate_helper(deposit, ranges)
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
    # Updated ranges for Getir Finans and Enpara
    getir_ranges = [
        (2500, 25000, 2500, 50),
        (25001, 50000, 5000, 50),
        (50001, 100000, 7500, 50),
        (100001, 500000, 20000, 50),
        (500001, 1000000, 40000, 50),
        (1000001, 2000000, 75000, 50),
        (2000001, 2100000, 100000, 50),
        (2100001, 5100000, 100000, 30),
        (5100001, 6000000, 100000, 30)  # Limit adjusted to 6,000,000
    ]

    enpara_ranges = [
        (0, 100000, 32.00),
        (100001, 500000, 35.00),
        (500001, 1000000, 38.00),
        (1000001, float('inf'), 41.00)
    ]

    labels = []
    getir_rates = []
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
        "enpara_rates": enpara_rates
    })


@app.route('/calculate-best', methods=['POST'])
def calculate_best():
    data = request.json
    deposit = data.get('deposit', 0)

    getir_ranges = [
        (2500, 25000, 2500, 50),
        (25001, 50000, 5000, 50),
        (50001, 100000, 7500, 50),
        (100001, 500000, 20000, 50),
        (500001, 1000000, 40000, 50),
        (1000001, 2000000, 75000, 50),
        (2000001, 2100000, 100000, 50),
        (2100001, 5100000, 100000, 30),
        (5100001, float('inf'), 100000, 30)
    ]

    enpara_ranges = [
        (0, 100000, 32.00),
        (100001, 500000, 35.00),
        (500001, 1000000, 38.00),
        (1000001, float('inf'), 41.00)
    ]

    getir_rate = calculate_effective_rate_helper(deposit, getir_ranges)

    # Enpara flat rate calculation
    enpara_rate = 0
    for min_limit, max_limit, rate in enpara_ranges:
        if min_limit <= deposit <= max_limit:
            enpara_rate = rate
            break

    # Compare rates
    if getir_rate > enpara_rate:
        best_bank = "Getir Finans"
        best_rate = round(getir_rate, 2)
    else:
        best_bank = "Enpara"
        best_rate = round(enpara_rate, 2)

    return jsonify({"best_bank": best_bank, "best_rate": best_rate})


if __name__ == "__main__":
    app.run(debug=True)
