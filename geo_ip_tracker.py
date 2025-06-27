import requests
import csv
import folium
import sys
import os
API_url = "http://ip-api.com/json/"
input_file="ips.txt"
output_file="ip_info.csv"
fields=["status","country","countryCode", "region", "regionName", "city", "zip", "lat", "lon", "timezone", "isp", "org", "as", "query"]
m = folium.Map((0.0,0.0),tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',attr='Dark Map')

def get_info(ip):
    response = requests.get(API_url+ip)
    if(response.status_code==200):
        return response.json()
    else:
        return -1



def main(input_file,user_id):
    base_dir="downloads"   
    user_dir=os.path.join(base_dir,user_id)
    os.makedirs(user_dir, exist_ok=True)
    output_file = os.path.join(user_dir, 'ip_info.csv')

    with open(input_file,'r') as f, open(output_file,'w',newline='') as csvfile:
        failed_checks=[]
        writer=csv.DictWriter(csvfile,fieldnames=fields)
        writer.writeheader()
        json_data=[]
        coordinates={} #store it in the form: [ip,lat,lon]
        while(True):
            ip=f.readline().strip()
            if(ip==''):
                break
            info = get_info(ip)
            if(info == -1):
                failed_checks.append(ip)
                continue
            if(info["status"]=="fail"):
                failed_checks.append(ip)
                continue
            json_data.append(info)
            coordinates[ip]=[info["org"],[float(info["lat"]), float(info["lon"])]]
        writer.writerows(json_data)
        '''for coord in coordinates:
            print(coord+": "+str(coordinates[coord]))'''
        #Generate the html page with marked cities
        for coord in coordinates:
            folium.Marker(location=coordinates[coord][1],
                        tooltip=coord,
                        popup=coordinates[coord][0],
                        icon=folium.Icon(icon="cloud")).add_to(m)
        m.save(f"{user_dir}/map.html")
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python geo_ip_tracker.py <input_file> <user_id>")
        sys.exit(1)

    input_file = sys.argv[1]
    user_id = sys.argv[2]
    main(input_file,user_id)  
        
        