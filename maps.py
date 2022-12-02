import gmaps
import gmaps.datasets
gmaps.configure(api_key='AIzaSyAP8lAVlpx6dMZbMgDlegUlHcu2vGOa6vk')

marker_locations = [
(51.216671, 5.0833302),
(51.333328, 4.25)
]
 
 
fig = gmaps.figure()
markers = gmaps.marker_layer(marker_locations)
fig.add_layer(markers)


from ipywidgets.embed import embed_minimal_html
fig = gmaps.figure()
embed_minimal_html('index.html', views=[fig])