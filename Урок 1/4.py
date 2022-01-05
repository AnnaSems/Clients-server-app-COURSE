# 4.
LST = ["разработка", "администрирование", "protocol", "standard"]

def encode_decode(lst):
  for el in range(0, len(lst)):
    LST[el] = LST[el].encode(encoding='UTF-8')
    print(LST[el])
    LST[el] = LST[el].decode(encoding='UTF-8')
    print(LST[el], type(LST[el]))

encode_decode(LST)
print(LST)