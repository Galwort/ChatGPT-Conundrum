import matplotlib.pyplot as plt
from pandas import read_csv
from os import getcwd
from numpy import zeros

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
viz_dir = dir.replace("Code", "Graphs\\")

abs_df = read_csv(data_dir + "abstracts.csv")
abs_1_df = abs_df[abs_df["segment"] == 1]

abs_1_df["word_count"].plot(kind="hist", bins=100, figsize=(20, 10))
plt.xlabel("Word Count")
plt.ylabel("Number of Abstracts")
plt.title("Distribution of Abstract Word Counts")
plt.savefig(viz_dir + "word-count-distribution.png")

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
yr_grouped = a.reindex(columns=new_order)

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
jr_grouped = yr_df_sample.groupby(["journal", "Legend"]).size().unstack()

new_order = [
    "Greater than 90% chance of being AI generated",
    "Greater than 80% chance of being AI generated",
    "Greater than 70% chance of being AI generated",
    "Greater than 60% chance of being AI generated",
    "Greater than 50% chance of being AI generated",
    "Less than 50% chance of being AI generated",
]

yr_grouped = yr_grouped.reindex(columns=new_order)
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
seg_df_sample = abs_df.merge(
    yr_df_sample[["article_url", "year_range", "url"]],
    on=["article_url", "year_range", "url"],
    how="inner",
)
seg_grouped = (
    seg_df_sample.groupby(["segment", "Legend"]).size().unstack()
).reset_index()
seg_grouped["segment"] = seg_grouped["segment"].astype(str)
tick_labels = seg_grouped["segment"].astype(str)
seg_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.xlabel("Segment")
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Segments.png")

# by segment, 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.set_xlabel("Segment")
ax.set_xticklabels(seg_grouped["segment"])
ax.set_zlabel("Abstracts")
ax.set_ylim3d(0,10)

dz = zeros(seg_grouped.shape[0])
for i in range(seg_grouped.shape[1]-1):
    ax.bar3d(
        seg_grouped.index, # starting point for x
        1, # starting point for y
        dz, # starting point for z
        0.5, # width of bar
        0.5, # depth of bar
        seg_grouped.iloc[:, i+1], # height of bar
        color=colors[i]
    )
    dz += seg_grouped.iloc[:, i+1]

plt.savefig(viz_dir + "Segments-3D.png")