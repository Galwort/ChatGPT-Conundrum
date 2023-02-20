import matplotlib.pyplot as plt
import matplotlib
from pandas import read_csv
import ipywidgets as widgets
from IPython.display import display

matplotlib.use('Qt5Agg')

abs_df = read_csv("abstracts.csv")
# abs_df = abs_df[abs_df["segment"] == 1]
# abs_df = abs_df[abs_df["journal"] == 'Science']
# abs_df = abs_df[abs_df["year_range"] == '2010-2019']
abs_df = abs_df.sort_values(by='score', ascending=False)
abs_df = abs_df.set_index('score', drop=False)


options = list(abs_df['journal'].unique())

def update_chart(journal):
    filtered_df = abs_df[abs_df["journal"] == journal]
    fig, ax = plt.subplots()
    ax.bar(filtered_df.index, filtered_df['score'])
    ax.set_xlabel('Abstracts')
    ax.set_ylabel('Score')
    ax.set_title(f'Pareto Chart for {journal}')
    plt.show()

# dropdown = widgets.Dropdown(options=options, description='Journal:')
# dropdown.observe(lambda event: update_chart(event.new), names='value')

# display(dropdown)
# update_chart(options[0])

widgets.interact(update_chart, journal=options)

# plt.bar(abs_df.index, abs_df['score'])
# plt.xlabel('Abstracts')
# plt.ylabel('Score')
# plt.title('Pareto Chart')
# plt.show()