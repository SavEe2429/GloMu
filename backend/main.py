import csv , serial , time
from Local_Serial import init_serial, dynamic_record_gesture, static_record_gesture


def main():
    ser = None
    try:
        ser = init_serial()
        if ser is None:
            print("ไม่สามารถเชื่อมต่ออุปกรณ์ได้ ตรวจสอบสายเชื่อมต่อ")
            return # ออกจากโปรแกรมถ้าไม่มีการเชื่อมต่อ
        
        while True:
            cmd = input("เลือกโหมด (r: ท่าเคลื่อนไหว, s: ท่านิ่ง, q: ออก): ").lower()
            if cmd == 'q': break
            if cmd in ['r' , 's']:
                label = input("ชื่อท่า :")
                g_id = input("ID ของท่า :")
                if cmd == 'r':
                    dynamic_record_gesture(ser,label , g_id)
                else:
                    static_record_gesture(ser , label , g_id)
            else:
                print("คำสั่งไม่ถูกต้อง โปรดใส่ r , s ,q")

    except KeyboardInterrupt:
        print("\nปิดโปรแกรม")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("ปิดการเชื่อมต่อ")

if __name__ == "__main__":
    main()