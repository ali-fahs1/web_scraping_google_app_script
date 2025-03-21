import requests
import re
from bs4 import BeautifulSoup
import json
from itertools import zip_longest

import csv
i_states=['new-york','texas','ohio','florida','oregon','california','montana','arizona','michigan']
title=[]
state=[]
img=[]
link=[]
emails=[]
location=[]
website=[]
phone=[]
for i in i_states:
  r=requests.get(f'https://americasbestrestaurants.com/rests/{i}')
  soup=BeautifulSoup(r.text,'html.parser')
  div=soup.find_all('div',{'class':'companies local_listing element-item card'})
  for x in div:
        state.append(i.replace(f'https://americasbestrestaurants.com/rests/',''))
        link.append(f"https://americasbestrestaurants.com/{x.find('a')['href']}")
        img.append(f"https://americasbestrestaurants.com{x.find('a').find('div').find('img')['src']}")
        title.append(x.find('a').find('div',{'class':'content_local_listing'}).find('p',{'class':'story_title file-by'}).text)
for i in link:
      print(i)
      r2=requests.get(i)
      soup2=BeautifulSoup(r2.text,'html.parser  ')
      li=soup2.find('ul',{'class':'fs-5 fw-bold text-end h-100 d-flex flex-column justify-content-evenly'}).find_all('li')
      t=0
      for x in li:
           
           if '@' in x.text.strip():
                print(x.text.strip(),i)
                emails.append(x.text.strip())
                t=1
      if t==0:
          emails.append('')
  
data = zip_longest(title,state,img,link,emails)
print(data)
# save data to google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes=[
'https://www.googleapis.com/auth/speadsheets',
'https://www.googleapis.com/auth/drive'
]
creds=ServiceAccountCredentials.from_json_keyfile_name('orbital-ability-453910-m2-dc3b822afc81.json')
file=gspread.authorize(creds)
sheet=file.open('web_scraping_and_google_script')
spread_sheet=sheet.sheet1
headers=['title','state','img','link','email']
values=data
spread_sheet.update([headers]+ list(values))

