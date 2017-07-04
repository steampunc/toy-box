import soundfile as sf
import numpy as np
import random

raw_data = ''
while True:
  user_input = raw_input("Enter f for file or t for raw text: ")
  if user_input.lower() == "f":
    with open(raw_input("Enter filename: "), 'r') as data_file:
      raw_data = data_file.read()
      break
  elif user_input.lower() == "t":
    raw_data = raw_input("Enter text: ")
    break
  else:
    print("Sorry, it looks like you didn't enter f or t. Please try again.")

seed = raw_input("Enter Seed: ")

seed = int(''.join(str(ord(char) % 10) for char in seed))

length = max(len(raw_data), random.random() * 100000)

random.seed(seed)

data = np.zeros((int(length), 2))

for counter, frame in enumerate(data):
  data_val = 0
  try:
    data_val = float(ord(raw_data[counter]) ^ ord(str(seed)[counter % len(str(seed))])) / (254.0 * 4) 
  except:
    pass
  rand_num = (random.uniform(-1, 1)) * 0.25
  value = rand_num + data_val
  data[counter] = (value, value) 

sf.write("encrypted_file.wav", data, 44100)

