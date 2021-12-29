# 6.
import chardet

LST = ['сетевое программирование', 'сокет', 'декоратор']
def test_file():
    with open('test_file.txt', 'w') as test_f:
      for line in LST:
        test_f.write(line + '\n')

    f = open('test_file.txt')
    read_file = f.read()
    print(read_file)

    f_unicode = open('test_file.txt', 'rb')
    read_unicode_file = f_unicode.read()
    print(read_unicode_file)

test_file()