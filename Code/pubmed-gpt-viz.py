import matplotlib.pyplot as plt
from pandas import read_csv, cut
from os import getcwd
# from numpy import zeros

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
viz_dir = dir.replace("Code", "Graphs\\")

# word count distribution
abs_df = read_csv(data_dir + "abstracts.csv")
abs_1_df = abs_df[abs_df["segment"] == 1]

abs_1_df["word_count"].plot(kind="hist", bins=100, figsize=(20, 10))
plt.xlabel("Word Count", fontsize=24)
plt.ylabel("Number of Abstracts", fontsize=24)
plt.title("Distribution of Abstract Word Counts", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
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
    "Over 50% chance of being real": "Greater than 50% chance of real",
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
    "Greater than 50% chance of real",
]
yr_grouped = yr_grouped.reindex(columns=new_order)
tick_labels = yr_grouped.index.astype(str)
yr_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.legend(fontsize=22)
plt.xlabel("Year Range", fontsize=24)
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts", fontsize=24)
plt.title("Real published extracts evaluated by AI generated text detector", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

fig = plt.gcf()
fig.set_size_inches(20, 10)
fig.subplots_adjust(left=0.07, right=0.93, top=0.91, bottom=0.09)

rect = plt.Rectangle((0, 0), 1, 1, fill=False, linewidth=5, edgecolor="black", zorder=10)
fig.patch.set_edgecolor("black")
fig.patch.set_linewidth(2)
plt.savefig(viz_dir + "Years.png")

int_df = read_csv(data_dir + "number-of-internet-users.csv")
int_df = int_df.drop(["Entity", "Code"], axis=1)
int_df['year_range'] = cut(int_df['Year'], bins=range(1990, 2024, 5),
                              labels=[f"{i}-{i+4}" for i in range(1990, 2019, 5)])
int_df = int_df.groupby('year_range')['Number of Internet users'].sum().reset_index()

# create stacked bar chart
yr_grouped_ai = yr_grouped.drop("Greater than 50% chance of real", axis=1)
ax1 = yr_grouped_ai.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

# create line chart on top of stacked bar chart
ax2 = ax1.twinx()
ax2.plot(int_df['year_range'], int_df['Number of Internet users'], color='black', linewidth=3)
ax2.set_ylabel('Number of Internet Users')

# add labels, title, and legend
ax1.set_xlabel('Year Range')
ax1.set_ylabel('Number of Abstracts')
ax1.set_title('Falsely attributed abstracts attributed by Year Range')
ax1.legend(loc='upper left')
ax2.legend(['Number of Internet Users'], loc='upper right')

# adjust chart properties
ax1.tick_params(axis='both', labelsize=18)
ax2.tick_params(axis='both', labelsize=18)
ax1.set_xticklabels(int_df['year_range'], rotation=0)
ax1.set_ylim([0, 600])
ax2.set_ylim([0, 2500])
ax1.grid(axis='y')
ax2.grid(axis='y')

# save chart
plt.savefig(data_dir + "Years with Internet.png")

# by journal
jr_grouped = yr_df_sample.groupby(["journal", "Legend"]).size().unstack()

new_order = [
    "Greater than 90% chance of being AI generated",
    "Greater than 80% chance of being AI generated",
    "Greater than 70% chance of being AI generated",
    "Greater than 60% chance of being AI generated",
    "Greater than 50% chance of being AI generated",
    "Greater than 50% chance of real",
]

jr_grouped = jr_grouped.reindex(columns=new_order)
tick_labels = jr_grouped.index.astype(str)
jr_grouped.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.legend(fontsize=22)
plt.xlabel("Journal", fontsize=24)
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts", fontsize=24)
plt.title("Real published extracts evaluated by AI generated text detector", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

fig = plt.gcf()
fig.set_size_inches(20, 10)
fig.subplots_adjust(left=0.07, right=0.93, top=0.91, bottom=0.09)

rect = plt.Rectangle((0, 0), 1, 1, fill=False, linewidth=5, edgecolor="black", zorder=10)
fig.patch.set_edgecolor("black")
fig.patch.set_linewidth(2)
plt.savefig(viz_dir + "Journals.png")

# by segment
seg_df_sample = abs_df.merge(
    yr_df_sample[["article_url", "year_range", "url"]],
    on=["article_url", "year_range", "url"],
    how="inner",
)

seg_rep = {
    0.25: "25%",
    0.5: "50%",
    1: "100%"
}
seg_df_sample["segment"] = seg_df_sample["segment"].replace(seg_rep)

seg_grouped = (
    seg_df_sample.groupby(["segment", "Legend"]).size().unstack()
).reset_index()

seg_grouped["order"] = seg_grouped["segment"].apply(lambda x: {"100%": 2, "50%": 1, "25%": 0}[x])
seg_grouped_sorted = seg_grouped.sort_values("order")
seg_grouped_sorted = seg_grouped_sorted.drop("order", axis=1)


tick_labels = seg_grouped_sorted["segment"].astype(str)
seg_grouped_sorted.plot(kind="bar", stacked=True, color=colors, figsize=(20, 10))

plt.legend(fontsize=22)
plt.xlabel("Percentage of abstract words", fontsize=24)
plt.xticks(range(len(tick_labels)), tick_labels, rotation=0)
plt.ylabel("Number of Abstracts", fontsize=24)
plt.title("Real published extracts evaluated by AI generated text detector", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

fig = plt.gcf()
fig.set_size_inches(20, 10)
fig.subplots_adjust(left=0.08, right=0.92, top=0.91, bottom=0.09)

rect = plt.Rectangle((0, 0), 1, 1, fill=False, linewidth=5, edgecolor="black", zorder=10)
fig.patch.set_edgecolor("black")
fig.patch.set_linewidth(2)
plt.savefig(viz_dir + "Segments.png")