# -*- coding: utf8 -*-#
import os
import argparse
import re
import sys
import pickle
import json

#"c:\dev\MyPythonPrg\Tinkoff_generate_text\data" 'my_model1'

class mytrain:    
    def __init__(self, inputdir, model, inputtext):
        self.inputdir=inputdir
        self.model=model
        self.inputtext=inputtext
        
    def fit(self):
        if self.inputtext!="":
            self.__processtext(inputtext)    
        else:            
            for filename in os.listdir(self.inputdir):
                f = os.path.join(self.inputdir, filename)
                
                if os.path.isfile(f) and filename.endswith('.txt'):
                    #print("Text file is found:", filename)        
                    
                    f = open(f, 'r')
                    txt=f.read()#.encode('utf-8'))    
                    #print("file length=[{0}]".format(len(txt)))
                    f.close()   
                    self.__processtext(txt)
                    
                    break

    def __processtext(self, txt):      
        
        txt = re.sub(r'\<[^\>]+\>', '', txt) # очистка от html форматирования
        #file(f+'_','w').write(txt)
        txt=txt.lower()

        #reg = re.compile('[^a-zA-Z ]')
        #txt=txt.replace.sub('[^а-яА-Я ]', '', txt)
        txt=re.sub('[.]', ' .', txt) #заменяем точки на пробел-точка, чтобы отделять предложения
        txt=re.sub('[\n]', ' ', txt)
        txt=re.sub('[^а-яА-Я. ]', '', txt)
        #print("txt length=[{0}]".format(len(txt)))
        
        #print(txt)     
        
        tl=txt.split()
        #print(len(tl))     
        
        model={}
        
        for i in range(len(tl)):
            if tl[i]==".": #если встретилась точка, то это конец фразы и такие сло ва не учитываем
                continue
 
            key= f"{tl[i]}"
            
            j=i+1
            while j<len(tl):# and j-i<6:
                if tl[j]==".": #если встретилась точка, то это конец фразы и такие слова не учитываем
                    break                
            
                word3=tl[j]                
                
                if key in model.keys():
                    el=model[key]                
                    if word3 in el: # если 3е слово уже есть в списке наиболее часто используемых слов после пары слов key
                        el[word3]=el[word3]+1 # уdеличиваем счетчик частоты встречаемости этого слова word3                     
                    else:
                        el[word3]=1
    
                    maxword=el['#'] # смотрим какое слово чаще всего встречалось 
                    if maxword!=word3: #если раньше лидером было другое слово xtb word3
                        if el[word3]>el[maxword]: 
                            # если частота слова лидера для пары key меньше частоты нового слова word3 то запоминаем word3
                            el['#']=word3 
                else:
                    elnew={'#': word3, word3: 1}
                    model[key]=elnew
    
                key= f"{key}_{tl[j]}"
                j=j+1
                
        
        dumpfilename = self.model#os.path.join(self.inputdir, self.model+'.pkl')
        with open(dumpfilename, 'wb') as fp:
            pickle.dump(model, fp)
        
        #json_object = json.dumps(model, indent = 4, ensure_ascii=False)#.encode('utf8')   
        #dumpfilename = os.path.join(self.inputdir, self.model+'.json')
        #with open(dumpfilename, "w") as output: #, encoding='utf-8'
        #    output.write(json_object)        
        
                
parser = argparse.ArgumentParser(description='Параметры')

parser.add_argument('model', type=str, help='Model file name')
parser.add_argument('--inputdir', type=str, help='Input dir for data files (*.txt)')
args = parser.parse_args()
#print(args)

if args.inputdir is None or args.inputdir=="":
    print("введите текст")
    inputtext=input()
else:
    inputtext=""
    
train=mytrain(args.inputdir, args.model, inputtext)
train.fit()