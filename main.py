from live_activity_vals import get_live_activity_vals

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

def print_ppl_activity(vals):
    for i, name in enumerate(["Push", "Pull", "Legs"]):
        print(f"{name}: {vals[i]*100:.1f}%")

print(f"Wooden center (Updated {str(dw)}):")
print_ppl_activity(get_business(wppl, w_vals))
print(f"\nBfit: (Updated {str(db)})")
print_ppl_activity(get_business(bppl, b_vals))