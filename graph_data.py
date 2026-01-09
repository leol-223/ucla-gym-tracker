import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

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

existing_bfit = {}
existing_wooden = {}
if os.path.exists("data.json"):
    with open('data.json', 'r') as f:
        data = json.load(f)
        existing_bfit = data['bfit']
        existing_wooden = data['wooden']

def print_ppl_activity(vals):
    for i, name in enumerate(["Push", "Pull", "Legs"]):
        print(f"{name}: {vals[i]*100:.1f}%")

dates = []
points = []

for dw in existing_wooden:
    print(f"Bfit (Updated {dw}):")
    ppl = get_business(wppl, existing_wooden[dw])
    print(ppl)
    dates.append(datetime.fromisoformat(dw))
    points.append(ppl[1])

print(dates, points)

# print(f"\nBfit: (Updated {str(db)})")
# print_ppl_activity(get_business(bppl, b_vals))

plt.plot(dates, points)
plt.show()