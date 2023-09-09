import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
#результат функции словарь {'neg': 0.0, 'neu': 0.256, 'pos': 0.744, 'compound': 0.4404}
def tone(txt):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(GoogleTranslator(source='auto', target='en').translate(txt))
    return scores 
