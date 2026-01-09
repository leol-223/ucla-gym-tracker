import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Wooden, Bfit
GYM = "Wooden"
# Push, Pull, Legs
routine = "Push"

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

existing_data = {}
if os.path.exists("data.json"):
    with open('data.json', 'r') as f:
        data = json.load(f)
        if GYM == "Wooden":
            existing_data = data['wooden']
        else:
            existing_data = data['bfit']

def print_ppl_activity(vals):
    for i, name in enumerate(["Push", "Pull", "Legs"]):
        print(f"{name}: {vals[i]*100:.1f}%")

dates = []
activities = []
index_to_push = 0
if routine == "Pull":
    index_to_push = 1
elif routine == "Legs":
    index_to_push = 2

for dw in existing_data:
    if GYM == "Wooden":
        ppl = get_business(wppl, existing_data[dw])
    else:
        ppl = get_business(bppl, existing_data[dw])
    dates.append(datetime.fromisoformat(dw))
    activities.append(ppl[index_to_push])
# print(f"\nBfit: (Updated {str(db)})")
# print_ppl_activity(get_business(bppl, b_vals))
print('Num data points:', len(activities))
buckets_push_orig = {i: [] for i in range(5, 24)}

for i, d in enumerate(dates):
    buckets_push_orig[d.hour].append(activities[i])

buckets_push = {i: 0 for i in range(5, 24)}
for k, v in buckets_push_orig.items():
    if len(v) == 0:
        buckets_push[k] = 0
    else:
        buckets_push[k] = sum(v) / len(v)
print(buckets_push)
def format_hour(h):
    if h == 0: return "12 AM"
    if h < 12: return f"{h} AM"
    if h == 12: return "12 PM"
    return f"{h-12} PM"

keys_formatted = [format_hour(k) for k in buckets_push.keys()]
values = list(buckets_push.values())

# 2. Setup a larger, wider window
plt.style.use('seaborn-v0_8-white') 
fig, ax = plt.subplots(figsize=(14, 7)) # Increased width significantly

# 3. Create the bars with a more "premium" color
# Using a modern Indigo/Navy: #3F51B5 or a Deep Teal: #264653
bar_color = '#34495e' 
bars = ax.bar(keys_formatted, values, color=bar_color, width=0.75, edgecolor=None, alpha=0.85)

# 4. Add data labels on top 
# Increased font size and used a slightly offset color for readability
labels = [f'{sum(v)/len(v)*100:.1f}% ({len(v)})' if len(v) > 0 else '' for v in list(buckets_push_orig.values())]
ax.bar_label(bars, labels=labels, padding=5, fontsize=10, fontweight='600', color='#2c3e50')

# 5. Make the Y-axis show percentages too (Consistency is key!)
ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])

# 6. Aesthetic Clean-up
ax.set_title(f'{GYM} Activity: {routine}', fontsize=18, pad=25, fontweight='bold', color='#1a1a1a')
ax.set_xlabel('Time of Day', fontsize=13, labelpad=15, fontweight='500')
ax.set_ylabel('Activity', fontsize=13, labelpad=15, fontweight='500')

# Modernizing the frame
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#dddddd')
ax.spines['bottom'].set_color('#dddddd')

# Clean up the X-axis (prevent squishing)
plt.xticks(rotation=0, fontsize=10) 

# Add a very subtle horizontal grid
ax.yaxis.grid(True, linestyle='-', which='major', color='#eeeeee', zorder=0)
ax.set_axisbelow(True) 

plt.tight_layout()
plt.show()