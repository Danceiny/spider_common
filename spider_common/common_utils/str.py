import re

try:
    # Wide UCS-4 build
    myre = re.compile(u'['
                      u'\U0001F300-\U0001F64F'
                      u'\U0001F680-\U0001F6FF'
                      u'\u2600-\u2B55'
                      u'\u23cf'
                      u'\u23e9'
                      u'\u231a'
                      u'\u3030'
                      u'\ufe0f'
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u'\U00010000-\U0010ffff'
                      u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                      u'\U00002702-\U000027B0]+',
                      re.UNICODE)
except re.error:
    # Narrow UCS-2 build
    myre = re.compile(u'('
                      u'\ud83c[\udf00-\udfff]|'
                      u'\ud83d[\udc00-\ude4f]|'
                      u'\uD83D[\uDE80-\uDEFF]|'
                      u"(\ud83d[\ude00-\ude4f])|"  # emoticon
                      u'[\u2600-\u2B55]|'
                      u'[\u23cf]|'
                      u'[\u1f918]|'
                      u'[\u23e9]|'
                      u'[\u231a]|'
                      u'[\u3030]|'
                      u'[\ufe0f]|'
                      u'\uD83D[\uDE00-\uDE4F]|'
                      u'\uD83C[\uDDE0-\uDDFF]|'
                      u'[\u2702-\u27B0]|'
                      u'\uD83D[\uDC00-\uDDFF])+',
                      re.UNICODE)


def remove_emoji(text):
    return myre.sub(' ', text)
