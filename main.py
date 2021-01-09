from crossminds_scrapy import crossminds_scrapy
from crossminds_parser import crossminds_parser
import datetime

if __name__ == '__main__':
    print("start")
    starttime = datetime.datetime.now()
    items = crossminds_scrapy().get_items()
    crossminds_parser().parser(items)
    endtime = datetime.datetime.now()
    print(endtime - starttime)
