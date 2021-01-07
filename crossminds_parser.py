import json
from crossminds_config import crossminds_config
from tqdm import tqdm
from crossminds_saver import crossminds_saver
from crossminds_scrapy import crossminds_scrapy
from bs4 import BeautifulSoup
import re

class crossminds_parser:

    def parse_title(self,item):
        #todo:title处理 不同会议的怎么处理
        raw_title = item["title"]
        # title = raw_title.split(']')[-1].strip()
        return raw_title

    def parse_author(self,item):
        #todo:
        # authors从description里找 没有的话再直接用json中的author字段

        return item["author"]["name"]

    def parse_publicationOrg(self,item):
        str = ' '
        publicationOrg = str.join(item["category"][0].split(' ')[0:-1])
        return publicationOrg

    def parse_url(self,item):
        #从网页中解析出url
        rawpdfurl = ''
        rawcodeurl = ''
        id = item["_id"]
        url = "https://crossminds.ai/video/{}/".format(id)
        result = crossminds_scrapy().get_content(url).decode()
        soup = BeautifulSoup(result, 'lxml')
        divs = soup.find('div',class_ = 'video-attached-link')
        if divs is not None:
            a = divs.find_all('a')
            for i in a:
                spans = i.find_all('span')
                # print(spans)
                for span in spans:
                    text = span.contents[0]
                    # print("text: " ,text)
                    if text == "Paper Link":
                        rawpdfurl = i["href"]
                        print("rawpdfurl: ",rawpdfurl)
                    if text == "Code Link":
                        rawcodeurl = i["href"]
                        print("rawcodeurl: ",rawcodeurl)
                if rawpdfurl!='' and rawcodeurl!='':
                    break  
        #从description中解析
        string = item["description"]
        # print("description: \n", string)
        urls = re.findall('https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', string)
        print("urls: ", urls)
        for url in urls:
            if "github" in url:
                rawcodeurl = url
            if "arxiv.org" in url:
                rawpdfurl = url
            if "aclweb.org/" in url:
                rawpdfurl = url
            if rawpdfurl!='' and rawcodeurl!='':
                    break 
        #处理得到的url
        pdfurl=''
        if "arxiv.org" in rawpdfurl:
            pdfurl = rawpdfurl.replace('abs', 'pdf') + '.pdf'
        if "aclweb.org" in rawpdfurl:
            pdfurl = rawpdfurl[:-1]+".pdf"
        codeurl=rawcodeurl
        return pdfurl, codeurl
        

    def parse_abstract(self,item):
        #预计从description中解析，先判断有无abstract字样，有的话根据回车提取？maybe
        description = item["description"]
        if re.search('abstract', description, re.IGNORECASE) is not None:
            
            pass
        else:
            return ''

    def parser(self, items):
        json_results = []
        for i in range(len(items)):
            for j in range(len(json.loads(items[i])["results"])):
                json_results.append(json.loads(items[i])["results"][j]) 
        for i in tqdm(range(len(json_results))):
            item = json_results[i]
            title = self.parse_title(item)
            videoUrl = item["video_url"]
            year = item["created_at"][0:4]
            publicationOrg = self.parse_publicationOrg(item)
            authors = self.parse_author(item)
            pdfurl,codeurl = self.parse_url(item)
            datasetUrl = ''
            videoPath = ''
            pdfPath = ''
            abstract = self.parse_abstract(item)
            publicationUrl = ''
            _id = item["_id"]

            paperInfo = {
                "_id": _id,
                "title" : title,
                "authors": authors,
                "abstract": abstract,
                "publicationOrg": publicationOrg,
                "year": year,
                "pdfUrl": pdfurl,
                "pdfPath": "",
                "publicationUrl":publicationUrl,
                "codeUrl": codeurl,
                "datasetUrl": datasetUrl,
                "videoUrl": videoUrl,
                "videoPath": ""
            }


            print("id: ", _id)
            print("title: ", title)
            print("authors: ", authors)
            print("abstract: ", abstract)
            print("year: ", year)
            print("publicationOrg: ", publicationOrg)
            print("pdfurl: ", pdfurl)
            print("pdfPath: ", pdfPath)
            print("videoUrl: ", videoUrl)
            print("videoPath: ", videoPath)
            print("datasetUrl: ", datasetUrl)
            print("publicationUrl: ",publicationUrl)
            print("codeurl: ", codeurl)

            # crossminds_saver().savePaperInfo(paperInfo)




