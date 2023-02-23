from pandas import read_csv, set_option
from os import getcwd

# set_option('display.width', None)

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")
abs_df = read_csv(data_dir + "abstracts.csv")
yr_df_sample = read_csv(data_dir + "year-sample.csv")


seg_df_sample = abs_df.merge(
    yr_df_sample[["article_url", "year_range", "url"]],
    on=["article_url", "year_range", "url"],
    how="inner",
)

print("Instances in year-sample.csv: ", len(yr_df_sample))
print("Instances in segment sample: ", len(seg_df_sample))
print("Missing instances: ", abs((len(yr_df_sample) * 3) - len(seg_df_sample)))
print("")

# Create a boolean mask that identifies the duplicate rows
duplicate_mask = seg_df_sample.duplicated(subset=['article_url', 'year_range', 'url', 'segment'])

# Index the dataframe using the duplicate_mask to print out the duplicate rows
duplicate_rows = seg_df_sample[duplicate_mask]
print(len(duplicate_rows))
print(duplicate_rows)
