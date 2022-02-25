#define M5STACK_MPU6886

#include <WiFi.h>
#include <WiFiUdp.h>
#include <M5Stack.h>

float accX, accY, accZ;
float gyroX, gyroY, gyroZ;
float pitch, roll, yaw;
int A_f = 0;

static int giBattery = 0;

const char ssid[] = "*****"; //WiFIのSSIDを入力
const char pass[] = "*****"; // WiFiのパスワードを入力

WiFiUDP wifiUdp; 
const char *pc_addr = "192.168.11.**";  //PCのアドレス
const int pc_port = 50007; //送信先のポート
const int my_port = 50008;  //自身のポート

void setup() {
  M5.begin();
  M5.Power.begin();
  M5.Speaker.write(0);
  M5.IMU.Init();
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextColor(WHITE , BLACK);
  M5.Lcd.setTextSize(2);

  WiFi.begin(ssid, pass);
  wifiUdp.begin(my_port);

  if(!M5.Power.canControl()) {
    //can't control.
    M5.Lcd.print("NG");
    return;
  }
}

void loop(){

  giBattery = M5.Power.getBatteryLevel();
  if(giBattery > 50){
    M5.Lcd.setCursor(250, 20);
    M5.Lcd.setTextColor(WHITE , BLACK);
    M5.Lcd.printf("%3d",giBattery);
  }else{
    M5.Lcd.setCursor(250, 20);
    M5.Lcd.setTextColor(RED , BLACK);
    M5.Lcd.printf("%3d \%",giBattery);
  }

  if(M5.BtnB.wasPressed()){
    wifiUdp.beginPacket(pc_addr, pc_port);
    wifiUdp.write('b');
    wifiUdp.endPacket();
  }
  if(M5.BtnB.wasReleased()){
    wifiUdp.beginPacket(pc_addr, pc_port);
    wifiUdp.write('d');
    wifiUdp.endPacket();
  }
  if(M5.BtnC.wasPressed()){
    wifiUdp.beginPacket(pc_addr, pc_port);
    wifiUdp.write('c');
    wifiUdp.endPacket();
  }
  if(M5.BtnC.wasReleased()){
    wifiUdp.beginPacket(pc_addr, pc_port);
    wifiUdp.write('e');
    wifiUdp.endPacket();
  }

  if(M5.BtnA.wasPressed()){
    if(A_f){
      wifiUdp.beginPacket(pc_addr, pc_port);
      wifiUdp.write('x');
      wifiUdp.endPacket();
      A_f = 0;
      M5.Lcd.setCursor(10, 20);
      M5.Lcd.setTextColor(WHITE , BLACK);
      M5.Lcd.printf("Wifi OFF");
    }else{
      A_f = 1;
      M5.Lcd.setCursor(10, 20);
      M5.Lcd.setTextColor(WHITE , BLUE);
      M5.Lcd.printf("Wifi ON ");
    }
  }

  if(A_f){
    String accX_txt = String(accX, 3);
    String accY_txt = String(accY, 3);
    String accZ_txt = String(accZ, 3);
    String gyroX_txt = String(gyroX, 3);
    String gyroY_txt = String(gyroY, 3);
    String gyroZ_txt = String(gyroZ, 3);
    String pitch_txt = String(pitch, 3);
    String roll_txt = String(roll, 3);
    String yaw_txt = String(yaw, 3);
    wifiUdp.beginPacket(pc_addr, pc_port);
    for(int i=0; i < 20; i++){
      wifiUdp.write(accX_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(accY_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(accZ_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(gyroX_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(gyroY_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(gyroZ_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(pitch_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(roll_txt[i]);
    }
    wifiUdp.write(',');
    for(int i=0; i < 20; i++){
      wifiUdp.write(yaw_txt[i]);
    }
    wifiUdp.endPacket(); 
    }else{
      M5.Lcd.setCursor(10, 20);
      M5.Lcd.setTextColor(WHITE , BLACK);
      M5.Lcd.printf("Wifi OFF");
  }

  M5.IMU.getAccelData(&accX,&accY,&accZ);
  M5.Lcd.setCursor(10, 50);
  M5.Lcd.setTextColor(WHITE , BLACK);
  M5.Lcd.printf("accel");
  M5.Lcd.setCursor(30, 70);
  M5.Lcd.setTextColor(WHITE , BLACK);
  M5.Lcd.printf("%5.2f, %5.2f, %5.2f", accX, accY, accZ);

  M5.IMU.getGyroData(&gyroX,&gyroY,&gyroZ);
  M5.Lcd.setCursor(10, 100);
  M5.Lcd.setTextColor(WHITE , BLACK);
  M5.Lcd.printf("gyro");
  M5.Lcd.setCursor(30, 120);
  M5.Lcd.setTextColor(WHITE , BLACK);
  M5.Lcd.printf("%5.2f, %5.2f, %5.2f     ", gyroX, gyroY, gyroZ);
  
  M5.IMU.getAhrsData(&pitch,&roll,&yaw);
  M5.Lcd.setCursor(10, 150);
  M5.Lcd.setTextColor(WHITE , BLACK);
  M5.Lcd.printf("PRY");
  M5.Lcd.setCursor(30, 170);
  M5.Lcd.setTextColor(WHITE , BLACK);
  M5.Lcd.printf("%5.2f, %5.2f, %5.2f     ", pitch, roll, yaw);

  delay(50);

  M5.update();

}
