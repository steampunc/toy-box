import soundfile as sf
import numpy as np

filename = raw_input("Enter filename: ")
data, samplerate = sf.read(filename)

seed = raw_input("Enter Seed: ")
seed = int(''.join(str(ord(char) % 10) for char in seed)[-9:])
print(seed)

np.random.seed(seed)
message = ''
for counter, frame in enumerate(data):
  pseudorand_num = np.random.randn() * 0.25
  unhidden_val = frame - pseudorand_num
  try:
    unhidden_num = int(round(unhidden_val[0] * 254, 0))
    if(unhidden_num > 0):
      message += chr(unhidden_num)
  except:
    pass
print(message)
