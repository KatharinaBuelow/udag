#!/usr/bin/env python3

import pandas as pd


def check(df, df_result, sc, ts, var, mm="7"):
    value_column = f"{var}_{ts}"
    key_columns = ["realization", "region", "mid_month", "scenario"]

    original = df.loc[
        df["scenario"].eq(sc), key_columns + [value_column]
    ].copy()
    merged = df_result.loc[
        df_result["scenario"].eq(sc), key_columns + [value_column]
    ].copy()

    numeric_mm = pd.to_numeric(mm, errors="coerce")
    if pd.notna(numeric_mm):
        original = original.loc[
            pd.to_numeric(original["mid_month"], errors="coerce").eq(numeric_mm)
        ]
        merged = merged.loc[
            pd.to_numeric(merged["mid_month"], errors="coerce").eq(numeric_mm)
        ]
    else:
        original = original.loc[original["mid_month"].astype(str).eq(str(mm))]
        merged = merged.loc[merged["mid_month"].astype(str).eq(str(mm))]

    if original.empty or merged.empty:
        raise ValueError(
            f"No rows to compare for scenario={sc!r}, mid_month={mm!r}: "
            f"original={len(original)}, merged={len(merged)}"
        )

    comparison = original.merge(
        merged,
        on=key_columns,
        how="outer",
        suffixes=("_original", "_merged"),
        validate="one_to_one",
        indicator=True,
    )
    original_values = comparison[f"{value_column}_original"]
    merged_values = comparison[f"{value_column}_merged"]
    values_equal = original_values.eq(merged_values).fillna(False) | (
        original_values.isna() & merged_values.isna()
    )
    rows_match = comparison["_merge"].eq("both") & values_equal
    differences = comparison.loc[
        ~rows_match,
        key_columns
        + [f"{value_column}_original", f"{value_column}_merged", "_merge"],
    ]

    if differences.empty:
        print(
            f"All {len(comparison)} values match for "
            f"{value_column}, scenario={sc!r}, mid_month={mm!r}."
        )
        return True

    print(f"Found {len(differences)} differences for {value_column}:")
    print(differences.to_string(index=False))
    return False
