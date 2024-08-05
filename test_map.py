import folium
import plotly.express as px
from folium import IFrame
from folium.features import CustomIcon
import pandas as pd
from folium import Popup
import random
from datetime import datetime, timedelta


# Create a map centered around Latin America
m = folium.Map(location=[-25, -60], zoom_start=5)

# Sample data for specific locations in Latin America
locations = [
    {'location': 'Expo ARG-BOL', 'coords': (-24, -65),'tipo':'Expo'},
    {'location': 'Impo ARG-BOL', 'coords': (-24, -66),'tipo':'Impo'},
    {'location': 'Expo BOL-ARG', 'coords': (-20, -66),'tipo':'Expo'},
    {'location': 'Impo BOL-ARG', 'coords': (-20, -65),'tipo':'Impo'},
    {'location': 'Expo ARG-BRL', 'coords': (-26, -54),'tipo':'Expo'},
    {'location': 'Impo ARG-BRL', 'coords': (-26, -54.5),'tipo':'Impo'},
    {'location': 'Expo BRL-ARG', 'coords': (-23, -54),'tipo':'Expo'},
    {'location': 'Impo BRL-ARG', 'coords': (-23, -53),'tipo':'Impo'},
    {'location': 'Expo ARG-PY', 'coords': (-27.5, -56),'tipo':'Expo'},
    {'location': 'Impo ARG-PY', 'coords': (-26.4, -56),'tipo':'Impo'},
    {'location': 'Expo PY-ARG', 'coords': (-26.4, -56.5),'tipo':'Expo'},
    {'location': 'Impo PY-ARG', 'coords': (-27.5, -56.5),'tipo':'Impo'},
    {'location': 'Expo ARG-UY', 'coords': (-31.5, -59.5),'tipo':'Expo'},
    {'location': 'Impo ARG-UY', 'coords': (-32.5, -59.5),'tipo':'Impo'},
    {'location': 'Expo UY-ARG', 'coords': (-32.5, -56.5),'tipo':'Expo'},
    {'location': 'Impo UY-ARG', 'coords': (-31.5, -56.5),'tipo':'Impo'},
    {'location': 'Generación Eléctrica Argentina', 'coords': (-31, -64),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Chile', 'coords': (-33.4, -70.4),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Uruguay', 'coords': (-34.9, -56.1),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Brasil', 'coords': (-15.8, -47.9),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Bolivia', 'coords': (-17.8, -63.2),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Ecuador', 'coords': (-1.6, -78.7),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Colombia', 'coords': (4.8, -73.6),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Peru', 'coords': (-11.5, -74.8),'tipo':'Elec'},
    {'location': 'Generación Eléctrica Paraguay', 'coords': (-24.0, -57.5),'tipo':'Elec'},
]

exchanges = [
    {'from': 'Expo ARG-BOL', 'to': 'Impo BOL-ARG', 'value': 0.0, 'from_coords': locations['location'=='Expo ARG-BOL']['coords'], 'to_coords':(-20,-65)},
    {'from': 'Expo BOL-ARG', 'to': 'Impo ARG-BOL', 'value': 30.8, 'from_coords': (-20,-66), 'to_coords':(-24,-66)},
    {'from': 'Expo PY-ARG', 'to': 'Impo ARG-PY', 'value': 7, 'from_coords': (-26.4,-56.5), 'to_coords':(-27.5,-56.5)},
    {'from': 'Expo BRL-ARG', 'to': 'Impo ARG-BRL', 'value': 384, 'from_coords': (-23,-54), 'to_coords':(-26,-54.5)},
    {'from': 'Expo UY-ARG', 'to': 'Impo ARG-UY', 'value': 202.4, 'from_coords': (-32.5,-56.5), 'to_coords':(-32.5,-59.5)},
]

def generate_monthly_table():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    current_date = start_date

    columns = ['Térmica', 'Eólica', 'Nuclear', 'Hidráulica']
    table_html = '<table border="1" style="border-collapse: collapse; width: 100%;">'
    table_html += '<caption>Tabla Inventada</caption>'
    table_html += '<tr><th>Month</th>'
    
    for col in columns:
        table_html += f'<th>{col}</th>'
    table_html += '</tr>'
    
    while current_date <= end_date:
        table_html += '<tr>'
        table_html += f'<td>{current_date.strftime("%Y-%m")}</td>'
        for _ in columns:
            table_html += f'<td>{random.randint(1, 100)}</td>'
        table_html += '</tr>'
        current_date += timedelta(days=30)  # Move to the next month

    table_html += '</table>'
    return table_html


# Function to create a Plotly plot and return it as an HTML string
def create_plot(info):
    fig = px.bar(x=['A', 'B', 'C'], y=info)
    return fig.to_html(full_html=False)

# Add clickable markers to the map
for location in locations:
    print(location['tipo'])
    popup_html = generate_monthly_table()
    iframe = IFrame(popup_html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)

    if location['tipo'] == 'Expo':
        color_marker = 'green'
        icon_marker = 'arrow-up'
    elif location['tipo'] == 'Impo':
        color_marker = 'red'
        icon_marker = 'arrow-down'
    else:
        color_marker = 'blue'
        icon_marker = 'glyphicon glyphicon-flash'

    folium.Marker(
        location=location['coords'],
        popup=popup,
        icon = folium.Icon(icon=icon_marker,color = color_marker),
        tooltip=location['location']
    ).add_to(m)

# Function to add a curved arrow to the map
def add_curved_arrow(m, start, end, color='blue', weight=1, opacity=1, tooltip=None):

    # Create the curve
    line = folium.PolyLine(
        locations=[start, end],
        color=color,
        weight=weight,
        opacity=opacity,
        tooltip=tooltip
    )
    line.add_to(m)
    
    # Add an arrow head
    arrow_head = folium.Marker(
        location=end,
        icon=None
    )
    arrow_head.add_to(m)

# Add curved arrows for exchanges
for exchange in exchanges:
    tooltip_text = f"{exchange['from']} to {exchange['to']}: {exchange['value']}"
    add_curved_arrow(
        m, 
        start=exchange['from_coords'], 
        end=exchange['to_coords'], 
        weight = exchange['value']/50,
        tooltip=tooltip_text
    )

# Save the map to an HTML file
m.save('interactive_map_exchanges.html')


