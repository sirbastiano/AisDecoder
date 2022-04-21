#aisdecoder env
import pandas as pd
import geopandas as gpd
from decoder import NMEA_decoder
from datetime import date
from shapely.geometry import Point, Polygon
import folium 
import numpy as np
from mapper import *
import os
from utils import findInterval

today = date.today().strftime("%Y-%m-%d")

style = 'symbol:pin; fill:#0000ff; fill-opacity:0.7; stroke:#ffffff; stroke-opacity:1.0; stroke-width:0.5'
text = None
dateTime = None

# SETTINGS
output_path = 'SRC\\Output\\'
decoded_path = '240322'
file_path = "SRC\\Input\\Vesperino_24032022.txt"


timestring0='15:57:39'
timestring1='15:57:39'
t0, t1 = findInterval(timestring0=timestring0, timestring1=timestring1)
filterInterval = [t0, t1] # Start, Stop


def main():
     ais_msg = NMEA_decoder(file_path)
     GPS = ais_msg.get_GPS()
     ais = ais_msg.to_df()
     ais.to_excel('SRC\\Output\\180322\\Ais_decoded.xlsx')
     # GPS.to_excel('SRC\\Output\\131021\\GPS_decoded.xlsx')
     ais.dropna(axis=0,subset=['lon','lat'], inplace=True)
     ais.reset_index(inplace=True, drop=True)

     # FILTER TO WINDOW:
     ais = ais[ (ais['timestamp']>filterInterval[0]) & (ais['timestamp']<filterInterval[1])]
     # ais = ais.drop_duplicates(subset='mmsi')
     ais.dropna(axis=0,subset=['lon','lat'], inplace=True)
     ais.reset_index(inplace=True, drop=True)


     SHP = gpd.GeoDataFrame(columns = ['style_css', 'label', 'text', 'dateTime', 'geometry'])

     for i in range(len(ais)):
          label = ais['mmsi'][i]
          # lat, lon = ais['latitude'][i], ais['longitude'][i]
          lat, lon = float(ais['lat'][i]), float(ais['lon'][i])
          coordinates = [(lon, lat)]
          geometry = Point(coordinates)
          new_row = {'style_css':style, 'label':label, 'text':text, 'dateTime':dateTime, 'geometry':geometry}
          SHP = SHP.append(new_row, ignore_index=True)
     
     SHP.to_file(output_path+decoded_path+'\\'+'navi.shp')


if __name__ == "__main__":
     main()
     os.system('cls')
     print('Execution termined successfully!')