from spellchecker import SpellChecker

def t9(text):
    spell = SpellChecker(language='ru')
    text_split = text.split()
    cor = ""
    try:
        for word in text_split:
            if spell.correction(word) == word:
                cor += word+' '
            else:
                cor += spell.correction(word)+' '
    except TypeError:
        cor = text
    return {"t9_corretion" : cor}
