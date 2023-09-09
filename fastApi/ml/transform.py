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
        if txt[i].lower() in web2lowerset:
            text+=txt[i]+" "
        else:
            text+=translate_txt(txt[i])+" "
        i+=1
    return text
print(translate_with_en(f"'nj ghjcnj ghtrhfcyj? Acer ltkftn dtob"))
