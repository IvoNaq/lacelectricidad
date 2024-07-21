import folium
import plotly.express as px
from folium import IFrame
from folium.features import CustomIcon

# Sample data for specific locations in Latin America
locations = [
    {'location': 'De BOL - a ARG', 'coords': (-23.816, -65.417)},
    {'location': 'De ARG - a BOL', 'coords': (-23.8, -65.4)},
    {'location': 'Sucre', 'coords': (-19.0333, -65.2627)},
    {'location': 'Umuarama', 'coords': (-23.765, -53.3204)},
    {'location': 'Posadas', 'coords': (-27.3626, -55.8976)},
    {'location': 'Salto', 'coords': (-31.3833, -57.9667)},
    {'location': 'Parana', 'coords': (-31.73197, -60.5238)},
]

exchanges = [
    {'from': 'Jujuy', 'to': 'Sucre', 'value': 0.7, 'from_coords': (-23.816, -65.417), 'to_coords': (-19.0333, -65.2627)},
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
