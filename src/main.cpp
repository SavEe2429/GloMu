#include <Arduino.h>
#include <Wire.h>
#include <MPU6050_light.h>

// indexFinger 34
// middleFinger 35
// ringFinger 32
// littelFinger 33
const int potPins[] = {34, 35, 32, 33};
struct DataType
{
  uint32_t timestamp; // Current Time
  float imu[6];       // ax, ay, az, gx, gy, gz; // Accelerometer Gyroscope
  int pot[4];         // Potentiometer 4 นิ้ว
};

// สร้าง Object MPU6050
MPU6050 mpu(Wire);
QueueHandle_t sensorQueue;
unsigned long timer = 0;

void taskSensorCollect(void *param)
{
  DataType sensorData;

  while (1)
  {
    mpu.update();
    sensorData.timestamp = pdTICKS_TO_MS(xTaskGetTickCount()); //  แปลงจาก Tick -> ms

    // เก็บค่าจาก GY-521
    sensorData.imu[0] = mpu.getAccX();
    sensorData.imu[1] = mpu.getAccY();
    sensorData.imu[2] = mpu.getAccZ();
    sensorData.imu[3] = mpu.getGyroX();
    sensorData.imu[4] = mpu.getGyroY();
    sensorData.imu[5] = mpu.getGyroZ();

    // เก็บค่าจาก Potentiometer
    for (int i = 0; i < 4; i++)
    {
      sensorData.pot[i] = analogRead(potPins[i]); // อ่านค่า adc
    }

    // ส่งข้อมูลไปใน Queue
    xQueueOverwrite(sensorQueue, &sensorData); // ส่งค่าเข้าไปใน Queue
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

void assignData(DataType &dataSend)
{
  Serial.printf("%u", dataSend.timestamp);
  for (int i = 0; i < sizeof(dataSend.imu) / sizeof(dataSend.imu[0]); i++)
  {
    Serial.printf(",%.2f", dataSend.imu[i]);
  }
  for (int i = 0; i < sizeof(dataSend.pot) / sizeof(dataSend.pot[0]); i++)
  {
    Serial.printf(",%d", dataSend.pot[i]);
  }
  Serial.println(); // จบบรรทัด
}

void taskSerial(void *param)
{
  DataType dataSend;

  while (1)
  {
    if (Serial.available() > 0)
    {
      char cmd = Serial.read();
      cmd = toupper(cmd);

      // บรรทัดนี้เพื่อล้างตัวอักษรที่ค้างใน Buffer (เช่น \n หรือ \r)
      while (Serial.available() > 0)
      {
        Serial.read();
      }

      if (cmd == 'S')
      {
        vTaskDelay(20 / portTICK_PERIOD_MS);
        if (xQueueReceive(sensorQueue, &dataSend, 0))
        {
          assignData(dataSend);
        }
      }
      if (cmd == 'R')
      {
        unsigned long recordStart = millis();
        const int duration = 2000;

        Serial.println("START_RECORDING");

        while (millis() - recordStart < duration)
        {
          if (xQueueReceive(sensorQueue, &dataSend, 20 / portTICK_PERIOD_MS))
          {
            assignData(dataSend);
          }
        }
        Serial.println("STOP_RECORDING");
      }
    }
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

void setup()
{
  Serial.begin(115200);
  Wire.begin(21, 22);

  // ส่วนของ GY-521
  Serial.println(F("\n--- เริ้มต้นทำงาน GY-521 ---"));
  byte status = mpu.begin(); // status = 0 ปกติ , 1 = ข้อมูลยาวไป, 2 = หาอุปกรณ์ไม่เจอ
  Serial.print(F("Status : "));
  Serial.println(status);
  // ถ้าไม่เชื่อมต่อก็ให้ทำการเชื่อมต่อซ้ำไปเรื่อยๆ
  while (status != 0)
  {
    delay(1000);
    status = mpu.begin(); // เริ่มทำงาน GY-521
    Serial.print(".");
  }
  // ขั้นตอนการ Calibrate ต้องวางนิ่งๆ
  Serial.println(F("กำลังคำนวณค่า Offset... ห้ามขยับเซนเซอร์เด็ดขาด!"));
  delay(2000);
  mpu.calcOffsets(true, true); // Calibrate ทั้ง Gyro และ Accel
  Serial.println(F("Calibrate เสร็จสิ้น!\n"));
  Serial.println(F("พิกัดปัจจุบัน (องศา):"));
  Serial.printf("X: %.2f\t\tY: %.2f\t\tZ: %.2f\n", mpu.getGyroX(), mpu.getGyroY(), mpu.getGyroZ());

  // ตั้งค่า Resolution เป็น 12-bit (0 - 4095)
  analogReadResolution(12);

  // ตั้งค่าความไว (Attenuation) เพื่อให้อ่านแรงดันได้สูงสุดประมาณ 3.3V
  analogSetAttenuation(ADC_11db);

  sensorQueue = xQueueCreate(1, sizeof(DataType));
  xTaskCreate(taskSensorCollect, "taskPotentiometer", 4095, NULL, 1, NULL);
  xTaskCreate(taskSerial, "taskSerial", 4095, NULL, 1, NULL);
}

void loop()
{
  // Serial.print("ADC Values: ");
  // for (int i = 0; i < 4; i++) {
  //   int val = analogRead(potPins[i]); // อ่านค่าจากขา 34, 35, 32, 33
  //   Serial.print(val);
  //   if (i < 3) Serial.print(", ");
  // }
  // Serial.println();
  // delay(100); // หน่วงเวลาเล็กน้อยเพื่อให้ดูทัน
}