from pandas import read_csv, DataFrame, concat
from numpy import random
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
abs_df = read_csv(data_dir + "abstracts.csv")

# creating the legend column
abs_df.loc[
    (abs_df["score"] < 0.5), "Legend"
] = "Over 50% chance of being real"

abs_df.loc[
    (abs_df["score"] >= 0.5) & (abs_df["score"] < 0.6), "Legend"
] = "Less than 50% chance of being real"  

abs_df.loc[
    (abs_df["score"] >= 0.6) & (abs_df["score"] < 0.7), "Legend"
] = "Less than 40% chance of being real"  

abs_df.loc[
    (abs_df["score"] >= 0.7) & (abs_df["score"] < 0.8), "Legend"
] = "Less than 30% chance of being real"

abs_df.loc[
    (abs_df["score"] >= 0.8) & (abs_df["score"] < 0.9), "Legend"
] = "Less than 20% chance of being real"

abs_df.loc[
    (abs_df["score"] >= 0.9), "Legend"
] = "Less than 10% chance of being real"

# creating year sample data
yr_df = abs_df[abs_df["segment"] == 1]
yr_df_grouped = yr_df.groupby("year_range")
yr_df_sample = DataFrame(columns=yr_df.columns)
for name, group in yr_df_grouped:
    random_rows = group.sample(1600, random_state=random.randint(0, 100000))
    yr_df_sample = concat([yr_df_sample, random_rows])

yr_df_sample.to_csv(data_dir + "year-sample.csv")

# creating journal sample data
jr_df = abs_df[abs_df["segment"] == 1]
jr_df_grouped = jr_df.groupby("journal")
jr_df_sample = DataFrame(columns=jr_df.columns)
for name, group in jr_df_grouped:
    random_rows = group.sample(1400, random_state=random.randint(0, 100000))
    jr_df_sample = concat([jr_df_sample, random_rows])

jr_df_sample.to_csv(data_dir + "journal-sample.csv")

# segment data does not need to be sampled