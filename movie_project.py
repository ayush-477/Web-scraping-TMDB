import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
import requests
needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
r = requests.get(('https://www.themoviedb.org/movie'),headers = needed_headers)
r.status_code
if r.status_code == 200:
    print(str(r.status_code) + " Request was executed successfully")
else:
    print("Failed. Request was not executed successfully")
response_data=r.text
print(response_data)
print(type(response_data))
print(response_data[0:200])
soup = BeautifulSoup(response_data, "html.parser")
soup.title.string
session=requests.Session()
session.max_redirects = 40
def func(inputurl):
  try:
    time.sleep(random.randint(3,8))
    needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    response = session.get((inputurl),headers = needed_headers)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      return soup
    else:
      raise requests.exceptions.HTTPError(f"Request failed with status code- {response.status_code}")
  except Exception as e:
    raise e
url=" https://www.themoviedb.org/movie"
soupobject=func(url)
first_movie = soupobject.find('div', class_='card style_1')
print(first_movie.prettify())
first = soupobject.find('div', class_='card style_1')
name=first.h2.a.text
print(name)
rating_percentage_first = soupobject.find(attrs={'data-percent': True})
rating_first = rating_percentage_first['data-percent']
print(rating_first)
first = soupobject.find('div', class_='card style_1')
url=first.h2.a["href"]
print(url[1:])
def list_of_movieTitles(soupobject):
  movie_titles=[]
  list_of_names = soupobject.findAll('div', class_='card style_1')
  for item in list_of_names:
    name=item.h2.a.text
    movie_titles.append(name)
  return(movie_titles)
print(list_of_movieTitles(soupobject))
def list_of_movieRatings(soupobject):
  movie_ratings=[]
  rating_percentages = soupobject.findAll(attrs={'data-percent': True})
  for rating in rating_percentages:
    temp = rating['data-percent']
    if(temp!="None"):
      movie_ratings.append(temp)
    else:
      movie_ratings.append("not rated")
  return(movie_ratings)
def list_of_HTML(soupobject):
  htmlist=[]
  listofHTML = soupobject.findAll('div', class_='card style_1')
  for item in listofHTML:
    htm=item.h2.a["href"]
    htmlist.append(htm[1:])
  return(htmlist)
print(len(list_of_HTML(soupobject)))
htmlist=list_of_HTML(soupobject)
def genres(htmlist):
  list_of_genres=[]
  for item in htmlist:
    url="https://www.themoviedb.org/"+item
    soupobj=func(url)
    genresouter=soupobj.find('div', class_='facts')
    genresinner=genresouter.find('span', class_='genres')
    final_list=genresinner.findAll('a')
    inner_list=[]
    for j in final_list:
      inner_list.append(j.text)
    list_of_genres.append(inner_list)
  return list_of_genres
print(genres(htmlist))
def cast(htmlist):
  list_of_cast_outer=[]
  for item in htmlist:
    url="https://www.themoviedb.org/"+item
    soupobj=func(url)
    castouter=soupobj.find('ol',class_='people scroller')
    castinner=castouter.findAll('li',class_="card")
    inner_list_cast=[]
    for x in castinner:
      op=x.find('p')
      inner_list_cast.append(op.text)
    list_of_cast_outer.append(inner_list_cast)
  return list_of_cast_outer
print(cast(htmlist))
def funcforpandas(soupobject,htmlist):
  column_names=["Title","User Rating","Genres","Cast"]
  dataframe= pd.DataFrame(columns=column_names)
  dataframe["Title"]=list_of_movieTitles(soupobject)
  dataframe["User Rating"]=list_of_movieRatings(soupobject)
  dataframe["Genres"]=genres(htmlist)
  dataframe["Cast"]=cast(htmlist)
  time.sleep(random.randint(5,8))
  return dataframe
x=funcforpandas(soupobject,htmlist)
x.head(n=10)
def funcpage(baseurl,page_no):
  dataframes=[]
  for i in range(page_no,4):
    soupObj=func(baseurl+"?page="+str(i))
    list_of_movies=list_of_HTML(soupObj)
    dataframes.append(funcforpandas(soupObj,list_of_movies))
  for i in range(4,6):
    soupObj=func(baseurl+"?page="+str(i))
    list_of_movies=list_of_HTML(soupObj)
    dataframes.append(funcforpandas(soupObj,list_of_movies))
  return dataframes
X=funcpage("https://www.themoviedb.org/movie",1)
concatenated_df=pd.DataFrame()
for i in range(5):
  concatenated_df = pd.concat([concatenated_df,X[i]])
concatenated_df.to_csv("partBfinal.csv",index=False)
