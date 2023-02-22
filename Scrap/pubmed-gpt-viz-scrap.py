import matplotlib.pyplot as plt
from pandas import read_csv
from os import getcwd
from numpy import zeros

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")
viz_dir = dir.replace("Scrap", "Graphs\\")

colors = [
    "#1f77b4", # blue
    "#ff7f0e", # orange
    "#2ca02c", # green
    "#d62728", # red
    "#9467bd", # purple
    "#a5a5a5" # grey
]

# by year
yr_df_sample = read_csv(data_dir + "year-sample.csv")
yr_grouped = (
    yr_df_sample.groupby(["year_range", "Legend"]).size().unstack()
).reset_index()
tick_labels = yr_grouped["year_range"].astype(str)
yr_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.xlabel("Year Range")
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Years.png")

# by year, 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.set_xlabel("Year Range")
ax.set_xticklabels(yr_grouped["year_range"])
ax.set_zlabel("Abstracts")
ax.set_ylim3d(0,10)

dz = zeros(yr_grouped.shape[0])
for i in range(yr_grouped.shape[1]-1):
    ax.bar3d(
        yr_grouped.index, # starting point for x
        1, # starting point for y
        dz, # starting point for z
        0.5, # width of bar
        0.5, # depth of bar
        yr_grouped.iloc[:, i+1], # height of bar
        color=colors[i]
    )
    dz += yr_grouped.iloc[:, i+1]

plt.savefig(viz_dir + "Years-3D.png")

# by journal
jr_df_sample = read_csv(data_dir + "journal-sample.csv")
jr_grouped = (
    jr_df_sample.groupby(["journal", "Legend"]).size().unstack()
).reset_index()
tick_labels = jr_grouped["journal"].astype(str)
jr_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.xlabel("Journal")
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Journals.png")

# by journal, 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.set_xlabel("Journal")
ax.set_xticklabels(jr_grouped["journal"])
ax.set_zlabel("Abstracts")
ax.set_ylim3d(0,10)

dz = zeros(jr_grouped.shape[0])
for i in range(jr_grouped.shape[1]-1):
    ax.bar3d(
        jr_grouped.index, # starting point for x
        1, # starting point for y
        dz, # starting point for z
        0.5, # width of bar
        0.5, # depth of bar
        jr_grouped.iloc[:, i+1], # height of bar
        color=colors[i]
    )
    dz += jr_grouped.iloc[:, i+1]

plt.savefig(viz_dir + "Journals-3D.png")

# by segment
abs_df = read_csv(data_dir + "abstracts.csv")
abs_grouped = (
    abs_df.groupby(["segment", "Legend"]).size().unstack()
).reset_index()
tick_labels = abs_grouped["segment"].astype(str)
abs_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.xlabel("Segment")
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Segments.png")

# by segment, 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.set_xlabel("Segment")
ax.set_xticklabels(abs_grouped["segment"])
ax.set_zlabel("Abstracts")
ax.set_ylim3d(0,10)

dz = zeros(abs_grouped.shape[0])
for i in range(abs_grouped.shape[1]-1):
    ax.bar3d(
        abs_grouped.index, # starting point for x
        1, # starting point for y
        dz, # starting point for z
        0.5, # width of bar
        0.5, # depth of bar
        abs_grouped.iloc[:, i+1], # height of bar
        color=colors[i]
    )
    dz += abs_grouped.iloc[:, i+1]

plt.savefig(viz_dir + "Segments-3D.png")