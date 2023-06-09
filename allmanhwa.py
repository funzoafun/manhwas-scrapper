import sys

from util.allManhwas import AllManhwas
from providers.asura import getManhwaDetails

sys.path.append("/manhwa-scrapper/model")

def passManhwaLink(manhwaList):
    seen_items = set()
    for manhwa in manhwaList:
        if manhwa not in seen_items:
            try:
                getManhwaDetails(str('https://www.asurascans.com/manga/0879654290-solo-leveling/'))
                seen_items.add(manhwa)
            except Exception as e:
                print(f"An error occurred while processing {manhwa}: {e}")


# getManhwaDetails('https://www.asurascans.com/manga/1672760368-emperors-domination/')

# Asura
asuraManhwas = AllManhwas('https://www.asurascans.com/manga/list-mode/')
asuraManhwasList = asuraManhwas.getAllManhwasList

# # Cosmic
# cosmicManhwas = AllManhwas('https://cosmicscans.com/manga/list-mode/')
# cosmicManhwasList =  cosmicManhwas.getAllManhwasList
#
#
# # flameScans
# flameManhwas = AllManhwas("https://flamescans.org/series/list-mode/")
# flameManhwasList = flameManhwas.getAllManhwasList

passManhwaLink(asuraManhwasList)