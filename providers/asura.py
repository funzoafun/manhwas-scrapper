from util.single_manhwa import Manhwa
from model.manhwa import ManhwaItem
from model.chapter import Chapter, Chapters
import pymongo


SCRAPER_URL = 'http://api.webscrapingapi.com/v1'

def getMannhwaChapterDetails(chapterTagList, manhwaTitle, provider):
    chapter_list: list = []

    for chapterItem in chapterTagList:
        a_tag = chapterItem.find('a')
        chapter_num = a_tag.find('span',{'class':'chapternum'}).text
        chapter_date = a_tag.find('span',{'class':'chapterdate'}).text
        chapter_link = a_tag['href']
        chapter_list.append({'chapterNumber':chapter_num, 'chapterDate':chapter_date})
    manhwaChapters = Chapters()
    manhwaChapters.provider = provider
    manhwaChapters.manhwaTitle = manhwaTitle
    manhwaChapters.chapters = chapter_list
    return manhwaChapters


def getManhwaDetails(manhwaUrl):

    manhwa = Manhwa(manhwaUrl)
    manhwaSoup = manhwa.getManhwaSoup
    # manhwaTitle = manhwaSoup.find('h1', {'itemprop': 'name', 'class': 'entry-title'}).text if manhwaSoup.find('h1', {'itemprop': 'name', 'class': 'entry-title'}) else None
    manhwa_chapters_tags = manhwaSoup.findAll('div', {'class': 'chbox'})

    manhwaItem = ManhwaItem()
    manhwaItem.title = manhwaSoup.find('h1', {'itemprop': 'name', 'class': 'entry-title'}).text if manhwaSoup.find('h1', {'itemprop': 'name', 'class': 'entry-title'}) else None
    # manhwaItem.chapters = getMannhwaChapterDetails(manhwa_chapters_tags)
    manhwaItem.coverImgUrl = manhwaSoup.find('div',{'class':'thumb'}).find('img',{'itemprop':'image'})['src'] if manhwaSoup.find('div',{'class':'thumb'}).find('img',{'itemprop':'image'}) else None
    manhwaItem.provider = manhwaUrl.split('.')[1].split('.')[0]
    manhwaItem.description = ' '.join(p.text for p in manhwaSoup.select('div.entry-content-single p'))
    manhwaItem.genres = [tag.text for tag in manhwaSoup.find_all('a', {'class':'tag'})]
    manhwaChapters = getMannhwaChapterDetails(manhwa_chapters_tags,manhwaItem.title, manhwaItem.provider )

    try:

        client = pymongo.MongoClient("mongodb+srv://rajpranit1207:rajpranit123@animascluster.4m2s0wm.mongodb.net/test")
        db = client['manhwas']
        manhwa_id = db.manhwa.insert_one(vars(manhwaItem)).inserted_id
        chapter_id = db.chapters.insert_one(manhwaChapters).inserted_id
        db.manhwa.update_one({"_id": manhwa_id}, {'$push': {'chpaters': chapter_id}})
    except Exception as e:
        print(f"Error: {e}")
    

    print(vars(manhwaItem))



# def getChapterDetails(chapterlink, chapterno):
#     chapter_image_no_list = []
#     chapter_img_list = []
#     chapter_url = chapterlink
#     manhwa_chapter_params = {
#         'api_key': API_KEY,
#         'url': chapter_url,
#         'render_js': 1
#     }
#     manhwa_chapter_response = requests.get(SCRAPER_URL, params=manhwa_chapter_params)
#     manhwa_chapter_content = manhwa_chapter_response.text
#     chapter_soup = BeautifulSoup(manhwa_chapter_content, 'html.parser')
#     alt_image = chapter_soup.findAll('img', {'class': 'alignnone'}, alt=True)
#     if(len(alt_image) <=2):
#         another_alt_img = chapter_soup.findAll('img', {'class':'aligncenter'}, alt=True)
#         for img in another_alt_img[1:]:
#             chapter_img_list.append(img['src'])
#     else:
#         for img in alt_image[1:]:
#             chapter_img_list.append(img['src'])
#     return {chapterno: chapter_img_list}
#
#
#
# chapter_list = []
#
# for chapter in manhwa_chapters:
#     a_tag = chapter.find('a')
#     chapter_num = a_tag.find('span',{'class':'chapternum'}).text
#     chapter_link = a_tag['href']
#     chapter_list.append({chapter_num:chapter_link})
#
# #print(chapter_list)
#
#
# all_manhwa_chapters = []
# for dictionary in chapter_list:
#     for chapter, url in dictionary.items():
#         chapters_image_list = getChapterImages(url,chapter)
#         all_manhwa_chapters.append(chapters_image_list)
#
#
# print("all manhwa chapters with images", all_manhwa_chapters)
# manhwa_data = {all_manhwa_chapters}
# print('manhwa_data', manhwa_data)
# client = pymongo.MongoClient("mongodb+srv://rajpranit1207:rajpranit123@animascluster.4m2s0wm.mongodb.net/test")
# db = client['manhwas']
# collection = db['manhwa']
#
# insert_result = collection.insert_one(manhwa_data)
# print(insert_result)



