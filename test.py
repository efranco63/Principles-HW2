import os
if os.path.isfile('db.txt'):
    f = open('db.txt')
    for line in f:
        print line.split('|') 