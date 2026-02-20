import pyttsx3

def speak_number(num):
    # สร้าง engine ครั้งเดียว
    _engine = pyttsx3.init()
    voices = _engine.getProperty('voices')
    # ตั้งค่าเสียง (ปรับได้)
    _engine.setProperty("rate", 200)   # ความเร็วพูด
    _engine.setProperty("volume", 1.0) # ความดัง

    """
    รับเลข 1-4 แล้วพูดออกลำโพง
    """
    text_map = {
        0: "orangjuie",
        1: "one",
        2: "two",
        3: "three",
        4: "four"
    }

    text = text_map.get(num, str(num))
    _engine.say(text)
    _engine.runAndWait()

