from pyais import decode_msg
import pandas as pd
import pynmea2

class NMEA_decoder:
    def __init__(self, NMEA_log_path: str) -> None:
        self.file = NMEA_log_path
        
                 
    def clock(self, line, idx: int):
        with open (self.file, "r") as myfile:
            data = myfile.read().splitlines()
        
        if data[idx+2][0] != '$':        # MULTI-LINE
            try:
                msg = pynmea2.parse(line, data[idx+2])
                time = msg.timestamp.isoformat()
                return time
            except pynmea2.ParseError as e:
                print(e)
        else:
            try:
                msg = pynmea2.parse(line)
                time = msg.timestamp.isoformat()
                return time
            except pynmea2.ParseError as e:
                print(e)

    def decode(self, line: str, idx: int):
        with open (self.file, "r") as myfile:
            data = myfile.read().splitlines()

        if data[idx+2][0] == '!':        # MULTI-LINE
            try:
                msg = decode_msg(line, data[idx+2])
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
        DataFrame = pd.DataFrame()
        with open (self.file, "r", encoding="utf-8") as myfile:
            data = myfile.read().splitlines()

        def get_clock(idx, data):
            for i in range(30):
                try:
                    line = data[idx+i]
                    msg = pynmea2.parse(line)
                    time = msg.timestamp.isoformat()
                    if isinstance(time, str):
                        return time
                except pynmea2.ParseError:
                    continue
                except AttributeError:
                    continue
            


        for idx, line in enumerate(data):
            try:
               if line != '':
                    if line[0] == '!':
                        msg = self.decode(line, idx)
                        time = get_clock(idx, data)
                        msg['timestamp'] = time
                        df = pd.DataFrame(msg, index=[idx])
                        DataFrame = DataFrame.append(df)

            except:
                continue
            
        
        cols = DataFrame.columns.tolist()
        cols.remove('timestamp')
        cols = ['timestamp'] + cols

        DataFrame = DataFrame[cols]
        DataFrame.reset_index(drop=True, inplace=True)
        return DataFrame


if __name__ == "__main__":
    file_path = "Input\\tobedecoded.txt"
    ais_msg = NMEA_decoder(file_path)
    ais_df = ais_msg.to_df()
    ais_df.to_excel('Ais_decoded.xlsx')