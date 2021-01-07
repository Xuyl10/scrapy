import requests
from bs4 import BeautifulSoup
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

def get_conferences():
    r = requests.get('https://api.crossminds.io/content/category/parents/details')
    content = r.text
    # print(content.decode())
    
    my_json = json.loads(r.content.decode())
    print(my_json)

    # # with open('test.json', 'r') as f:
    # #     my_json = json.load(f)
    # conferences = my_json['results'][0]
    # conferences_categories = conferences['subcategory']
    # conference_names = []
    # for category in conferences_categories:
    #     conference_names.append(category['name'])

    # return conference_names

if __name__ == '__main__':
    # get_conferences()

    url = "https://api.crossminds.io/web/content/bycategory"
    temp = {'search': {'category': 'CVPR 2020'},'limit': 20, 'offset': 0}
    data = json.dumps(temp)
    response = requests.post(url, data=data, headers={'Content-Type':'application/json'}).content.decode()
    # print(response.text)

    json_results = json.loads(response)["results"]
    for i in range(20):
        item = json_results[i]
        description = item["description"]
        title = item["title"]
        videoUrl = item["video_url"]
        year = item["category"][0].split(' ')[-1]
        str = ' '
        publicationOrg = str.join(item["category"][0].split(' ')[0:-1])
        #authors从description里找 没有的话再直接用json中的author字段
        #authors 


        print("description ",description)
        print("title ", title)
        print("videoUrl ",videoUrl)
        print("year  ", year)
        print("publicationOrg", publicationOrg)

    

