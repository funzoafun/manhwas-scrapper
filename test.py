from util.single_manhwa import Manhwa


manhwa = Manhwa('https://www.asurascans.com/manga/1672760368-dr-player/')


manhwaSoup = manhwa.getManhwaSoup

manhwaTitle = manhwaSoup.find('h1', {'itemprop': 'name', 'class': 'entry-title'}).text
print(manhwaTitle)

