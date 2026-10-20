import pandas as pd

# CSV einlesen
df = pd.read_csv("catalogue/CORDEX-CMIP6_variables_catalogue_20261012-19:01:31.csv")

# Startjahr aus time_range extrahieren
df["start_year"] = df["time_range"].str[:4].astype(int)

# 30-Jahres-Blöcke definieren
periods = [
    (1961, 1990),
    (1991, 2020),
    (2021, 2050),
    (2051, 2080),
    (2081, 2110),
    (2111, 2140),
    (2141, 2170),
    (2171, 2200)
]

for start, end in periods:
    subset = df[(df["start_year"] >= start) & (df["start_year"] <= end)]

    if len(subset) > 0:
        outfile = f"catalogue/CORDEX-CMIP6_variables_catalogue_{start}_{end}.csv"
        subset.drop(columns=["start_year"]).to_csv(outfile, index=False)
        print(f"{outfile}: {len(subset)} Zeilen")