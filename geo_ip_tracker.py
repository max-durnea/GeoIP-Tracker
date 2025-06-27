import requests
import csv
import folium

API_url = "http://ip-api.com/json/"
input_file="ips.txt"
output_file="ip_info.csv"
fields=["status","country","countryCode", "region", "regionName", "city", "zip", "lat", "lon", "timezone", "isp", "org", "as", "query"]

def get_info(ip):
    response = requests.get(API_url+ip)
    if(response.status_code==200):
        return response.json()
    else:
        return -1


    
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
        coordinates[ip]={info["org"],float(info["lat"]), float(info["lon"])}
    writer.writerows(json_data)
    '''for coord in coordinates:
        print(coord+": "+str(coordinates[coord]))'''
    #Generat
    
        
        