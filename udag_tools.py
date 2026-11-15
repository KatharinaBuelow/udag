#!/usr/bin/env python3
# 
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob



def check(df,df_result,sc,ts, var,mm='7'):
    #check id meging of df succided:

    realisations=df["realization"].unique()
    regions=df["region"].unique()
    #scenarios=df["scenario"].unique()
    #mid_months=df["mid_month"].unique()
    r=realisations[8]
    rg=regions[3]
    print(sc)
    print(mm)
    print(var)
    print(r)
    print(rg)
    
    
    match = df_result.loc[
        (df_result["realization"] == r)
        & (df_result["region"] == rg)
        & (df_result["scenario"] == sc)
        & (df_result["mid_month"] == mm),
        f"{var}_{ts}"
    ]

    match_org = df.loc[
        (df["realization"] == r)
        & (df["region"] == rg)
        & (df["scenario"] == sc)
        & (df["mid_month"] == mm),
        f"{var}_{ts}"
    ]
    if match.empty or match_org.empty:
        raise ValueError(
            f"No rows found for realization={r!r}, region={rg!r}, "
            f"scenario={sc!r}, mid_month={mm!r}. "
            f"Rows: merged={len(match)}, original={len(match_org)}. "
            f"mid_month dtypes: merged={df_result['mid_month'].dtype}, "
            f"original={df['mid_month'].dtype}; "
            f"original values={df['mid_month'].drop_duplicates().head(12).tolist()}"
        )

    print("match_org (original):")
    print(match_org.to_string())
    print("match (merged):")
    print(match.to_string())

    values_match = match.reset_index(drop=True).equals(
        match_org.reset_index(drop=True)
    )
    print(f"Values match (ignoring index labels): {values_match}")

#--------------------------------------------------------------------
#
#--------------------------------------------------------------------

def plot_change(plotdir,df,col_value, ylabel,r,y1,y2 ,title):

    from matplotlib.patches import Patch

    fig, ax = plt.subplots()
    seasons = df["season"].unique()
    scenarios = df["scenario"].unique()


    colors = ["darkred", "darkblue"] 

    stats, positions, box_colors = [], [], []
    box_width = 0.8 / len(scenarios)

    for i, seas in enumerate(seasons):
        for j, scenario in enumerate(scenarios):
            vals = df.loc[
                (df["season"] == seas) & (df["scenario"] == scenario),
                col_value
            ].dropna()

            if vals.empty:
                continue

            stats.append({
                "label": str(scenario),
                "med": vals.median(),
                "q1": vals.min(),
                "q3": vals.max(),
                "whislo": vals.min(),
                "whishi": vals.max(),
             })
            positions.append(i + 1 + (j - (len(scenarios) - 1) / 2) * box_width * 0.6)
            box_colors.append(colors[j])

    bp = ax.bxp(
        stats, positions=positions, widths=box_width * 0.4,
        patch_artist=True, showfliers=False,
        showcaps=False,
        medianprops={"visible": False},
        whiskerprops={"visible": False},
        )
    for i, (box, color) in enumerate(zip(bp["boxes"], box_colors)):
        box.set_facecolor(color)
        box.set_edgecolor(color)
        box.set_alpha(0.75)
        box.set_linewidth(2.5)


    ax.set_xticks(range(1, len(seasons) + 1))
    ax.set_xticklabels(seasons)
    ax.legend(
        handles=[Patch(facecolor=colors[j], label=scenario, alpha=0.75)
             for j, scenario in enumerate(scenarios)],
        loc="upper right",
        title='scenario',
    )
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_ylim(y1, y2)
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=1)

    fig.savefig(f"{plotdir}/{col_value}_{r}.png", dpi=1200, bbox_inches="tight")
    plt.show()



def rename_season(df_result):
    
    df_result = df_result.rename(
        columns={"mid_month": "season"}).replace(
            {"season": {1: "DJF", 7: "JJA", 4: "MAM", 10: "SON"}}
            )
    return df_result

def rename_year(df_result):

    df_result = df_result.rename(
            columns={"mid_month": "season"}).replace(
                {"season": {7: "YEAR"}}
                )
    return df_result


def create_df(scenarios,var='TG', season='_year_', what='rcp'):
    import os
    import glob

    keys = ["realization", "region", "mid_month", "scenario"]
    wkd=os.getcwd()
    time_slices = ['1971_2000', '2040_2069', '2070_2099']

    for s in scenarios:
        #print(s)
        for t in time_slices:
        #print(t)
            datadirs = glob.glob(os.path.join(wkd, "data", var+season+t+"*"+s+"*"))
        #print(f"Data directories for {s} and {t}: {datadirs}")
            datadirs = [os.path.abspath(path) for path in datadirs]
            df= pd.read_csv(datadirs[0])
        # rename column:
            name=os.path.basename(datadirs[0])
            col_name=name.split('.')[0]
        #print(f"Column name for {s} and {t}: {col_name}")
            df = df.rename(columns={col_name: var+'_'+t})
            df['scenario'] = s
            if t != '1971_2000':
                df_result = df_result.merge(
                    df[keys + [var+'_'+t]],
                    on=keys,
                    how="left",
                    validate="one_to_one",
                    )
            else:
                df_result=df

    # umbennen von mid_month
    if season =='_year_':
        df_result=rename_year(df_result)
    else:
        df_result=rename_season(df_result)

    
    # save df:
    output_path = os.path.join(wkd, "df_"+var+season+what+".csv")
    df_result.to_csv(output_path, index=False)
    print(f"Saved {len(df_result)} rows to {output_path}")
    #print(df.head(3))
    #print(df_result.head(3))
    # dies funktioniert nicht, perhand sehen die Dataframes gut aus
    #check(df,df_result,s,t,var,mm='7')

def cal_diff(df,wkd, var):
    
    ref=var+'_1971_2000'

    for t in [var+'_2040_2069', var+'_2070_2099']:
        print(t)

        df[t+'_diff']=df[t]-df[ref]
        if var =='RRm':
            df[t + "_diff_pro"] = ((df[t] - df[ref]) / df[ref]) * 100
        else:
            print('nichts zu tun bei TG')

    output_path = os.path.join(wkd, "df_"+var+"_diff.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")
