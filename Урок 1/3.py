# 3.
LST = ["attribute", "класс", "функция", "type"]

def encode_word(lst):
    for el in range(0, len(lst)):
      if LST[el].isascii() == False:
        print(f'Слово "{LST[el]}" невозможно записать в байтовом типе.')
      else:
        LST[el] = eval(f"b'{lst[el]}'")

encode_word(LST)