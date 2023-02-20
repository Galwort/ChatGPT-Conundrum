from pandas import read_csv
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
tbl_dir = dir.replace("Code", "Tables\\")

# importing sample data
yr_df_sample = read_csv(data_dir + "year-sample.csv")
jr_df_sample = read_csv(data_dir + "journal-sample.csv")
abs_df = read_csv(data_dir + "abstracts.csv")

# creating pivots
yr_df_sample.pivot_table(index="year_range", columns="Legend", aggfunc="size").to_csv("Pivots/year-pivot.csv")
jr_df_sample.pivot_table(index="journal", columns="Legend", aggfunc="size").to_csv("Pivots/journal-pivot.csv")
abs_df.pivot_table(index="segment", columns="Legend", aggfunc="size").to_csv("Pivots/segment-pivot.csv")

# word counts
word_df = abs_df.pivot_table(index="year_range", columns="journal", aggfunc="mean", values="word_count")