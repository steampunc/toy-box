import soundfile as sf
import numpy as np

raw_data = raw_input("Enter Data to be Encrypted: ")
seed = raw_input("Enter Seed: ")

# This is bad because it reduces entropy. If I ever make this a serious endeavor then I've got a _lot_ to fix.
seed = int(''.join(str(ord(char) % 10) for char in seed)[-9:])
print(seed)

length = max(len(raw_data), abs(np.random.randn()) * 100000)
print(length)

np.random.seed(seed)

data = np.zeros((int(length), 2))

for counter, frame in enumerate(data):
  data_val = 0
  try:
    data_val = float(ord(raw_data[counter])) / 254.0
  except:
    pass
  rand_num = np.random.randn() * 0.25
  value = rand_num + data_val
  data[counter] = (value, value) 
  if counter < 20:
    print(rand_num)
print(data)

sf.write("test.wav", data, 44100)

