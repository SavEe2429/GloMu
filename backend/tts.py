import pyttsx3

# สร้าง engine ครั้งเดียว
_engine = pyttsx3.init()

# ตั้งค่าเสียง (ปรับได้)
_engine.setProperty("rate", 160)   # ความเร็วพูด
_engine.setProperty("volume", 1.0) # ความดัง

def speak_number(num):
    """
    รับเลข 1–4 แล้วพูดออกลำโพง
    """
    text_map = {
        1: "หนึ่ง",
        2: "สอง",
        3: "สาม",
        4: "สี่"
    }

    text = text_map.get(num, str(num))
    _engine.say(text)
    _engine.runAndWait()
