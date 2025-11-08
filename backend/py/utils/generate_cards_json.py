# converts minified (handcoded) json data to formal json cards

import json

import pandas
from core.path_manager import METADATA_DIR

cards_input = METADATA_DIR / "cards_minified.json"
cards_output = METADATA_DIR / "cards.json"

with open(cards_input, "r") as f:
    o = json.load(f)

df = pandas.DataFrame(o)

arr = ["onyx", "sapphire", "emerald", "ruby", "diamond"]
sorted = ["diamond", "sapphire", "emerald", "ruby", "onyx"]
costs = ["onyx", "diamond", "ruby", "sapphire", "emerald"]

df = df.rename(
    columns={
        "bonus": "engine",
        "points": "prestige",
    }
)

# from number to name
df["engine"] = [arr[i] for i in df["engine"]]

# sort 'engine' by doing magic jack shit
from functools import reduce

disassembled = [df[df["engine"] == gem] for gem in sorted]
assembled = reduce(lambda a, b: pandas.concat([a, b], ignore_index=True), disassembled)

df = assembled

# sort by tier afterwards
df.sort_values(by=["tier"], inplace=True)

# mutate 'cost' col by appending JSON costs
costs_col = df["cost"]
costs_col = [{costs[i]: cost_row[i] for i in range(5)} for cost_row in costs_col]
df["cost"] = costs_col

# add index
df = df.reset_index(names="id")

json_str = df.to_json(orient="records")

parsed = json.loads(json_str)
pretty = json.dumps(parsed, indent=4)

with open(cards_output, "w") as f:
    f.write(pretty)
