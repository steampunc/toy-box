import base64
import string
import random

def xor(data, xor_key):
  result = b'';

  decoded_data = base64.b16decode(data)
  decoded_xor_key = str.encode(xor_key) 

  for val in decoded_data:
    result += bytes([val ^ decoded_xor_key[0]])
  try:
    str_result = result.decode("utf-8")
    return str_result
  except:
    return ""

def score_response(response):
  if " " in response:
    return (response.count("E") + response.count("T") + response.count("A") + response.count("O") + response.count("I") + response.count("N")) / len(response)
  else: return False


all_responses = []
for line in open("4.data"):
  for i in string.printable:
    response = xor(line[:-1].upper(), i).upper()
    if response != "":
      all_responses.append([response, score_response(response)])

all_responses = sorted(all_responses, key=lambda response: response[1], reverse=True)
for response in all_responses:
  if response[1] > 0.3:
    print(response)
