from pandas import read_csv, set_option
from os import getcwd
import matplotlib.pyplot as plt

# set_option('display.width', None)

colors = [
    "#1f77b4", # blue
    "#ff7f0e", # orange
    "#2ca02c", # green
    "#d62728", # red
    "#9467bd", # purple
    "#a5a5a5" # grey
]

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")
abs_df = read_csv(data_dir + "abstracts.csv")
yr_df_sample = read_csv(data_dir + "year-sample.csv")

# by segment
abs_df = read_csv(data_dir + "abstracts.csv")
seg_df_sample = abs_df.merge(
    yr_df_sample[["article_url", "year_range", "url"]],
    on=["article_url", "year_range", "url"],
    how="inner",
)
seg_grouped = (
    seg_df_sample.groupby(["segment", "Legend"]).size().unstack()
).reset_index()
seg_grouped["segment"] = seg_grouped["segment"].astype(str)

# Print the value counts of the "Legend" column
print(seg_grouped)

tick_labels = seg_grouped["segment"].astype(str)
seg_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.xlabel("Segment")
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.show()

# by journal
jr_grouped = (
    yr_df_sample.groupby(["journal", "Legend"]).size().unstack()
).reset_index()
tick_labels = jr_grouped["journal"].astype(str)
jr_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

print(jr_grouped)