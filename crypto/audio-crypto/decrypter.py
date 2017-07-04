import soundfile as sf
import numpy as np
import random

filename = raw_input("Enter filename of audio to decrypt: ")
data, samplerate = sf.read(filename)

seed = raw_input("Enter Seed: ")
seed = int(''.join(str(ord(char) % 10) for char in seed))

random.seed(seed)
message = ''
for counter, frame in enumerate(data):
  pseudorand_num = random.uniform(-1, 1) * 0.25
  unhidden_val = frame - pseudorand_num
  try:
    unhidden_num = int(round(unhidden_val[0] * 254 * 4, 0))
    if unhidden_num > 0:
      unhidden_num = unhidden_num ^ ord(str(seed)[counter % len(str(seed))])
    if(unhidden_num > 0 and unhidden_num < 128):
      message += chr(unhidden_num)
  except:
    pass
print(message)

with open("decrypted_file.txt", 'w') as out_file:
  out_file.write(message)
