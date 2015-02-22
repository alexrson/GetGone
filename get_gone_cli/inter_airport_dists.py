from collections import defaultdict
distlist =[
    ('SEA', 'SFO', 817),
    ('SFO', 'DEN', 1263),
    ('SEA', 'DEN', 1660),
]

dists = defaultdict(dict)
for a1, a2, d in distlist:
    dists[a1][a2] = d
