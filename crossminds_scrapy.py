import requests
import json
from requests import exceptions 
from crossminds_config import crossminds_config
from tqdm import tqdm

class crossminds_scrapy():
    def get_content(self,url):
        try:
            response = requests.get(url)

            response = requests.get(url,  headers={'User-Agent': crossminds_config.user_agent})
            response.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
            response.encoding = response.apparent_encoding  # 判断网页的编码格式， 便于respons.content知道如何解码;
        except exceptions.Timeout:
            print('请求超时' )
        except exceptions.HTTPError:
            print('http请求错误')
        else:
            return  response.content

    def post_content(self,url,data):
        try:
            response = requests.post(url=url, data=data, headers={'Content-Type':'application/json'})
            response.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
            response.encoding = response.apparent_encoding  # 判断网页的编码格式， 便于respons.content知道如何解码;
        except exceptions.Timeout:
            print('请求超时')
        except exceptions.HTTPError:
            print('http请求错误')
        else:
            return  response.content

    def get_categaries(self):
        url = "https://api.crossminds.io/content/category/parents/details"
        content = self.get_content(url).decode()
        json_results = json.loads(content)["results"]
        subcategory = json_results[0]["subcategory"]
        categaries = []
        for categary in subcategory:
            categaries.append(categary["name"])
        print(categaries)
        return categaries
    
    def get_items(self):
        url = "https://api.crossminds.io/web/content/bycategory"
        categories = self.get_categaries()
        items = []
        for category in tqdm(categories):
            #if category == "NeurIPS 2020":
            data = {'search': {'category': category},'limit': crossminds_config.request_num, 'offset': 0}
            result = self.post_content(url,json.dumps(data)).decode()
            items.append(result)
        # print(items)
        return items

if __name__ == '__main__':
    cm_scrapy = crossminds_scrapy()
    cm_scrapy.get_categaries()
    cm_scrapy.get_items()
