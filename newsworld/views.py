import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from newsworld.models import Headline

requests.packages.urllib3.disable_warnings()

def news_list(request):
	headlines = Headline.objects.all()[::-1]
	context = {
		'object_list': headlines,
	}
	return render(request, "newsworld/home.html", context)

def scrape(request):
	session = requests.Session()
	session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
	url = "https://www.theonion.com/"

	content = session.get(url, verify=False).content
	soup = BSoup(content, "html.parser")
	News = soup.find_all('div', {"class":"sc-1pw4fyi-3"})
	for article in News:
		main = article.find_all('a')[0]
		link = main['href']
		img_tag = main.find('img')
		print("Img tag: ", img_tag)
		try:
			image_src = str(img_tag['srcset']).split(" ")[-4] 
		except:
			continue
		title = main['title']
		new_headline = Headline()
		new_headline.title = title
		new_headline.url = link
		new_headline.image = image_src
		new_headline.save()
	return redirect("../")
