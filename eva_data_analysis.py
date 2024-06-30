import pandas as pd
import matplotlib.pyplot as plt



data_f = './eva-data.json'
data_t = './eva-data.csv'
g_file = './cumulative_eva_graph.png'

data = pd.read_json(data_f, convert_dates=['date'])
data['eva'] = data['eva'].astype(float)
data.dropna(axis=0, inplace=True)
data.sort_values('date', inplace=True)

data.to_csv(data_t, index=False)

data['duration_hours'] = data['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
data['cumulative_time'] = data['duration_hours'].cumsum()
plt.plot(data.date, data.cumulative_time, 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(g_file)
plt.show()
