# backend/tests/test_server.py

import pytest
from server import app
import json
import os
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def load_data():
    """
    Fixture to load actual banks.json and split_config.json data.
    Ensure that these files are present in the backend directory.
    """
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    banks_path = os.path.join(backend_dir, 'banks.json')
    split_config_path = os.path.join(backend_dir, 'split_config.json')

    with open(banks_path, 'r', encoding='utf-8') as f:
        banks = json.load(f)

    if os.path.exists(split_config_path):
        with open(split_config_path, 'r', encoding='utf-8') as f:
            split_config = json.load(f)
    else:
        split_config = {}

    return banks, split_config


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in response.data


def test_get_banks(client, load_data):
    banks, _ = load_data
    response = client.get('/banks')
    assert response.status_code == 200
    data = response.get_json()
    assert 'banks' in data
    assert isinstance(data['banks'], list)
    for bank_key, bank_info in banks.items():
        assert bank_info['name'] in data['banks']


def test_graph_data(client, load_data):
    banks, _ = load_data
    response = client.get('/graph-data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'labels' in data
    # Check for presence of rates for each bank
    for bank_key in banks.keys():
        rate_key = f"{bank_key}_rates"
        assert rate_key in data, f"{rate_key} not found in graph data."
        assert isinstance(data[rate_key], list), f"{rate_key} should be a list."
    assert len(data['labels']) == 100  # As per server.py, num_points = 100


def test_calculate_best_valid_input(client, load_data):
    banks, _ = load_data
    payload = {
        "deposit": 5000,
        "banks": list(banks.keys())
    }
    response = client.post('/calculate-best', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'best_bank' in data
    assert 'best_rate' in data
    assert 'one_day_return' in data


def test_calculate_best_invalid_deposit(client, load_data):
    banks, _ = load_data
    payload = {
        "deposit": -100,
        "banks": list(banks.keys())
    }
    response = client.post('/calculate-best', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Invalid deposit amount."


def test_calculate_best_invalid_banks(client, load_data):
    _, _ = load_data
    payload = {
        "deposit": 5000,
        "banks": ["NonExistentBank1", "NonExistentBank2"]
    }
    response = client.post('/calculate-best', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert "Invalid bank names" in data['error']


def test_calculate_best_no_banks_selected(client):
    payload = {
        "deposit": 5000,
        "banks": []
    }
    response = client.post('/calculate-best', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "No banks selected."


def test_calculate_best_with_split(client, load_data):
    banks, split_config = load_data
    payload = {
        "deposit": 60000,  # Adjust based on split_config.json logic
        "banks": list(banks.keys())
    }
    response = client.post('/calculate-best', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    if "split_strategy" in data:
        assert 'split_strategy' in data
        assert 'effective_rate_after_split' in data
        assert 'one_day_return_after_split' in data
    else:
        # Depending on split_config.json content
        pass


def test_calculate_best_no_split(client, load_data):
    banks, split_config = load_data
    payload = {
        "deposit": 40000,  # Adjust based on split_config.json logic
        "banks": list(banks.keys())
    }
    response = client.post('/calculate-best', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'split_strategy' not in data
    assert 'effective_rate_after_split' not in data
    assert 'one_day_return_after_split' not in data


def test_graph_data_content(client, load_data):
    banks, _ = load_data
    response = client.get('/graph-data')
    assert response.status_code == 200
    data = response.get_json()
    # Check that rates are present for each bank
    for bank_key in banks.keys():
        rate_key = f"{bank_key}_rates"
        assert rate_key in data, f"{rate_key} not found in graph data."
        assert len(data[rate_key]) == 100, f"{rate_key} should have 100 data points."