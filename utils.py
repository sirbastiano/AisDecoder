from datetime import timedelta, datetime

def findInterval(timestring0,timestring1):
     delta = timedelta(minutes=1, seconds=30)
     form = '%H:%M:%S'

     t0 = datetime.strptime(timestring0, form)
     t1 = datetime.strptime(timestring1, form)
     
     t0 = t0 - delta
     t0 = t0.strftime(form)

     t1 = t1 + delta
     t1 = t1.strftime(form)
     return t0, t1


def main():
     print('Main execution.')

if __name__=="__main__":
     main()
