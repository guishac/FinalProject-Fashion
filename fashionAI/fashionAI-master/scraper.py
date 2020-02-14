from bs4 import BeautifulSoup
import requests
from splinter import Browser

from pprint import pprint
import re
# from ai_model import predict
import json
import boto3


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver'}
    return Browser("chrome", **executable_path, headless=True)
    # browser = Browser('chrome', **executable_path, headless=False)

def scrape_info(si):
    browser = init_browser()
    # url = f"https://www.google.com/search?sa=X&biw=1536&bih=793&tbm=shop&psb=1&x=0&y=0&q={pipi['Predicted0']}"
    url = f"https://www.google.com/search?sa=X&biw=1536&bih=793&tbm=shop&psb=1&x=0&y=0&q={si}"

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('h4', class_='A2sOrd')
    results_2 = soup.find_all('div' , class_="sh-dgr__offer-content")


    #dictionary: item description, lists: item name, urllink, store name and price
    item_description = {}
    item_n = []
    item_l = []
    item_p = []
    item_s = []

    for result in results:
        try:
            item_name = result.text
            if (item_name):
                item_n.append(item_name)
                
        except AttributeError as e:
            print(e)
    # browser.quit()

    for result in results_2:
        try:
            item_price = result.span.find('span', class_='Nr22bf').text 
            item_url = result.a['href']
            item_store = result.a.text
            if (item_price and item_url and item_store):
                item_s.append(item_store)
                item_p.append(item_price[:-1]) 
                item_l.append('https://www.google.com'+item_url)
                
        except AttributeError as e:
            print(e)
    browser.quit()


    item_description = {'Item_Name':item_n[:3],
                     'Item_URL': item_l[:3],
                     'Item_Price': item_p[:3],
                     'Item_Store': item_s[:3],
                     'Prediction': si}
                      
                    
    
    return item_description
