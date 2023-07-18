import genanki
import json
import os
from get_card_model import card_back, card_front, card_css

BASE_DIR = os.getcwd()


TOEFL_listening_setences_model = genanki.Model(
        4546874654,
        "TOEFL Listening Sentences",
        fields=[
            {'name': 'sentence_index_text'},
            {'name': 'en_text'},
            {'name': 'zh_text'},
            {'name': 'Media'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': card_front,
                'afmt': card_back
            }
        ],
        css=card_css
    )

def getInfo(tpo_code, set_code):
    data_dir = os.path.join(BASE_DIR, 'downloaded_data',
                             f'T{tpo_code}S{set_code}')
    with open(os.path.join(data_dir, f'T{tpo_code}S{set_code}_log.json'), encoding='UTF-8') as f:
        data = json.load(f)

    return data


def export_deck(tpo_code, set_code):
    TOEFL_listening_deck = genanki.Deck(
        int(f'1251879{tpo_code}654398{set_code}'),
        f'TOEFL Listening::TPO {tpo_code:02}::Set {set_code}'
    )

    data = getInfo(tpo_code, set_code)

    audio_list = []
    for i, d in enumerate(data):
        en_text = d['en_text'].replace('<-', '').replace('->', '').strip()
        zh_text = d['zh_text'].strip()
        audio_location = os.path.join(BASE_DIR, d['audio_location'])


        sentence_note = genanki.Note(
            model=TOEFL_listening_setences_model,
            fields=[f'Sentence {i+1} of TPO {tpo_code} Set {set_code}', en_text, zh_text, f"[sound:{audio_location}]"]
        )
        audio_list.append(audio_location)

        TOEFL_listening_deck.add_note(sentence_note)

    return TOEFL_listening_deck, audio_list


if __name__ == '__main__':
    decks = []
    all_audio_list = []
    for i in range(1, 55):
        for j in range(1, 7):
            if i == 36 and j == 1:
                pass
            else:
                try:
                    deck, deck_audio_list = export_deck(i, j)
                    decks.append(deck)
                    all_audio_list.extend(deck_audio_list)
                except:
                    print(f'No T{i}S{j}')
    
    print('Start export')
    TPO_package = genanki.Package(decks)
    TPO_package.media_files = all_audio_list

    TPO_package.write_to_file(os.path.join('export', f'TOEFL_listening.apkg'))
