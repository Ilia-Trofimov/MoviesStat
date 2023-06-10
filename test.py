from array import array

import chardet as chardet

try:
    s = 'P'
    s2 = s.encode('ascii')
except UnicodeError:
    print('ERROR')
