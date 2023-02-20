import matplotlib.pyplot as plt
from pandas import read_csv
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Code", "Data\\")
viz_dir = dir.replace("Code", "Graphs\\")
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#a5a5a5']

# by year
yr_df_sample = read_csv("year-sample.csv")
yr_df_sample.groupby(["year_range", "Legend"]).size().unstack().plot(
    kind="bar", stacked=True, color=colors, figsize=(20, 10)
)

plt.xlabel("Year Range")
plt.xticks(rotation=0)
plt.ylabel("Number of Abstracts")
plt.title("Real published extracts evaluated by AI generated text detector")
plt.savefig(viz_dir + "Years.png")

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