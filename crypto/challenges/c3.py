import base64
import string
import random

def xor(data, xor_key):
  result = b'';

  decoded_data = base64.b16decode(data) 
  decoded_xor_key = str.encode(xor_key) 

  for val in decoded_data:
    result += bytes([val ^ decoded_xor_key[0]])
  return result

def score_response(response):
  if " " in response:
    return (response.count("A") + response.count("E") + response.count("I") + response.count("O") + response.count("U")) / len(response)
  else: return False

xor_responses = []
for i in string.ascii_uppercase:
  response = xor("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".upper(), i).decode("utf-8").upper()
  xor_responses.append([response, score_response(response)])

xor_responses = sorted(xor_responses, key=lambda response: response[1], reverse=True)
for response in xor_responses:
  print(response)
