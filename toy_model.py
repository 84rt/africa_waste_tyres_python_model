nodes = {
    "A": 100,
    "B": 0,
    "C": 0
}

flows = {
    "1": .3,
    "2": .7,
    "3": .0
}

years = 5

# repeat `years` numer of times:
for year in range(years):
    nodes["A"] *= 1.015

    # add value to B (flow 1)
    nodes["B"] += flows["1"] * nodes["A"]
    # add value to C (flow 2)
    nodes["C"] += flows["2"] * nodes["A"]

    
    # show results
    print(f"year: {year+1}",nodes["A"], int(nodes["B"]), int(nodes["C"]))
    