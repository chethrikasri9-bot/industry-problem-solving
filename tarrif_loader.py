import json

def load_tariffs():
    with open("tariff_config.json", "r") as f:
        return json.load(f)
