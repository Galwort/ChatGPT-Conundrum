import matplotlib.pyplot as plt
from pandas import read_csv
from numpy import zeros
from os import getcwd
from mpl_toolkits.mplot3d import Axes3D

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
viz_dir = dir.replace("Code", "Graphs\\")
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#a5a5a5']

# by year
yr_df_sample = read_csv(data_dir + "year-sample.csv")
yr_groups = yr_df_sample.groupby(["year_range", "Legend"]).size().unstack()
x = range(len(yr_groups.index))
y = range(len(yr_groups.columns))
z = zeros((len(yr_groups.index), len(yr_groups.columns)))
dx = 0.5
dy = 0.5
dz = yr_groups.values

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

for i in range(len(x)):
    for j in range(len(y)):
        ax.bar3d(x[i], y[j], z[i, j], dx, dy, dz[i, j], color=colors[j], zsort='average')

ax.set_xlabel("Year Range")
ax.set_xticks(x)
ax.set_xticklabels(yr_groups.index)
ax.set_ylabel("Legend")
ax.set_yticks(y)
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