from spellchecker import SpellChecker

def t9(text):
    spell = SpellChecker(language='ru')
    text_split = text.split()
    cor = ""
    for word in text_split:
        if spell.correction(word) == word:
            cor += word+' '
        else:
            cor += spell.correction(word)+' '
    return cor
print(t9('привед бротанн'))
