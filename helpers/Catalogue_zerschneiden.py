import pandas as pd

# CSV einlesen
df = pd.read_csv("/work/ch0636/g300047/UDAG/index_calculation/catalogue5/CORDEX_variables_catalogue_20261020-05:48:18.csv")

# Startjahr aus time_range extrahieren
df["start_year"] = df["time_range"].str[:4].astype(int)

# 30-Jahres-Blöcke definieren
periods = [
    (1961, 1980),
    (1981, 1990),
    (1991, 2005),
    (2006, 2020),
    (2021, 2040),
    (2041, 2060),
    (2061, 2080),
    (2081, 2101)
]

for start, end in periods:
    subset = df[(df["start_year"] >= start) & (df["start_year"] <= end)]

    if len(subset) > 0:
        outfile = f"/work/ch0636/g300047/UDAG/index_calculation/catalogue5/CORDEX_variables_catalogue_{start}_{end}.csv"
        subset.drop(columns=["start_year"]).to_csv(outfile, index=False)
        print(f"{outfile}: {len(subset)} Zeilen")
