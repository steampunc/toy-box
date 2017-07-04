import base64

def xor(data, xor_key):
  result = b'';

  decoded_data = base64.b16decode(data) 
  decoded_xor_key = base64.b16decode(xor_key)

  print(decoded_data, decoded_xor_key)
  for pos, val in enumerate(decoded_data):
    result += bytes([val ^ decoded_xor_key[pos]])
    print(pos, val)
  return base64.b16encode(result)

print(xor("1c0111001f010100061a024b53535009181c".upper(), "686974207468652062756c6c277320657965".upper()))
