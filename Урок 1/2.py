# 2.
LST = ['class', 'function', 'method']

def encode_word(lst):
    for el in range(0, len(lst)):
      LST[el] = eval(f"b'{lst[el]}'")
      print(LST[el])
      print(type(LST[el]))
      print(len(LST[el]))

encode_word(LST)