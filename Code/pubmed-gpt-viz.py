import matplotlib.pyplot as plt
from pandas import read_csv
from os import getcwd
from mpl_toolkits.mplot3d import Axes3D

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
viz_dir = dir.replace("Code", "Graphs\\")
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#a5a5a5']

# by year
yr_df_sample = read_csv(data_dir + "year-sample.csv")
yr_df_sample.groupby(["year_range", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10)
)

plt.xlabel("Year Range")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Years.png")

# by year, 3d
yr_df_sample = read_csv(data_dir + "year-sample.csv")
groups = yr_df_sample.groupby(["year_range", "Legend"]).size().unstack()

fig, ax = plt.subplots(figsize=(15, 10))

bottom = None
for i, col in enumerate(groups.columns):
    ax.bar(groups.index, groups[col], bottom=bottom, color=colors[i], width=0.5, zorder=3-i)
    bottom = groups[col] if bottom is None else bottom + groups[col]

ax.set_xlabel("Year Range")
ax.set_xticks(groups.index)
ax.set_ylabel("Number of Abstracts")
ax.set_title("Real published extracts evaluated by AI generated text detector")

plt.savefig(viz_dir + "3D_Stacked_Bar.png")

# by journal
jr_df_sample = read_csv(data_dir + "journal-sample.csv")
jr_df_sample.groupby(["journal", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10) 
)

plt.xlabel("Journal")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Journals.png")

# by segment 
abs_df = read_csv(data_dir + "abstracts.csv")
abs_df.groupby(["segment", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10)
)

plt.xlabel("Segment")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Segments.png")