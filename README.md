# scrapy

## 目录结构
│  README.md   
│--crossminds  
│     crossminds_config.py  参数设置  
│     crossminds_parser.py  解析对应的论文的各个字段  
│     crossminds_scrapy.py  按会议类别取论文  
│     crossminds_saver.py   存数据库、重复判断  
│     downloader.py         负责视频和PDF文件的下载  
│     main.py               运行程序的入口  
│


## 环境 
- python3

运行必须要安装的包
```
pip install requests
pip install beautifulsoup4
pip install lxml
pip install pymongo
pip install pytube
pip install json
```

## 整体流程
1、首先通过 https://api.crossminds.io/web/node/interest-list?offset=0&limit=10 接口获得crossminds中按Knowledge Area分的十个类别

2、通过 https://api.crossminds.io/web/node/video/name/{category}?limit=1500&offset=0 从各个类别中获取相应的论文的json数据，category为第1步中获取到的类别（由于在网站中可以直接看到每个类别的item数量，最大为1471，所以这里的limit先设置为了1500）

3、解析每个论文的json数据  
着重说明以下几个字段的解析
- pdfurl字段
```
由于crossminds给到的paperurl并不统一，有些是用paperlink做了链接，而有些直接写在了一篇paper对应的description中，所以这里采用两种方式解析：
- 每片paper对应的json文件中都有对应的_id，而它所对应的展示页面对应于https://crossminds.ai/video/_id，通过使用beautifulsoup可以解析对应的页面中的paperlink
- 如果页面中没有paperlink链接，则去相应的description中使用正则表达式找到pdf的地址，并做相应的替换，便于后续下载pdf使用
```
- abstract字段
```
- crossminds中paper的description部分包含abstract，有些会明确指出有abstract，对于这种我们用正则表达式提取出abstract部分
- 如果没有且之前爬到了对应的pdfurl，比如arxiv网站的url，则用beautifulsoup解析arxiv中论文主页的摘要
```
- authors字段
```
- crossminds中paper的json数据中有authors字段，但很多的上传者都是“computor vision”此类，对于没有pdfurl的paper，我们直接使用该字段
- 对于爬到了pdfurl的paper，比如arxiv网站的url，则用beautifulsoup解析arxiv中论文主页的作者
```
4、数据的存储，使用pymongo存储到了mongodb数据库中  
5、视频和pdf的下载，将视频和PDF文件下载到本地，将存储路径存到mongodb数据库中



