from spellchecker import SpellChecker

import re
import sys

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)



def t9(text):
    spell = SpellChecker(language='ru')
    word = text
    cor = ""
    try:
        if spell.correction(str(word)) == str(word):
            cor += str(word)
        else:
            cor += spell.correction(str(word))
    except TypeError:
        cor = word
    return cor


from english_words import get_english_words_set

def translate_txt(txt):
    wordbook = [
        list("ё1234567890-=йцукенгшщзхъфывапролджэ\\ячсмитьбю.Ё!\"№;%:?*()_+ХЪЖЭ/БЮ,"),
        list("`1234567890-=qwertyuiop[]asdfghjkl;'\\zxcvbnm,./~!@#$%^&*()_+{}:\"|<>?")]
    text = ''
    for symbol in txt:
        for i in range(0, len(wordbook[1])):
            if symbol == wordbook[1][i]:
                text += wordbook[0][i]
                break
            elif symbol == wordbook[1][i].upper():
                text += wordbook[0][i].upper()
                break
            elif symbol == ' ':
                text += ' '
                break
            elif symbol == "\n":
                text += "\n"
                break
    return text

def translate_with_en(txt):
    txt = txt.split()
    text = ''
    lenn = len(txt)
    i=0
    web2lowerset = get_english_words_set(['web2'], lower=True)
    while i in range(lenn):
        if txt[i].lower()[0] in list("ё1234567890-=йцукенгшщзхъфывапролджэячсмитьбю"):
            text += t9(txt[i])+" "
        else:
            if txt[i].lower() in web2lowerset or txt[i].lower() in ['iphone', 'bmw']:
                text+=txt[i]+" "
            else:
                text+=translate_txt(txt[i])+" "
        i+=1
    return text
