import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px



intercambios_arg = pd.read_csv('intercambios_arg.csv', delimiter= ';',decimal=',')
print(intercambios_arg.head())
intercambios_arg['anio'] = intercambios_arg['anio'].astype(int)
intercambios_arg['mes'] = intercambios_arg['mes'].astype(int)

# Combine 'anio' and 'mes' into a string, then convert to datetime
intercambios_arg['date'] = pd.to_datetime(intercambios_arg['anio'].astype(str) + '-' + intercambios_arg['mes'].astype(str) + '-01')

data = intercambios_arg.groupby(['tipo','destino','date'])['energia'].sum().reset_index()
print(data)

unique_combinations = data[['tipo', 'destino']].drop_duplicates()

# Iterate over each combination and create a plot
for index, row in unique_combinations.iterrows():
    destino = row['destino']
    tipo = row['tipo']

    # Filter the DataFrame for this combination
    df_plot = data[(data['destino'] == destino) & (data['tipo'] == tipo)]

    # Create a plot with Plotly
    fig = px.line(df_plot, x='date', y='energia', title=f'{destino} - {tipo}',
                  labels={'date': 'Date', 'energia': 'Energia'})

    # Save the plot as an HTML file
    fig.write_html(f'{destino}_{tipo}.html')