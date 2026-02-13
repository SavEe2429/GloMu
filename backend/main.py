from Local_Serial import (
    init_serial,
    dynamic_record_gesture,
    static_record_gesture,
    execute_gesture,
)
from tts import speak_number


def main():
    ser = None
    try:
        ser = init_serial()
        if ser is None:
            print("ไม่สามารถเชื่อมต่ออุปกรณ์ได้ ตรวจสอบสายเชื่อมต่อ")
            return

        while True:
            choice = input("เลือกโหมด (w: ใช้งานจริง , d: เก็บข้อมูล) : ").lower()
            match choice:
                case "w":
                        execute_gesture(ser)
                case "d":
                    cmd = input(
                        "เลือกโหมด (r: เก็บข้อมูลท่าเคลื่อนไหว, s: เก็บข้อมูลท่านิ่ง, t: ฟังเสียง, q: ออก): "
                    ).lower()

                    if cmd == "q":
                        break

                    elif cmd in ["r", "s"]:
                        label = input("ชื่อท่า :")
                        g_id = input("ID ของท่า :")

                        if cmd == "r":
                            dynamic_record_gesture(ser, label, g_id)
                        else:
                            static_record_gesture(ser, label, g_id)
                case _:
                    print("กรุณากรอก (w: ใช้งานจริง , d: เก็บข้อมูล)")

            # elif cmd == "t":
            #     print("โหมด TTS (กด Ctrl + C เพื่อออก)")
            #     try:
            #         while True:
            #             if ser.in_waiting:
            #                 line = ser.readline().decode(errors="ignore").strip()
            #                 print("รับ:", line)

            #                 # ถ้าเป็นตัวเลขล้วน
            #                 if line.isdigit():
            #                     speak_number(int(line))
            #             else:
            #                 time.sleep(0.01)

            #     except KeyboardInterrupt:
            #         print("\nออกจากโหมด TTS")

            # else:
            #     print("คำสั่งไม่ถูกต้อง โปรดใส่ r, s, t, q")

    except KeyboardInterrupt:
        print("\nปิดโปรแกรม")

    finally:
        if ser and ser.is_open:
            ser.close()
            print("ปิดการเชื่อมต่อ")


if __name__ == "__main__":
    main()
