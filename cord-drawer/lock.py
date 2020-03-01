import serial

ser = serial.Serial('/dev/ttyACM1', 9600)
ser.write('1,1\n'.encode())
