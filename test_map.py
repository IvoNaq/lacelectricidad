import folium
import plotly.express as px
from folium import IFrame
from folium.features import CustomIcon
import pandas as pd
from folium import Popup
from folium import FeatureGroup
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a map centered around Latin America
m = folium.Map(location=[-25, -60], zoom_start=3)

# Sample data for specific locations in Latin America
locations = [
    {'location': 'Expo ARG-BOL', 'coords': (-24, -65),'tipo':'Expo', 'origen': 'Argentina','destino':'Bolivia'},
    {'location': 'Impo ARG-BOL', 'coords': (-24, -66),'tipo':'Impo', 'origen': 'Bolivia','destino':'Argentina'},
    {'location': 'Expo BOL-ARG', 'coords': (-20, -66),'tipo':'Expo', 'origen': 'Bolivia','destino':'Argentina'},
    {'location': 'Impo BOL-ARG', 'coords': (-20, -65),'tipo':'Impo', 'origen': 'Argentina','destino':'Bolivia'},
    {'location': 'Expo ARG-BRL', 'coords': (-26, -54),'tipo':'Expo','origen': 'Argentina','destino':'Brasil'},
    {'location': 'Impo ARG-BRL', 'coords': (-26, -54.5),'tipo':'Impo','origen': 'Brasil','destino':'Argentina'},
    {'location': 'Expo BRL-ARG', 'coords': (-23, -54),'tipo':'Expo','origen': 'Brasil','destino':'Argentina'},
    {'location': 'Impo BRL-ARG', 'coords': (-23, -53),'tipo':'Impo','origen': 'Argentina','destino':'Brasil'},
    {'location': 'Expo ARG-PY', 'coords': (-27.9, -56),'tipo':'Expo','origen': 'Argentina','destino':'Paraguay'},
    {'location': 'Impo ARG-PY', 'coords': (-27.9, -56.5),'tipo':'Impo','origen': 'Paraguay','destino':'Argentina'},
    {'location': 'Expo PY-ARG', 'coords': (-26.4, -56.5),'tipo':'Expo','origen': 'Paraguay','destino':'Argentina'},
    {'location': 'Impo PY-ARG', 'coords': (-26.4, -56),'tipo':'Impo','origen': 'Argentina','destino':'Paraguay'},
    {'location': 'Expo ARG-UY', 'coords': (-31.5, -59.5),'tipo':'Expo','origen': 'Argentina','destino':'Uruguay'},
    {'location': 'Impo ARG-UY', 'coords': (-32.5, -59.5),'tipo':'Impo','origen': 'Uruguay','destino':'Argentina'},
    {'location': 'Expo UY-ARG', 'coords': (-32.5, -56.5),'tipo':'Expo','origen': 'Uruguay','destino':'Argentina'},
    {'location': 'Impo UY-ARG', 'coords': (-31.5, -56.5),'tipo':'Impo','origen': 'Argentina','destino':'Uruguay'},
    {'location': 'Generación Eléctrica Argentina', 'coords': (-31, -64),'tipo':'Elec','origen':'Argentina'},
    {'location': 'Generación Eléctrica Chile', 'coords': (-33.4, -70.4),'tipo':'Elec','origen':'Chile'},
    {'location': 'Generación Eléctrica Uruguay', 'coords': (-34.9, -56.1),'tipo':'Elec','origen':'Uruguay'},
    {'location': 'Generación Eléctrica Brasil', 'coords': (-15.8, -47.9),'tipo':'Elec','origen':'Brasil'},
    {'location': 'Generación Eléctrica Bolivia', 'coords': (-17.8, -63.2),'tipo':'Elec','origen':'Bolivia'},
    {'location': 'Generación Eléctrica Ecuador', 'coords': (-1.6, -78.7),'tipo':'Elec','origen':'Ecuador'},
    {'location': 'Generación Eléctrica Colombia', 'coords': (4.8, -73.6),'tipo':'Elec','origen':'Colombia'},
    {'location': 'Generación Eléctrica Peru', 'coords': (-11.5, -74.8),'tipo':'Elec','origen':'Peru'},
    {'location': 'Generación Eléctrica Paraguay', 'coords': (-24.0, -57.5),'tipo':'Elec','origen':'Paraguay'},
]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Diccionarios para almacenar htmls a ser mostrados en los popup de Folium
# Placeholder

# Create a Plotly placeholder
fig = go.Figure()
fig.add_annotation(
    text="Work In Progress",
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=24)
)

# Update layout to center the text
fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    template="simple_white"
)

# Save Plotly figure as HTML string
placeholder = fig.to_html(include_plotlyjs='cdn', full_html=False)


dict_gen_graph = {'Argentina': placeholder,
                  'Bolivia': placeholder,
                  'Brasil': placeholder,
                  'Uruguay': placeholder,
                  'Chile': placeholder,
                  'Peru': placeholder,
                  'Paraguay': placeholder,
                  'Ecuador': placeholder,
                  'Colombia':placeholder}

dict_inter_graph =[
    {'id':1,'origen': 'Argentina','destino':'Bolivia','graf':placeholder},
    {'id':2,'origen': 'Bolivia','destino':'Argentina','graf':placeholder},
    {'id':3,'origen': 'Argentina','destino':'Brasil','graf':placeholder},
    {'id':4,'origen': 'Brasil','destino':'Argentina','graf':placeholder},
    {'id':5,'origen': 'Argentina','destino':'Paraguay','graf':placeholder},
    {'id':6,'origen': 'Paraguay','destino':'Argentina','graf':placeholder},
    {'id':7,'origen': 'Argentina','destino':'Uruguay','graf':placeholder},
    {'id':8,'origen': 'Uruguay','destino':'Argentina','graf':placeholder},
]


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Auxiliary Functions
# Plot para iframe
def plot_arg_exchange(data,tipo,destino):

    # Filter the DataFrame for this combination
    df_plot = data[(data['destino'] == destino) & (data['tipo'] == tipo)]

    # Create a plot with Plotly
    fig = go.Figure(data=go.Scatter(x=df_plot['date'], y=df_plot['energia'],mode='lines'))
                    
    fig.update_layout(title=f'{destino} - {tipo}', xaxis_title = 'Date', yaxis_title = 'Energia')

    # Save the plot as an HTML file
    html_fig = fig.to_html(include_plotlyjs='cdn')

    return html_fig

# Function to add a curved arrow to the map
def add_arrow(m, start, end, start_location, end_location, color='blue', weight=4, opacity=1, tooltip=None):

    # Create the curve
    line = folium.PolyLine(
        locations=[start, end],
        color=color,
        weight=weight,
        opacity=opacity,
        tooltip=tooltip
    )
    line.add_to(intercambios)

    mid_lat = (start[0] + end[0]) / 2
    mid_lng = (start[1] + end[1]) / 2
    midpoint = [mid_lat, mid_lng]
    
    icon_marker_stats='glyphicon glyphicon-stats'
    html = next((item['graf'] for item in dict_inter_graph if item['origen'] == start_location and item['destino'] == end_location), None)
    iframe = IFrame(html=html,width = 400, height = 400)


    folium.Marker(
        location=midpoint,
        icon = folium.Icon(icon=icon_marker_stats,color = color_marker),
        popup=folium.Popup(iframe,max_width=400),
        tooltip=tooltip
    ).add_to(intercambios)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Información Argentina
# Información de intercambios - Fuente: CAMMESA - Sintesis Mensual:
intercambios_arg = pd.read_csv('intercambios_arg.csv', delimiter= ';',decimal=',')
intercambios_arg['anio'] = intercambios_arg['anio'].astype(int)
intercambios_arg['mes'] = intercambios_arg['mes'].astype(int)

# Combine 'anio' and 'mes' into a string, then convert to datetime
intercambios_arg['date'] = pd.to_datetime(intercambios_arg['anio'].astype(str) + '-' + intercambios_arg['mes'].astype(str) + '-01')

data = intercambios_arg.groupby(['tipo','destino','date'])['energia'].sum().reset_index()
unique_combinations = data[['tipo', 'destino']].drop_duplicates()
print(data)

graf_impo_bolivia = plot_arg_exchange(data=data,tipo = 'Importación',destino = 'Bolivia')
graf_expo_bolivia = plot_arg_exchange(data=data,tipo = 'Exportación',destino = 'Bolivia')
graf_expo_uruguay = plot_arg_exchange(data=data,tipo = 'Importación',destino = 'Uruguay')
graf_impo_uruguay = plot_arg_exchange(data=data,tipo = 'Exportación',destino = 'Uruguay')



for item in dict_inter_graph:
    if item['id'] == 2:
        item['graf'] = graf_impo_bolivia
    elif item['id'] == 1:
        item['graf'] = graf_expo_bolivia
    elif item['id'] == 7:
        item['graf'] = graf_expo_uruguay
    elif item['id'] == 8:
        item['graf'] = graf_impo_uruguay
        break


# Información de generación - Fuente: CAMMESA - Sintesis Mensual
generacion_arg = pd.read_csv('generacion_arg.csv', delimiter = ';')
numerical_values = ['Termica','Nuclear','Renovable con hidro', 'Renovable', 'hidro', 'total (mwh)'] 

for i in numerical_values:
    generacion_arg[i] = (generacion_arg[i].str.replace(',','').astype(int))/1000

gen_arg_chart = px.area(generacion_arg, x='date', y=['Termica', 'Renovable', 'hidro', 'Nuclear'], 
               labels={'value':'Generación (GWh)', 'date':'Mes'},
               title='Generación por tecnología')

gen_arg_chart_html = gen_arg_chart.to_html(include_plotlyjs = 'cdn')

dict_gen_graph['Argentina'] = gen_arg_chart_html

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Composing all the map elements

# Create layers
intercambios = FeatureGroup(name='Intercambios')
generacion = FeatureGroup(name='Matriz Eléctrica')

# Add clickable markers to the map
for location in locations:
   
    if location['tipo'] == 'Expo':
        color_marker = 'green'
        icon_marker = 'arrow-up'

    elif location['tipo'] == 'Impo':
        color_marker = 'red'
        icon_marker = 'arrow-down'

    else:
        color_marker = 'blue'
        icon_marker = 'glyphicon glyphicon-flash'
        html = dict_gen_graph[location['origen']]
        iframe = IFrame(html=html,width = 400, height = 400)

    try:
        
        marker = folium.Marker(
        location=location['coords'],
        popup=folium.Popup(iframe,max_width=400),
        icon = folium.Icon(icon=icon_marker,color = color_marker),
        tooltip=location['location']
    )
        
    except:

        marker = folium.Marker(
        location=location['coords'],
        icon = folium.Icon(icon=icon_marker,color = color_marker),
        tooltip=location['location']
    )


    if location['tipo'] == 'Expo':
        marker.add_to(intercambios)
    elif location['tipo'] == 'Impo':
        marker.add_to(intercambios)
    else:
        marker.add_to(generacion)

#Agrego líneas de intercambio genéricas
for location in locations:
    if location['tipo'] == 'Expo':
        start_arrow = location['coords']
        start_location = location['origen']
        end_location = location['destino']
        
        for location in locations:
            if location['tipo'] == 'Impo' and location['origen'] == start_location and location['destino'] == end_location:
                end_arrow = location['coords']
                print(end_arrow)
                add_arrow(m,start=start_arrow, end=end_arrow, start_location=start_location,end_location=end_location,tooltip=f"{start_location}->{end_location}")
    else:
        pass




intercambios.add_to(m)
generacion.add_to(m)
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('interactive_map_exchanges.html')


