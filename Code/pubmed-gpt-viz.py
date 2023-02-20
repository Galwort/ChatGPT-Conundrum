import matplotlib.pyplot as plt
from pandas import read_csv
from numpy import arange, meshgrid, zeros_like
from os import getcwd
from mpl_toolkits.mplot3d import Axes3D

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
viz_dir = dir.replace("Code", "Graphs\\")
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#a5a5a5']

# by year
yr_df_sample = read_csv(data_dir + "year-sample.csv")
yr_groups = yr_df_sample.groupby(["year_range", "Legend"]).size().unstack()

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

xpos = arange(len(yr_groups.index))
ypos = arange(len(yr_groups.columns))
xpos, ypos = meshgrid(xpos, ypos)

zpos = zeros_like(xpos)
dz = yr_groups.values

for i, col in enumerate(yr_groups.columns):
    ax.bar3d(xpos.ravel(), ypos.ravel(), zpos.ravel(), 0.5, 0.5, dz.ravel(), color=colors[i])

ax.set_xlabel("Year Range")
ax.set_xticks(arange(len(yr_groups.index)))
ax.set_xticklabels(yr_groups.index)
ax.set_ylabel("Legend")
ax.set_yticks(arange(len(yr_groups.columns)))
ax.set_yticklabels(yr_groups.columns)
ax.set_zlabel("Number of Abstracts")
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