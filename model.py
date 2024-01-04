# define the nodes and their values for the first year
nodes = {
    "A. Production": 107000.0,
    "B. Import": 131000.0,
    "B`. Illegal import": [],
    "C. Sales (new)": 0.0,
    "D. Sales (second-hand)": 0.0,
    "E. Use phase": 920000.0,
    # "F. Tyres remaning in use phase": 0.0,
    "G. Collection points": 0.0,
    "H. Reuse and retreading": 0.0,
    "I. Formal collection": 93400, 
    "J. Informal collection": 0.0, 
    "K. Mirco-collection": 29000, 
    "L. Wear and tear": 0.0, 
    "M. Landfilling/illegal dumping": [0.0, 0.0, 0.0], 
    # "N. Historical stockpiles": 22000000,
    "O. Export of Waste": 14400, 
    "P. Long-term stockpilling": 213000, # max cap is 250000, when full it all goes to "J. Informal collection"
    "Q. Depots/pre-processing": 22700, 
    "R. Formal processing": 0.0, 
    "S. Informal processing": 0.0, 
    "T. Crumbing": 0.0, 
    "U. Pyrolysis": 0.0, 
    "V. Energy recovery": 0.0, 
    "W. Secondary Industry": 0.0
    }

# define the flow multiples for the nodes
flows_multiples = {
    "1 (A to C)": 1,
    "2 (B to C)": 1,
    "3 (B` to D)": 1,
    "4 (C to E)": 1,
    "5 (D to E)": 1,
    "6 (E to L)": 0.035,                # estimated by taking a 10 year CAGR for tyres
    # "7": 1 - 0.054347826 - 0.326086957, 
    # "8": 1,
    "9 (E to G)": 0.326086957,          # estimated by taking current year data into a ratio: 300,000 / 920,000
    "10": 0,                            # not enough data to make an estimate 
    # "11": 0,                          
    "12 (H to D)": 1,
    "13 (G to I)": 0.214666667,         # estimated by taking current year data into a ratio: (93,400 - 29,000) / 300,000
    "14 (G to J)": 1 - 0.214666667,     # the remained of tons in `G. Collection points`
    "15 ": 1,
    "16": 93,                           # estimated by taking the remained of J. Informal collection - flow26 - flow15
    "17": 0.001318182,                  # estimated by taking current year data into a ratio: 14,500 / ???
    "18": 0.001318182,                  # estimated by taking current year data into a ratio: 14,500 / 22,000,000
    "19 (K to I)": 1,
    "20": .24,                          # estimated by taking current year data into a ratio: 27,600 / 93,400
    "21": .15,                          # estimated by taking current year data into a ratio: 14,400 / 93,400
    "22 (I to P)": 0.602783726,                  # estimated by taking current year data into a ratio: (93,400 - 27,600 - 14,400) / 93,400
    "23": 0,
    "24": 1,
    "25": 0,
    "26": 0,
    "27": .43,
    "28": .21,
    "29": .36,
    "30": 1,
}

previous_year_use_phase = nodes["E. Use phase"]
demand_increase = 1.045
years = 1
data1 = []
data2 = []

# run the model `years` number of times
for year in range(years):
    # THIS IS WHERE THE FLOWS ARE DEFINED

    # ======================================================= #

    # Calculate `C. Sales (new)` by adding up `A. Production` and `B. Import.
    nodes["C. Sales (new)"] = nodes["A. Production"] + nodes["B. Import"]
    print("C", nodes["C. Sales (new)"])
    
    # Increase `A. Production` and `B. Import` by 4.5% per year after the first year
    nodes["A. Production"] *= demand_increase
    nodes["B. Import"] *= demand_increase


    # In order to calulate the value of `D. Sales (second-hand)` we need to know the demand_gap_for_use_phase
    # Which is calculated by checking the net change in `E. Use phase`, for wich we need to know the value of `G. Collection points` and `L. Wear and tear`
    # calculate the value of `G. Collection points`
    nodes["G. Collection points"] = nodes["E. Use phase"] * flows_multiples["9 (E to G)"]
    # calculate the value of `L. Wear and tear`
    nodes["L. Wear and tear"] = nodes["E. Use phase"] * flows_multiples["6 (E to L)"]

    # the demand gap is calculated by taking "demand change from year to year (in year one it's 0)", adding G and L and subtracting C
    demand_gap_for_use_phase = nodes["E. Use phase"] - previous_year_use_phase + nodes["G. Collection points"] + nodes["L. Wear and tear"] - nodes["C. Sales (new)"]
    
    # previous year and next year use phase is updated
    previous_year_use_phase = nodes["E. Use phase"]
    nodes["E. Use phase"] *= demand_increase

    print(demand_gap_for_use_phase)

    # `D. Sales (second-hand)` must be equal to `demand_gap_for_use_phase` to bring 4.5% growth in demand
    # `D. Sales (second-hand)` is composed of `B`. Illegal import` and `H. Reuse and retreading`
    # Seince we don't know their value we can asign them to a range where B` + H = D, and B` = [0, D] and H = [0, D]
    nodes["B`. Illegal import"] = [0, demand_gap_for_use_phase/2, demand_gap_for_use_phase]
    nodes["H. Reuse and retreading"] = [demand_gap_for_use_phase - i for i in nodes["B`. Illegal import"]]

    # Calcualte `I. Formal Collection`
    nodes["I. Formal collection"] = nodes["G. Collection points"] * flows_multiples["13 (G to I)"]

    # Calcualte `J. Informal collection`
    nodes["J. Informal collection"] = nodes["G. Collection points"] * flows_multiples["14 (G to J)"]
    
    # Calcualte `M. Landfilling/illegal dumping`
    goes_to_m_from_j = [nodes["J. Informal collection"] - h for h in nodes["H. Reuse and retreading"]]    
    nodes["M. Landfilling/illegal dumping"] += goes_to_m_from_j

    # Calculate `P. Long-term stockpiling`, if it overflows add it to `M. Landfilling/illegal dumping`
    goes_to_p = nodes["I. Formal collection"] * flows_multiples["22 (I to P)"]
    if nodes["P. Long-term stockpilling"] + goes_to_p > 250000:
        # the amount over 250000 goes to `M. Landfilling/illegal dumping`
        add_to_m = nodes["P. Long-term stockpilling"] + goes_to_p - 250000
        nodes["M. Landfilling/illegal dumping"] = [i + add_to_m for i in nodes["M. Landfilling/illegal dumping"]]

    data1.append([nodes["M. Landfilling/illegal dumping"][1], nodes["P. Long-term stockpilling"], nodes["P. Long-term stockpilling"][0]])
    # data2.append()



# generate plots
# save the processed data