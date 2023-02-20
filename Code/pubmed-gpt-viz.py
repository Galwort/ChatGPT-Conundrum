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

# repeating the above but making it 3D
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111, projection="3d")
for i, (name, group) in enumerate(yr_df_sample.groupby("Legend")):
    xs = group["year_range"]
    ys = group["Legend"]
    zs = 1
    ax.bar(xs, zs, zs=ys, zdir="y", color=colors[i], alpha=0.8)

ax.set_xlabel("Year Range")
ax.set_ylabel("Legend")
ax.set_zlabel("Number of Abstracts")
ax.set_title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Years-3D.png")

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