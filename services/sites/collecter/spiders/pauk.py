import scrapy
from bs4 import BeautifulSoup
from loguru import logger
class MavikSpider(scrapy.Spider):
    name='mavikSpider'
    start_urls=['https://www.dji.com/ru/products/camera-drones?site=brandsite&from=nav']
    
    def parse(self, response, **kwargs):
        
        for link in response.css('div.product-item a::attr(href)'):
            yield response.follow(link,callback=self.parse_charact)
    

    def parse_charact(self, response):
        for link in response.css('ul.sub-nav-right a::attr(href)'):
             yield response.follow(link,callback=self.parse_specs)


    def parse_specs(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        try:
        # if response.css('h3.section-title::text').get()=='Летательный аппарат':
            for i in range(0,len(soup.find('tbody').find_all('tr'))):
                yield{
                    'name1':soup.find('span',class_='parent').text,
                    f"{soup.find('table',class_='table-specs').find_all('th')[i].text}":soup.find('table',class_='table-specs').find_all('td')[i].text
                }

        # elif response.css('h3.section-title::text').get()=='Дрон':
            for i in range(0,len(soup.find('tbody').find_all('tr'))):
                yield{
                    'name2':soup.find('span',class_='parent').text,
                    f"{soup.find('table',class_='table-specs').find_all('th')[i].text}":soup.find('table',class_='table-specs').find_all('td')[i].text
                }

        # elif response.css('h3.group-list-title::text').get()=='Дрон':
            for i in range(0,len(soup.find_all('ul',class_='detailed-parameter-list'))):            
                yield{'name3':soup.find('p',class_='font-opensans product-title').text,
                    
                    soup.find_all('li','detailed-parameter-key')[i].text:soup.find_all('div','detailed-parameter-value')[i].text }
        except:
            logger.error("ERROR")

    

    
        


      

    