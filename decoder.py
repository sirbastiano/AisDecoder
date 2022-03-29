from numpy import append
from pyais import decode_msg
import pandas as pd
import pynmea2
import geopandas as gpd
from shapely.geometry import Point, Polygon
# import folium 

class NMEA_decoder:
    """
    Class for decoding NMEA messages from XB-6000 transponder AIS. This implementation
    has been developed in the framework of the ARGO ("A wake Revalation system for GO-fast vessels") project.
    
    All credits goes to the University of Naples Federico II, 
    Department of Industrial Engineering.

    mail: roberto.delprete@unina.it
    """
    def __init__(self, NMEA_log_path: str) -> None:
        self.file = NMEA_log_path
        self.undecoded_log = []


        with open (self.file, "r", encoding="utf-8") as myfile:
            tmp = myfile.read().splitlines()
            self.data = [line for line in tmp if line]

    # def to_map(self):    


    def show_data(self):
        return self.data                 
   

    def get_GPS(self):
        GPS_stream = [row for row in self.data if row[0]=='$']

        row_list = []
        for line in GPS_stream:
            msg = pynmea2.parse(line)
            try:
                assert(msg.is_valid)

                time = msg.timestamp.isoformat()
                lat = msg.latitude
                lon = msg.longitude

                row = {'timestamp':time, 'latitude':lat, 'longitude':lon}
                row_list.append(row)
            except (KeyError,  AttributeError, AssertionError):
                continue

        df = pd.DataFrame(row_list, columns=list(row.keys()))
        df.drop_duplicates(inplace=True)
        df.reset_index(inplace=True, drop=True)
        return df



    def decode(self, line: str, idx: int):
        """
        | Decodes the NMEA message from an input string. The function also checks for multi-line messages.
        """


        if self.data[idx][:10] == '!AIVDM,2,1':        # MULTI-LINE
            try:
                msg = decode_msg(line, self.data[idx+1])
                return msg
            except:
                pass

        # TBD Add excpetion for handling second part of the message: ADDED!
        elif self.data[idx][:10] == '!AIVDM,2,2':
            pass

        else:                                          # SINGLE-LINE
            try:
                msg = decode_msg(line)
                return msg
            except:
                self.undecoded_log.append(line)
                pass

    
    def to_df(self):
        row_list = []

        def get_clock(idx):
            for i in range(30):
                try:
                    line = self.data[idx+i]
                    msg = pynmea2.parse(line)
                    time = msg.timestamp.isoformat()
                    if isinstance(time, str):
                        return time
                except pynmea2.ParseError:
                    continue
                except AttributeError:
                    continue
            

        # main:
        for idx, line in enumerate(self.data):
            try:
                if line[0] == '!':
                    msg = self.decode(line, idx)
                    time = get_clock(idx)
                    msg['timestamp'] = time
                    row_list.append(msg)

            except:
                continue
        
        cols = ['timestamp', 'type', 'repeat', 'mmsi', 'status', 'turn', 'speed', 'accuracy',
        'lon', 'lat', 'course', 'heading', 'second', 'maneuver', 'raim', 'radio', 'ais_version', 'imo',
        'callsign', 'shipname', 'shiptype', 'to_bow', 'to_stern', 'to_port', 'to_starboard',
        'epfd', 'month', 'day', 'hour', 'minute', 'draught', 'destination', 'dte', 'dac',
        'fid', 'data', 'offset1', 'number1', 'timeout1', 'increment1', 'offset2', 'number2',
        'timeout2', 'increment2', 'offset3', 'number3', 'timeout3', 'increment3', 'offset4',
        'number4', 'timeout4', 'increment4', 'year', 'aid_type', 'name', 'off_position',
        'regional', 'virtual_aid', 'assigned', 'name_extension', 'cs', 'display',
        'dsc', 'band', 'msg22', 'partno', 'vendorid', 'model', 'serial', 'mothership_mmsi', 'seqno', 'dest_mmsi', 'retransmit']


        DataFrame = pd.DataFrame(row_list, columns=cols)    
        
        # cols = DataFrame.columns.tolist()
        # cols.remove('timestamp')
        # cols = ['timestamp'] + cols

        # DataFrame = DataFrame[cols]
        # DataFrame.reset_index(drop=True, inplace=True)
        return DataFrame


def decodeMSG(inputFile: str, outputFolder: str, Timeframe: list):
    """
    Funzione che esegue il parsing del messaggio AIS
    inputFile: file di Testo.txt contentente messaggio AIS
    outputFolder: cartella di output
    Timeframe: tempo inizio, tempo fine --> ['16:59:24','16:59:44']
    """

    style = 'symbol:pin; fill:#0000ff; fill-opacity:0.7; stroke:#ffffff; stroke-opacity:1.0; stroke-width:0.5'
    text = None
    dateTime = None

    parser = NMEA_decoder(NMEA_log_path=inputFile)
    GPS = parser.get_GPS()
    ais = parser.to_df()
    ais.dropna(axis=0,subset=['lon','lat'], inplace=True)
    ais.reset_index(inplace=True, drop=True)

    ais = ais[ (ais['timestamp']>Timeframe[0]) & (ais['timestamp']<Timeframe[1])]
    ais.dropna(axis=0,subset=['lon','lat'], inplace=True)
    ais.reset_index(inplace=True, drop=True)

    SHP = gpd.GeoDataFrame(columns = ['style_css', 'label', 'text', 'dateTime', 'geometry'])
    ais.reset_index(inplace=True, drop=True)

    output_path = outputFolder

    for i in range(len(ais)):
        label = ais['mmsi'][i]
        # lat, lon = ais['latitude'][i], ais['longitude'][i]
        lat, lon = float(ais['lat'][i]), float(ais['lon'][i])
        coordinates = [(lon, lat)]
        geometry = Point(coordinates)
        new_row = {'style_css':style, 'label':label, 'text':text, 'dateTime':dateTime, 'geometry':geometry}
        SHP = SHP.append(new_row, ignore_index=True)
    SHP.to_file(output_path+'\\'+'navi.shp')




if __name__ == "__main__":
    file_path = "Input\\tobedecoded.txt"
    ais_msg = NMEA_decoder(file_path)
    ais_df = ais_msg.to_df()
    ais_df.to_excel('Ais_decoded.xlsx')