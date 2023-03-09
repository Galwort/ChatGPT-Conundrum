import matplotlib.pyplot as plt
from pandas import read_csv, cut
from os import getcwd

dir = getcwd()
data_dir = dir.replace("Scrap", "Data\\")
int_df = read_csv(data_dir + "number-of-internet-users.csv")
print(int_df.head())
# drop columns
int_df = int_df.drop(["Entity", "Code"], axis=1)
int_df['year_range'] = cut(int_df['Year'], bins=range(1990, 2024, 5),
                              labels=[f"{i}-{i+4}" for i in range(1990, 2019, 5)])
int_df = int_df.groupby('year_range')['Number of Internet users'].sum().reset_index()