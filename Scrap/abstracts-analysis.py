import matplotlib.pyplot as plt
from pandas import read_csv
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")

colors = [
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#a5a5a5",  # grey
]

# by year
yr_df_sample = read_csv(data_dir + "year-sample.csv")

leg_rep = {
    "Over 50% chance of being real": "Less than 50% chance of being AI generated",
    "Less than 20% chance of being real": "Greater than 80% chance of being AI generated",
    "Less than 10% chance of being real": "Greater than 90% chance of being AI generated",
    "Less than 50% chance of being real": "Greater than 50% chance of being AI generated",
    "Less than 30% chance of being real": "Greater than 70% chance of being AI generated",
    "Less than 40% chance of being real": "Greater than 60% chance of being AI generated",
}
yr_df_sample["Legend"] = yr_df_sample["Legend"].replace(leg_rep)
yr_grouped = yr_df_sample.groupby(["year_range", "Legend"]).size().unstack()

new_order = [
    "Greater than 90% chance of being AI generated",
    "Greater than 80% chance of being AI generated",
    "Greater than 70% chance of being AI generated",
    "Greater than 60% chance of being AI generated",
    "Greater than 50% chance of being AI generated",
    "Less than 50% chance of being AI generated",
]
yr_grouped = yr_grouped.reindex(columns=new_order)

tick_labels = yr_grouped.index.astype(str)
yr_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.xlabel("Year Range")
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.show()
