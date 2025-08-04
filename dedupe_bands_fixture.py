import json
from pathlib import Path

fixture_path = Path("gigs/fixtures/bands.json")
output_path = Path("gigs/fixtures/bands_cleaned.json")

with fixture_path.open("r") as f:
    data = json.load(f)

seen = set()
cleaned = []

for entry in data:
    name_raw = entry['fields']['name']
    name_key = name_raw.strip().lower()
    if name_key not in seen:
        seen.add(name_key)
        entry['fields']['name'] = name_raw.strip()
        cleaned.append(entry)

with output_path.open("w") as f:
    f.write('[\n')
    for i, entry in enumerate(cleaned):
        json.dump(entry, f)
        if i != len(cleaned) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    f.write(']')
