import folium
#you can choose your own tilesets from https://leaflet-extras.github.io/leaflet-providers/preview/
m = folium.Map(tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',attr='hello')
folium.Marker(location=[45.3288, -121],
              tooltip="8.8.8.8",
              popup="GOOGLE DNS SERVER",
              icon=folium.Icon(icon="cloud")).add_to(m)
m.save("map.html")