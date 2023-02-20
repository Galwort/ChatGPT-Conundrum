from pandas import read_csv
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")
abs_df = read_csv(data_dir + "abstracts.csv")
abs_df = abs_df[abs_df["segment"] == 1]
print(len(abs_df))

# counts = abs_df.groupby(['journal', 'year_range']).size().reset_index(name='count')
# counts.to_csv("journal-year-counts.csv", index=False)
