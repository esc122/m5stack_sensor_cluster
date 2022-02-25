# -*-coding:utf-8-*-

from socket import *
import numpy as np
import pyautogui

# マウス操作
import ctypes
ULONG_PTR = ctypes.POINTER(ctypes.c_ulong)
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ULONG_PTR)]
class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]
LPINPUT = ctypes.POINTER(INPUT)
SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = (ctypes.c_uint, LPINPUT, ctypes.c_int)
SendInput.restype = ctypes.c_uint

pyautogui.FAILSAFE = False
acc_rate_move = 80
x_move = 0
y_move = 0
x_move = 0
threshold_move = 30
threshold_jump = 30
move_r = 0
s_f = 0
w_f = 0
d_f = 0
a_f = 0
acc_rate_mouse =  70
rate_mouse = 1
x_threshold_mouse = 15
y_threshold_mouse =  25
b_b_f = 0
d_b_after = 4
c_b_f = 0
rate_mouse_hand = 5

print("start network")
addr = ("192.168.11.**", 50007)  # PCのアドレス

print("network setup started")
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.settimeout(0.0001)
print("Connected !!")
print("Network info -->" + str(addr))
UDPSock.bind(addr) 

print("setup finished")

while True:
    try:
        (data, addr) = UDPSock.recvfrom(1024)
    except timeout:
        continue

    if addr !=0:
        str_data = data.decode('utf-8')
        # Bボタンが押されている状態（マウス操作による視点変更）
        if b_b_f == 1:
            if str_data != 'd':
                data_list = np.array(str_data.split(","))
                data_list = data_list.astype('float64')

                x_mouse = int(data_list[0] * acc_rate_mouse * -1)
                y_mouse = int((data_list[1] -0.1) * acc_rate_mouse * -1)
                x_mouse_move =  x_mouse * rate_mouse
                y_mouse_move =  y_mouse * rate_mouse
                print(x_mouse, y_mouse, 'b')
                if (x_mouse > x_threshold_mouse or x_mouse < x_threshold_mouse*-1) and (y_mouse > y_threshold_mouse or y_mouse < y_threshold_mouse*-1):
                    _mi = MOUSEINPUT(x_mouse_move, y_mouse_move, 0, (0x0001|0x0002), 0, None)
                    SendInput(1, INPUT(0, _mi), ctypes.sizeof(INPUT))
                elif (x_mouse > x_threshold_mouse or x_mouse < x_threshold_mouse*-1) and (y_mouse < y_threshold_mouse or y_mouse > y_threshold_mouse*-1):
                    _mi = MOUSEINPUT(x_mouse_move, 0, 0, (0x0001|0x0002), 0, None)
                    SendInput(1, INPUT(0, _mi), ctypes.sizeof(INPUT))
                elif (y_mouse > y_threshold_mouse or y_mouse < y_threshold_mouse*-1) and (x_mouse < x_threshold_mouse or x_mouse > x_threshold_mouse*-1) :
                    _mi = MOUSEINPUT(0, y_mouse_move, 0, (0x0001|0x0002), 0, None)
                    SendInput(1, INPUT(0, _mi), ctypes.sizeof(INPUT))
        # Cボタンが押されている状態（マウス操作により手を動かす）
        if c_b_f == 1:
            if str_data != 'e':
                data_list = np.array(str_data.split(","))
                data_list = data_list.astype('float64')

                x_mouse = int(data_list[0] * acc_rate_mouse * -1)
                y_mouse = int((data_list[1] -0.1) * acc_rate_mouse * -1)
                x_mouse_move =  x_mouse * rate_mouse_hand
                y_mouse_move =  y_mouse * rate_mouse_hand
                print(x_mouse, y_mouse, 'c')
                if (x_mouse > x_threshold_mouse or x_mouse < x_threshold_mouse*-1) and (y_mouse > y_threshold_mouse or y_mouse < y_threshold_mouse*-1):
                    _mi = MOUSEINPUT(x_mouse_move, y_mouse_move, 0, (0x0001|0x0002), 0, None)
                    SendInput(1, INPUT(0, _mi), ctypes.sizeof(INPUT))
                elif (x_mouse > x_threshold_mouse or x_mouse < x_threshold_mouse*-1) and (y_mouse < y_threshold_mouse or y_mouse > y_threshold_mouse*-1):
                    _mi = MOUSEINPUT(x_mouse_move, 0, 0, (0x0001|0x0002), 0, None)
                    SendInput(1, INPUT(0, _mi), ctypes.sizeof(INPUT))
                elif (y_mouse > y_threshold_mouse or y_mouse < y_threshold_mouse*-1) and (x_mouse < x_threshold_mouse or x_mouse > x_threshold_mouse*-1) :
                    _mi = MOUSEINPUT(0, y_mouse_move, 0, (0x0001|0x0002), 0, None)
                    SendInput(1, INPUT(0, _mi), ctypes.sizeof(INPUT))
        # 各ボタンが押されたときのフラグ
        if str_data == 'b':
            print('b')
            b_b_f = 1
        elif str_data == 'd':
            print('d')
            b_b_f = 0
            d_b_after = 0
        elif str_data == 'c':
            print('c')
            pyautogui.keyDown('c')
            c_b_f = 1
        elif str_data == 'e':
            print('e')
            pyautogui.keyUp('c')
            c_b_f = 0
            d_b_after = 0
        elif str_data == 'x':
            print('end')
            break
        else:
            # BもCも押されない状態（キーボードにより移動を押す）
            if b_b_f + c_b_f <= 0:
                if d_b_after > 3:
                    data_list = np.array(str_data.split(","))
                    data_list = data_list.astype('float64')

                    x_move = int(data_list[0] * acc_rate_move * -1)
                    y_move = int(data_list[1] * acc_rate_move)
                    z_move = int((data_list[2]-1) * acc_rate_move)
                    print(x_move, y_move, z_move, d_b_after, b_b_f, c_b_f)
                    if y_move > threshold_move:
                        if s_f == 0:
                                pyautogui.keyDown('s')
                                s_f = 1
                                move_r = 1
                    elif y_move < threshold_move*-1:
                        if w_f == 0:
                                pyautogui.keyDown('w')
                                w_f = 1
                                move_r = 1
                    elif x_move > threshold_move:
                        if d_f == 0:
                                pyautogui.keyDown('d')
                                d_f = 1
                                move_r = 1
                    elif x_move < threshold_move*-1:
                        if a_f == 0:
                                pyautogui.keyDown('a')
                                a_f = 1
                                move_r = 1
                    else:
                        move_r = 0
                
                # ジャンプ
                if z_move > threshold_jump:
                    pyautogui.press('space')
                
                # 移動ボタンを戻す
                if move_r == 0:
                    if s_f == 1:
                        pyautogui.keyUp('s')
                        s_f = 0
                    elif w_f == 1:
                        pyautogui.keyUp('w')
                        w_f = 0
                    elif d_f == 1:
                        pyautogui.keyUp('d')
                        d_f = 0
                    elif a_f == 1:
                        pyautogui.keyUp('a')
                        a_f = 0

            # 視点変更後に少し移動するのを避ける
            if d_b_after < 5:
                d_b_after += 1

print('finish')
