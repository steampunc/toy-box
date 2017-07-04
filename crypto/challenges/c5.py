def xor(data, xor_key):
  result = b'';

  for pos, val in enumerate(data):
    result += bytes([val ^ xor_key[pos % len(xor_key)]])
    print(pos % len(xor_key), val)
  return result.decode("utf-8")

data = str.encode("Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal")
xor_key = str.encode("ICE")
print(xor(data, xor_key))
