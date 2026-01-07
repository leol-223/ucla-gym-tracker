import os
import json
from live_activity_vals import get_live_activity_vals
from datetime import datetime, timezone

wooden_url = "https://recreation.ucla.edu/facilities/jwc"
bfit_url = "https://recreation.ucla.edu/facilities/bfit"

wppl = [{2: 1.0}, {2: 0.71, 3: 0.29}, {2: 0.33, 3: 0.5, 6: 0.17}]
bppl = [{2: 0.67, 3: 0.33},{2: 0.57, 3: 0.29, 4: 0.14},{1: 0.17, 2: 0.33, 4: 0.50}]

def get_business(elements, vals):
    bs = []
    for element in elements:
        b = 0
        for e, p in element.items():
            b += p * vals[e]
        bs.append(b)
    return bs

w_vals, dw = get_live_activity_vals(wooden_url)
b_vals, db = get_live_activity_vals(bfit_url)

existing_bfit = {}
existing_wooden = {}
if os.path.exists("data.json"):
    with open('data.json', 'r') as f:
        data = json.load(f)
        existing_bfit = data['bfit']
        existing_wooden = data['wooden']

existing_bfit[dw.isoformat()] = w_vals
existing_wooden[db.isoformat()] = b_vals
with open('data.json', 'w') as f:
    data = {}
    data['bfit'] = existing_bfit
    data['wooden'] = existing_wooden
    print("data", data)
    json.dump(data, f)