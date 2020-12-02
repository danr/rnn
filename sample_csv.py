import numpy as np
from collections import defaultdict
from numpy.random import default_rng
import pandas as pd
df = pd.read_csv('./r16.csv.gz')
maxC = 10
maxR = 10
L = 100
N = 2 ** 18
ranks = 'phylum class order family genus'.split()
rng = default_rng()

def separate(df, rank, vs):
    subs = defaultdict(list)
    for i, v in enumerate(vs):
        # print(v)
        dfv = df[df[rank] == v]
        dfv = dfv.sample(frac=1)
        cut = int(len(dfv) * 0.8)
        for name, sub in [('train', dfv[:cut]), ('test', dfv[cut:])]:
            sub = sub.sample(N // len(vs), replace=True)
            sub['class'] = i
            sub['seq'] = sub['seq'].apply(lambda s: s[rng.integers(len(s) - L):][:L])
            subs[name] += [sub[['class', 'seq', rank]]]

    return {
        name: pd.concat(sub).sample(frac=1)
        for name, sub in subs.items()
    }

seps = separate(df, 'family', ['Bacillaceae', 'Paenibacillaceae'])
for name, sep in seps.items():
    sep.to_csv(f'Bacillales-{name}.csv.gz', index=False)

for rank in ranks:
    vc = df[rank].value_counts()
    max = vc[0]
    vc = vc[vc > vc[0]/maxR][:maxC]
    seps = separate(df, rank, vc.index)
    for name, sep in seps.items():
        sep.to_csv(f'r16-{rank}-{name}.csv.gz', index=False)

