#-*- encoding: utf-8 -*-
import ConfigParser
#import IniFile
import string, os, sys
import codecs


cf = ConfigParser.ConfigParser()
#cf =IniFile.IniFile("pyllk.conf",encoding="utf-8")
cf.read("Chess.conf")
#cf.read("pyllk.conf")
#cf.readfp(codecs.open( "pyllk.conf", "r", "utf-8" ))

sEncoding = os.sys.getfilesystemencoding()

types =[]

# 返回所有的section
s = cf.sections()
print 'section:', s
for i in s:
   # print cf.items(i)
    m ={}
    for j in cf.options(i):
        m[j] = cf.get(i,j);
    #print m['type']
    types.append(m)
print types;

