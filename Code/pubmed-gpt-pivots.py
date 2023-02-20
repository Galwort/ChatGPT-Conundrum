from pandas import read_csv

abs_df = read_csv("abstracts.csv")
abs_df = abs_df[abs_df["segment"] == 1]
abs_df["word_count"] = abs_df["abstract"].str.split().str.len()

abs_df_words = abs_df.pivot_table(index="year_range", columns="journal", aggfunc="mean", values="word_count")
# print(abs_df_words)

abs_df_chars = abs_df.pivot_table(index="year_range", columns="journal", aggfunc="mean", values="characters")
# print(abs_df_chars)

