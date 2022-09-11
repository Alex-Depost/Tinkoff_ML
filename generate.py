# -*- coding: utf8 -*-#
import os
import argparse
import re
import sys
import pickle
import random

#"c:\dev\MyPythonPrg\Tinkoff_generate_text\data" 'my_model1'

class mygenerate:    
    def __init__(self, modelfile, prefix, length):
        self.modelfile=modelfile
        self.prefix=prefix
        self.length=length        
        
    def generate(self):
        #dumpfilename = os.path.join(self.inputdir, self.model+'.pkl')
        model={}
        with open(self.modelfile, 'rb') as fp:
            model=pickle.load(fp)        
        fp.close()
        
        
        if self.prefix is None or self.prefix=="":
            x=random.randint(0,len(model)-1)
            t=0
            for i in model.keys():
                t=t+1
                if t==x: 
                    el=model[i]
                    self.prefix=el["#"]
                    break
  
        txt=re.sub('[^а-яА-Я ]', '', self.prefix.lower())
        #print("prefix=[{0}]".format(txt))               
        
        key = re.sub('[ ]', '_', txt)
        #print(key)
                
                    
        tl=self.prefix.split()    
        res=self.prefix    
        count=len(tl)
        while key in model.keys() and count<=int(self.length):
            el=model[key]
            nextword=el['#']
        
            if key.find("nextword", len(self.prefix))>0:
                #надо найти следующее словоб если такое уже было 
                maxnewkey=0
                for k in dict.keys():
                    if k!=nextword and el[k]>maxnewkey:
                        newkey=k
                        maxnewkey=el[k]
                nextword=newkey
                print(nextword)
        
            res=f"{res} {nextword}"
            key=nextword
            count=count+1
        print(res)
            
            
parser = argparse.ArgumentParser(description='parse key pairs into a dictionary')
#parser.add_argument("--key_pairs", dest="my_dict", action=StoreDictKeyPair, metavar="KEY1=VAL1,KEY2=VAL2...")
#args = parser.parse_args(sys.argv[1:])
#print args

parser.add_argument('model', type=str, help='путь к файлу, из которого загружается модель')
parser.add_argument('length', type=str, help='длина генерируемой последовательности')
parser.add_argument('--prefix', type=str, help='необязательный аргумент. Начало предложения (одно или несколько слов). Если не указано, выбираем начальное слово случайно из всех слов.')
args = parser.parse_args()
#print(args)

generate=mygenerate(args.model, args.prefix, args.length)
generate.generate()