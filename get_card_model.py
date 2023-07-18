card_front = None
card_back  = None
card_css   = None

with open('./card_model/card_front.html', encoding='UTF-8') as f:
    card_front = f.read()

with open('./card_model/card_back.html', encoding='UTF-8') as f:
    card_back = f.read()

with open('./card_model/card_css.css', encoding='UTF-8') as f:
    card_css = f.read() 