import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import wget
import json

DATA_DIR = 'downloaded_data'

class ListeningPage():
    def __init__(self, url, tpo_code, set_code) -> None:
        self.url = url
        self.tpo_code = tpo_code
        self.set_code = set_code

        print(f'Start downloading TPO {tpo_code} Set {set_code}')
        
        self.bs = BeautifulSoup(requests.get(url).content, features='lxml')

        self.en_text = [i.text for i in self.bs.find_all('p', class_='sentence-content')]
        self.zh_text = [i.text for i in self.bs.find_all('div', class_='translation-box')]
        self.audios = [i.get('data-url') for i in self.bs.find_all('li', class_="listen-sentence-list js-listen-sentence hide-original hide-translation")]

    def create_folder(self):
        dest_dir = os.path.join(DATA_DIR, f'T{self.tpo_code}S{self.set_code}')
        if not Path(dest_dir).exists():
            os.makedirs(dest_dir)
        
        self.dest_dir = dest_dir
        return dest_dir
    
    def download_audios(self):
        self.create_folder()

        for i, url in enumerate(self.audios):
            dest_audio_name = f'T{self.tpo_code}S{self.set_code}_sen{i+1}.mp3'
            dest_path = os.path.join(self.dest_dir, dest_audio_name)
            if not Path(dest_path).exists():
                wget.download(url, out=dest_path)
            else:
                print(f'T{self.tpo_code}S{self.set_code}_sen{i+1}.mp3 already exists!')

    def export_text(self):
        self.create_folder()

        result = []
        for i, (en, zh) in enumerate(zip(self.en_text, self.zh_text)):
            dest_audio_name = f'T{self.tpo_code}S{self.set_code}_sen{i+1}.mp3'
            audio_location = os.path.join(self.dest_dir, dest_audio_name)
            result.append({
                'en_text': en,
                'zh_text': zh,
                'audio_location': audio_location
            })

        with open(os.path.join(self.dest_dir, f'T{self.tpo_code}S{self.set_code}_log.json'), 'w', encoding='UTF-8') as f:
            json.dump(result, f, ensure_ascii=False)
        

if __name__ == '__main__':
    lp = ListeningPage('https://toefl.kmf.com/listening/newdrilling/c1el3j', 36, 1)
    lp.export_text()
    lp.download_audios()
