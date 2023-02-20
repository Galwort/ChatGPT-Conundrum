import matplotlib.pyplot as plt
from pandas import read_csv, DataFrame, concat
from numpy import random

abs_df = read_csv("abstracts.csv")

abs_df.loc[
    (abs_df["score"] < 0.5), "Legend"
] = "Over 50% chance of being real"

abs_df.loc[
    (abs_df["score"] >= 0.5) & (abs_df["score"] < 0.6), "Legend"
] = "Less than 50% chance of being real"  

abs_df.loc[
    (abs_df["score"] >= 0.6) & (abs_df["score"] < 0.7), "Legend"
] = "Less than 40% chance of being real"  

abs_df.loc[
    (abs_df["score"] >= 0.7) & (abs_df["score"] < 0.8), "Legend"
] = "Less than 30% chance of being real"

abs_df.loc[
    (abs_df["score"] >= 0.8) & (abs_df["score"] < 0.9), "Legend"
] = "Less than 20% chance of being real"

abs_df.loc[
    (abs_df["score"] >= 0.9), "Legend"
] = "Less than 10% chance of being real"  

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#a5a5a5']

# by year
yr_df = abs_df[abs_df["segment"] == 1]
yr_df_grouped = yr_df.groupby("year_range")
yr_df_sample = DataFrame(columns=yr_df.columns)
for name, group in yr_df_grouped:
    random_rows = group.sample(1600, random_state=random.randint(0, 100000))
    yr_df_sample = concat([yr_df_sample, random_rows])

yr_df_sample.groupby(["year_range", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10)#, ax=ax
)

plt.xlabel("Year Range")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.show()

# pivot counts by year and legend
yr_df_sample.pivot_table(index="year_range", columns="Legend", aggfunc="size").to_csv("year-pivot.csv")

# by journal
jr_df = abs_df[abs_df["segment"] == 1]
jr_df_grouped = jr_df.groupby("journal")
jr_df_sample = DataFrame(columns=jr_df.columns)
for name, group in jr_df_grouped:
    random_rows = group.sample(1400, random_state=random.randint(0, 100000))
    jr_df_sample = concat([jr_df_sample, random_rows])


jr_df_sample.groupby(["journal", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10) 
)

plt.xlabel("Journal")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.show()

# pivot counts by journal and legend
jr_df_sample.pivot_table(index="journal", columns="Legend", aggfunc="size").to_csv("journal-pivot.csv")

# by segment 

abs_df.groupby(["segment", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10)
)

plt.xlabel("Segment")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.show()

# pivot counts by segment and legend
abs_df.pivot_table(index="segment", columns="Legend", aggfunc="size").to_csv("segment-pivot.csv")

# chatgpt
chatgpt_df = read_csv("chatgpt-analysis.csv")

chatgpt_df.loc[
    (chatgpt_df["score"] < 0.5), "Legend"
] = "Over 50% chance of being real"

chatgpt_df.loc[
    (chatgpt_df["score"] >= 0.5) & (chatgpt_df["score"] < 0.6), "Legend"
] = "Less than 50% chance of being real"  

chatgpt_df.loc[
    (chatgpt_df["score"] >= 0.6) & (chatgpt_df["score"] < 0.7), "Legend"
] = "Less than 40% chance of being real"  

chatgpt_df.loc[
    (chatgpt_df["score"] >= 0.7) & (chatgpt_df["score"] < 0.8), "Legend"
] = "Less than 30% chance of being real"  

chatgpt_df.loc[
    (chatgpt_df["score"] >= 0.8) & (chatgpt_df["score"] < 0.9), "Legend"
] = "Less than 20% chance of being real"  

chatgpt_df.loc[
    (chatgpt_df["score"] >= 0.9), "Legend"
] = "Less than 10% chance of being real"

chatgpt_df_grouped = chatgpt_df.groupby("journal")
chatgpt_df_sample = DataFrame(columns=chatgpt_df.columns)
for name, group in chatgpt_df_grouped:
    random_rows = group.sample(15, random_state=random.randint(0, 100000))
    chatgpt_df_sample = concat([chatgpt_df_sample, random_rows])

# fig, ax = plt.subplots()
# ax2 = ax.twinx()
# ax2.set_ylim(0, 100)
# ax2.set_yticks([0, 25, 50, 75, 100])
# ax2.set_ylabel("Percentage")

chatgpt_df_sample.groupby(["journal", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10)#, ax=ax
)

plt.xlabel("Journal")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("ChatGPT generated extracts evaluated by AI generated text detector")
plt.show()