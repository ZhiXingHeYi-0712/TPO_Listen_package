from listening_page import ListeningPage
from listening_collections import getAllListeningPages
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=8)
listening_pages = getAllListeningPages()

def process(param):
    lp = ListeningPage(*param)
    lp.export_text()
    lp.download_audios()

pool.map(process, listening_pages)
pool.shutdown(wait=True)

