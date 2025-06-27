geoip_web_server/
├── geoip_tracker.py       # Fetches info and generates reports
├── simple_http_server.py  # Serves files over HTTP
├── ips.txt                # List of IPs to look up
├── output/
│   ├── results.csv
│   └── map.html
└── README.md

you need to have folium installed pip install folium
# To DO:
1. Implement HTTP Server
2. Make the map open at the location from where the user accessed the website