import requests
import os
from bs4 import BeautifulSoup

foldername='bookimgs'
if not (os.path.exists(f'./{foldername}')):
    os.mkdir(f'{foldername}')

def geturl(bname):
     searchurl=f"https://www.goodreads.com/search?q={bname}"
     searchpage= requests.get(searchurl).content
     soup = BeautifulSoup(searchpage, 'lxml')
     tag=soup.find('a',class_='bookTitle')
     return "https://www.goodreads.com"+tag.get('href')

def getpost(bookurl):
    bookpage= requests.get(bookurl).content
    soup= BeautifulSoup(bookpage, 'lxml')
    title= soup.find('h1', attrs={'data-testid': 'bookTitle'}).text
    authors= ", ".join([i.text for i in soup.find('div', class_='BookPageMetadataSection__contributor').find_all('span',class_='ContributorLink__name')])
    imgsrc = soup.find('img',class_='ResponsiveImage').get('src')
    image= requests.get(imgsrc).content
    with open(f'{foldername}/{title}.png','wb+') as f:
        f.write(image)
    rating = float(soup.find('div', class_="RatingStatistics__rating").text)
    star='⭐'
    stars = star*round(rating)
    desc = soup.find('div',class_='BookPageMetadataSection__description').find('span',class_='Formatted').get_text()
    post = \
    f"""
    {title}
    {authors}
    {stars} {rating}

    {desc}
    """
    return post

if __name__ =='__main__':
    book = input("enter a book name to search:")
    bookurl = geturl(book)
    print(getpost(bookurl))