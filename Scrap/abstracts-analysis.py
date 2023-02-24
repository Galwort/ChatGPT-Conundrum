import matplotlib.pyplot as plt
from pandas import read_csv
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")

abs_df = read_csv(data_dir + "abstracts.csv")
abs_df = abs_df[abs_df["segment"] == 1]

abs_df["word_count"].plot(kind="hist", bins=100, figsize=(20, 10))
plt.xlabel("Word Count")
plt.ylabel("Number of Abstracts")
plt.title("Distribution of Abstract Word Counts")
plt.save("word-count-distribution.png")