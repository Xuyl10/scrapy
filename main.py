from crossminds_scrapy import crossminds_scrapy
from crossminds_parser import crossminds_parser

if __name__ == '__main__':
    items = crossminds_scrapy().get_items()
    crossminds_parser().parser(items)

