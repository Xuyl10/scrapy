import re
from bs4 import BeautifulSoup
import requests

# a = "**Self-Supervised Object-in-Gripper Segmentation from Robotic Motions**\nWout Boerdijk (DLR)*; Martin Sundermeyer (German Aerospace Center (DLR)); Maximilian Durner (DLR); Rudolph Triebel (German Aerospace Center (DLR)) Publication: http://corlconf.github.io/paper_275/\n\n\n**abstract: Accurate object segmentation is a crucial task in the context of robotic manipulation. However, creating sufficient annotated training data for neural networks is particularly time consuming a"
# a = "Abstract: Normalizing flows, autoregressive models, variational autoencoders (VAEs), a**Self-Supervised Object-in-Gripper Segmentation from Robotic Motions**\nWout Boerdijk nd deep energy-based models are among competing likelihood-based frameworks for deep generative learning. Among them, VAEs have the advantage of fast and tractable sampling and easy-to-access encoding networks. However, they are currently outperformed by other models such as normalizing flows and autoregressive models. While the majority of the research in VAEs is focused on the statistical challenges, we explore the orthogonal d\n\nAuthors: Arash Vahdat, Jan Kautz (NVIDIA)"
# result = re.findall('(?i)Abstract.*\n*.*\n*',a)

# print(result)
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/ \
    537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
rawpdfurl = "https://arxiv.org/abs/1912.02424"
abstract = ''
result = response = requests.get(
                rawpdfurl, headers={'User-Agent': user_agent}).content.decode()
soup = BeautifulSoup(result, 'lxml')
# blockquotes = soup.find('blockquote', class_="abstract mathjax")

# if blockquotes is not None:
#     abstract = blockquotes.contents[2]
#     print(abstract)

authors = ''
div = soup.find('div', class_='authors')
print(div)
a = div.find_all('a')
for i in a:
    authors += i.get_text()+','
authors = authors[:-1]
print(authors)