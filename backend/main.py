from Local_Serial import (
    init_serial,
    dynamic_record_gesture,
    static_record_gesture,
    execute_gesture,
)



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
                        "เลือกโหมด (r: เก็บข้อมูลท่าเคลื่อนไหว, s: เก็บข้อมูลท่านิ่ง, q: ออก): "
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

    except KeyboardInterrupt:
        print("\nปิดโปรแกรม")

    finally:
        if ser and ser.is_open:
            ser.close()
            print("ปิดการเชื่อมต่อ")


if __name__ == "__main__":
    main()
