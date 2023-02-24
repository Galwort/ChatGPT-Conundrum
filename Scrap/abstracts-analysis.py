import matplotlib.pyplot as plt
from pandas import read_csv
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")
abs_df = read_csv(data_dir + "abstracts.csv")
abs_1_df = abs_df[abs_df["segment"] == 1]
print(len(abs_1_df))
