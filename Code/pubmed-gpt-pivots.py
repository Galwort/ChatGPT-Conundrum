from pandas import read_csv, DataFrame, concat
from os import getcwd
from scipy import stats

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
tbl_dir = dir.replace("Code", "Tables\\")

# importing sample data
yr_df_sample = read_csv(data_dir + "year-sample.csv")
# jr_df_sample = read_csv(data_dir + "journal-sample.csv")
abs_df = read_csv(data_dir + "abstracts.csv")

# creating pivots
yr_df_sample.pivot_table(index="year_range", columns="Legend", aggfunc="size").to_csv(
    tbl_dir + "year-pivot.csv"
)
yr_df_sample.pivot_table(index="journal", columns="Legend", aggfunc="size").to_csv(
    tbl_dir + "journal-pivot.csv"
)
yr_df_sample.pivot_table(index="segment", columns="Legend", aggfunc="size").to_csv(
    tbl_dir + "segment-pivot.csv"
)

# big table for word count and p-value
bt_df = DataFrame(columns=["year_range","journal","word_count","p_value"])

for jr in abs_df["journal"].unique():
    for yr in abs_df["year_range"].unique():
        ptr_df = abs_df.loc[(abs_df["journal"] == jr) & (abs_df["year_range"] == yr)]
        otr_df = abs_df.loc[(abs_df["journal"] != jr) & (abs_df["year_range"] != yr)]
        wc = ptr_df["word_count"].mean()
        _, pv = stats.ttest_ind(
            ptr_df["word_count"],
            otr_df["word_count"],
            equal_var=False
        )
        x_df = DataFrame(
            {"year_range": yr, "journal": jr, "word_count": wc, "p_value": pv},
            index=[0]
        )
        bt_df = concat([bt_df, x_df], ignore_index=True)

yr_tot_df = DataFrame(columns=["year_range","journal","word_count","p_value"])
for yr in abs_df["year_range"].unique():
    ptr_df = abs_df.loc[abs_df["year_range"] == yr]
    otr_df = abs_df.loc[abs_df["year_range"] != yr]
    wc = ptr_df["word_count"].mean()
    _, pv = stats.ttest_ind(
        ptr_df["word_count"],
        otr_df["word_count"],
        equal_var=False
    )
    x_df = DataFrame(
        {"year_range": yr, "journal": "Total", "word_count": wc, "p_value": pv},
        index=[0]
    )
    yr_tot_df = concat([yr_tot_df, x_df], ignore_index=True)
bt_df = concat([bt_df, yr_tot_df], ignore_index=True)

jr_tot_df = DataFrame(columns=["year_range","journal","word_count","p_value"])
for jr in abs_df["journal"].unique():
    ptr_df = abs_df.loc[abs_df["journal"] == jr]
    otr_df = abs_df.loc[abs_df["journal"] != jr]
    wc = ptr_df["word_count"].mean()
    _, pv = stats.ttest_ind(
        ptr_df["word_count"],
        otr_df["word_count"],
        equal_var=False
    )
    x_df = DataFrame(
        {"year_range": "Total", "journal": jr, "word_count": wc, "p_value": pv},
        index=[0]
    )
    jr_tot_df = concat([jr_tot_df, x_df], ignore_index=True)
bt_df = concat([bt_df, jr_tot_df], ignore_index=True)

ptr_df = abs_df
otr_df = abs_df
wc = ptr_df["word_count"].mean()
_, pv = stats.ttest_ind(
    ptr_df["word_count"],
    otr_df["word_count"],
    equal_var=False
)
tot_df = DataFrame(
    {"year_range": "Total", "journal": "Total", "word_count": wc, "p_value": pv},
    index=[0]
)
bt_df = concat([bt_df, tot_df], ignore_index=True)

bt_pivot = bt_df.pivot_table(
    index="year_range",
    columns="journal",
    values=["word_count","p_value"]
)
bt_pivot = bt_pivot.round(4)
bt_pivot.columns = [f"{k} {j}" for j, k in bt_pivot.columns]
# bt_pivot = bt_pivot.reindex(sorted(bt_pivot.columns), axis=1)
journals = sorted(bt_df['journal'].unique())
column_order = [f"{j} {col}" for j in journals for col in ['word_count', 'p_value']]
bt_pivot = bt_pivot.reindex(columns=column_order)
bt_pivot.to_csv(tbl_dir + "statistics-pivot.csv")