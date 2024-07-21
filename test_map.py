import folium
import plotly.express as px
from folium import IFrame
from folium.features import CustomIcon

# Sample data for specific locations in Latin America
locations = [
    {'location': 'Expo ARG-BOL', 'coords': (-24, -65)},
    {'location': 'Impo ARG-BOL', 'coords': (-23, -66)},
    {'location': 'Expo BOL-ARG', 'coords': (-18, -64)},
    {'location': 'Impo BOL-ARG', 'coords': (-19, -65)},
    {'location': 'Expo ARG-BRL', 'coords': (-24, -54)},
    {'location': 'Impo ARG-BRL', 'coords': (-23, -53)},
    {'location': 'Posadas', 'coords': (-27.3626, -55.8976)},
    {'location': 'Salto', 'coords': (-31.3833, -57.9667)},
    {'location': 'Parana', 'coords': (-31.73197, -60.5238)},
]

exchanges = [
    {'from': 'Expo ARG-BOL', 'to': 'Impo BOL-ARG', 'value': 0.7, 'from_coords': (-24, -65), 'to_coords': (-19, -65)},
    {'from': 'Umuarama', 'to': 'Posadas', 'value': 384, 'from_coords': (-23.765, -53.3204), 'to_coords': (-27.3626, -55.8976)},
    {'from': 'Salto', 'to': 'Parana', 'value': 203, 'from_coords': (-31.3833, -57.9667), 'to_coords': (-31.73197, -60.5238)},
]

# Create a map centered around Latin America
m = folium.Map(location=[-25, -60], zoom_start=5)

# Function to create a Plotly plot and return it as an HTML string
def create_plot(info):
    fig = px.bar(x=['A', 'B', 'C'], y=info)
    return fig.to_html(full_html=False)

# Add clickable markers to the map
for location in locations:
    plot_html = create_plot([100, 200, 300])  # Placeholder data for the plot
    iframe = IFrame(html=plot_html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)
    folium.Marker(
        location=location['coords'],
        popup=popup,
        icon = folium.Icon(icon='arrow-up',color='red'),
        tooltip=location['location']
    ).add_to(m)

# Function to add a curved arrow to the map
def add_curved_arrow(m, start, end, color='blue', weight=2.5, opacity=1, tooltip=None):
    # Calculate the mid-point for the curve
    mid_lat = (start[0] + end[0]) / 2
    mid_lon = (start[1] + end[1]) / 2
    mid_point = [mid_lat, mid_lon]
    
    # Adjust the mid-point to create a curve (simple approach)
    mid_point[0] += 2  # Adjust latitude to curve the line
    
    # Create the curve
    line = folium.PolyLine(
        locations=[start, mid_point, end],
        color=color,
        weight=weight,
        opacity=opacity,
        tooltip=tooltip
    )
    line.add_to(m)
    
    # Add an arrow head
    arrow_head = folium.Marker(
        location=end,
        #icon=CustomIcon(icon_image='https://upload.wikimedia.org/wikipedia/commons/5/5f/Arrow_down.svg', icon_size=(20, 20))
    )
    arrow_head.add_to(m)

# Add curved arrows for exchanges
for exchange in exchanges:
    tooltip_text = f"{exchange['from']} to {exchange['to']}: {exchange['value']}"
    add_curved_arrow(
        m, 
        start=exchange['from_coords'], 
        end=exchange['to_coords'], 
        tooltip=tooltip_text
    )

# Save the map to an HTML file
m.save('interactive_map_exchanges.html')

# Display the map in a Jupyter Notebook (if using one)
m
