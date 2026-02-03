import serial, csv, time , os
from serial.tools import list_ports

HEADER = ["id", "gesture_name", "timestamp", "ax", "ay", "az", "gx", "gy", "gz", "p0", "p1", "p2", "p3"]

def save_csv(filename, data_rows):
    """ฟังก์ชั่นเริ่มต้น csv และสร้างโฟลเดอร์ถ้าไม่มีอยู่"""
    # 🎯 เพิ่มส่วนนี้: ดึงชื่อโฟลเดอร์จาก filename
    dirname = os.path.dirname(filename)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname) # สร้างโฟลเดอร์ (เช่น backend) ให้โดยอัตโนมัติ
        print(f"📁 Created directory: {dirname}")

    file_exist = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exist:
            writer.writerow(HEADER)
        writer.writerows(data_rows)

def find_ports():
    """หา port ที่เชื่อมต่ออยู่"""
    ports = list_ports.comports()
    if not ports:
        print("ไม่พบ port ไหนเลย")
        return []

    target_keywords = ["USB", "CP210", "CH340", "UART", "Bridge"]
    print("\n--- Serial Ports ที่พบ")

    for port in ports:
        for keyword in target_keywords:
            if keyword.upper() in port.description.upper():
                print(f"- PORT : {port.device} | DESCRIPTION: {port.description}")
                return port.device

    print("ไม่พบพอร์ตที่เข้าข่าย ESP32 กรุณาตรวจสอบการเสียบสาย")
    return None


def init_serial(BAUD_RATE=115200):
    SERIAL_PORT = find_ports()

    if SERIAL_PORT:
        try:
            # connecting serial
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)  # รอให้ esp32 reboot เสร็จ
            ser.reset_input_buffer() # ล้างขยะตอนเริ่มต้น
            print("Connected!!")
            return ser

        except Exception as e:
            print(f"Connection Error: {e}")
    else:
        # หาไม่เจอก็ใส่ชื่อมาเอง
        manual_port = input("กรุณาระบุพอร์ตเอง (เช่น COM3 หรือ /dev/ttyUSB0): ")


def dynamic_record_gesture(ser , label, gesture_id):
    filename = f"./backend/dynamic_record_gesture.csv"
    print(f"เตรียมบันทึกท่า : {label} (ID : {gesture_id})\n")
    input("กด Enter เมื่อพร้อมขยับมือ...")

    print(f"บันทึกลงไฟล์: {filename}")
    ser.write(b"R")  # ส่งคำสั่ง r ไปที่ ESP32
    data_list = []
    recording = False

    while True:
        line = ser.readline().decode("utf-8").strip() # อ่านข้อมูลจาก serial
        if line == "START_RECORDING":
            recording = True
            print(">>> กำลังบันทึก... ขยับมือได้")
            continue
        if line == "STOP_RECORDING":
            print(">>> หยุดบันทึก")
            break

        if recording and line:
            # line จะมี 11 ค่าจาก ESP32
            raw_data = line.split(",")  # แบ่งข้อมูลที่มี , คั่น
            if len(raw_data) == 11:
                full_row = [gesture_id , label] + raw_data
                data_list.append(full_row)

    if data_list:
        save_csv(filename,data_list)
        print(f"บันทึกข้อมูลท่า {label} เรียบร้อยแล้ว ({len(data_list)}) แถว\n")


def static_record_gesture(ser , label, gesture_id):
    filename = f"./backend/static_gesture_data.csv"
    print(f"เตรียมบันทึกท่า : {label} (ID : {gesture_id})\n")
    input("กด Enter เมื่อพร้อมขยับมือ...")

    print(f"บันทึกลงไฟล์: {filename}")
    ser.write(b"S") 
    line = ser.readline().decode("utf-8").strip() # อ่านข้อมูลจาก serial
    if line:
        raw_data = line.split(",")
        if len(raw_data) == 11:
            full_row = [gesture_id , label] + raw_data
            save_csv(filename,[full_row])
        print(f"บันทึก Snapshot ท่า {label} สำเร็จ: {line}")
    else:
        print("ไม่มีข้อมูลตอบกลับ (Timeout)")

