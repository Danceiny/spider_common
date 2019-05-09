# -*- coding: utf-8 -*-

from .api import Api

# 替换成自己的授权信息
api = Api(api_key, api_secret, biz_channel)

content = {
    "title": {
      "type": "text",
      "value": "小米估值分析（微信：wnx907）",
      "recognizeTypes": [
        "porn",
        "illegal",
        "contact"
      ]
    },
    "content": {
      "type": "text",
      "value": "值得一提的是，小米的另一位创始人林斌，持有小米13.33%股权，按小米千亿美元估值来看，其身家将达到839.8亿元！如此，林斌的持股市值将超过刘强东，与百度李彦宏、360回A暴涨7倍的周鸿祎不相上下！今年50岁的林斌，和雷军一样少年时是个学霸，毕业于中山大学，曾是微软亚洲研究院的副院长。李开复离开微软后，林斌亦萌生退意，和雷军聊起创业想法时，说要不要做互联网音乐类，雷军大喜，且劝他，“别做音乐了，音乐我们投点钱，别人干就可以了，没意思。咱们一起做点更大的事情吧”。作为第一个登上小米战舰的船员，林斌此后一直不离不弃，伴随雷军度过了小米的风风雨雨。而他拿到的股权也充分证明了自己未辜负雷军的厚望。",
      "recognizeTypes": [
        "porn",
        "illegal",
        "contact"
      ]
    },
    "image0": {
      "type": "image",
      "value": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Xi_Jinping_2016.jpg/250px-Xi_Jinping_2016.jpg",
      "recognizeTypes": [
        "porn",
        "illegal",
        "ocr"
      ]
    },
    "image1": {
      "type": "image",
      "value": "http://img.mukewang.com/55755a9b000134e505000300.jpg",
      "recognizeTypes": [
        "porn",
        "illegal",
        "ocr"
      ]
    }
}

# 机审接口测试
#  res = api.robot_recognize_content_v2(content)
#  print(res)
# 机审+人审接口测试
#  res = api.recognize_content_v2(content)
#  print(res)
