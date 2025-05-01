import pandas as pd

def replace_emojis(text):
    emoji_map = {
        "😊": "기쁨", "😁": "행복", "😂": "웃음", "😢": "슬픔", "😭": "눈물",
        "😡": "화남", "😠": "분노", "😍": "좋아함", "😞": "실망", "😱": "놀람",
        "👍": "좋아요", "👎": "싫어요", "❤️": "사랑", "🔥": "강렬함", "👌": "나쁘지 않음", "🤗": "좋아함", "💪": "적극 추천",
        "🥹": "감동", "😋": "맛있음", "‼️": "강조", "🫶🏻": "감사",  "😀" : "웃음",
        "🌊": "시원함", "💫": "환상적", "🌸": "봄", "💙": "좋아요",  "☺️" : "행복",
        "🥰": "사랑스러움", "🩷": "핑크감성", "😓": "당황", "👍🏻": "좋아요"
    }

    for emoji, word in emoji_map.items():
        text = text.replace(emoji, f" {word} ")
    
    return text

df = pd.read_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviews.csv")

df["리뷰내용"] = df["리뷰내용"].astype(str).apply(replace_emojis)

df.to_csv("C:/Users/NM333-67/Desktop/personalized-tour-ai/All_reviewsd.csv", index=False, encoding="utf-8-sig")
