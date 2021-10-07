from pyais import decode_msg
import pandas as pd
import pynmea2

class NMEA_decoder:
    def __init__(self, NMEA_log_path: str) -> None:
        self.file = NMEA_log_path

        with open (self.file, "r", encoding="utf-8") as myfile:
            tmp = myfile.read().splitlines()
            self.data = [line for line in tmp if line]

    def show_data(self):
        return self.data                 
   

    def getGPS(self):
        GPS_stream = [row for row in self.data if row[0]=='$']

        row_list = []
        for line in GPS_stream:
            msg = pynmea2.parse(line)
            try:
                assert(msg.is_valid)
                assert(msg.longitude)
                assert(msg.latitude)
                assert(msg.timestamp)

                time = msg.timestamp.isoformat()
                lat = msg.latitude
                lon = msg.longitude

                row = {'timestamp':time, 'latitude':lat, 'longitude':lon}
                row_list.append(row)
            except:
                pass

        df = pd.DataFrame(row_list, columns=list(row.keys()))
        return df



    def decode(self, line: str, idx: int):

        if self.data[idx][:10] == '!AIVDM,2,1':        # MULTI-LINE
            try:
                msg = decode_msg(line, self.data[idx+1])
                return msg
            except:
                pass
        else:
            try:
                msg = decode_msg(line)
                return msg
            except:
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


if __name__ == "__main__":
    file_path = "Input\\tobedecoded.txt"
    ais_msg = NMEA_decoder(file_path)
    ais_df = ais_msg.to_df()
    ais_df.to_excel('Ais_decoded.xlsx')