from typing import List, Tuple
import pymorphy2
import re
def easy_tokenizer(text):
    word = str()
    for symbol in text:
        if symbol.isalnum(): word += symbol
        elif word:
            yield word
            word = str()
    if word: yield word

PYMORPHY_CACHE = {}
MORPH = None
#hint, чтобы установка pymorphy2 не была бы обязательной
def get_lemmatizer():
    global MORPH
    if MORPH is None: MORPH = pymorphy2.MorphAnalyzer()
    return MORPH

def pymorphy_tokenizer(text):
    global PYMORPHY_CACHE
    for word in easy_tokenizer(text):
        word_hash = hash(word)
        if word_hash not in PYMORPHY_CACHE:
            PYMORPHY_CACHE[word_hash] = get_lemmatizer().parse(word)[0].normal_form        
        yield PYMORPHY_CACHE[word_hash]



morph = pymorphy2.MorphAnalyzer()
                   
class Solution:


    def __init__(self):
        pass

    def train(self, train: List[Tuple[str, dict]]) -> None:
        # fit your models here
        pass

    def predict(self, test: List[str]) -> List[dict]:
        # Do some predictions here and return results
        # Let's return empty result in proper format
       train_data = dict()
       for k in range(len(test)):
          train_data[k]=test[k].split('\n')
       for k in range(len(test)):
          train_data[k]=list(filter( lambda x: not x.isspace(), train_data[k]))
        
       train_data_parsed_n = dict()
       for k in range(len(test)):
         train_data_parsed_n[k] = [None for st in range(len(train_data[k]))]
         for st in range(len(train_data[k])):
            train_data_parsed_n[k][st] = train_data[k][st].split(' ')
            train_data_parsed_n[k][st].append(' ')
       train_data_parsed = dict()
       for k in range(len(test)):
        train_data_parsed[k] = [None for st in range(len(train_data[k]))]
        for st in range(len(train_data[k])):
           train_data_parsed[k][st] = list(pymorphy_tokenizer(train_data[k][st]))
           train_data_parsed[k][st].append(' ')
        
       months = {'январь':'01','февраль':'02','март':'03','апрель':'04','май':'05','июнь':'06','июль':'07',\
              'август':'08','сентябрь':'09','октябрь':'10','ноябрь':'11','декабрь':'12'}

       namesnew = {'федеральный':'федеральный','закон':'закон','постановление':'постановление',\
            'указ':'указ','приказ':'приказ','распоряжение':'распоряжение'}
       namesnew_n = {'ФЕДЕРАЛЬНЫЙ':'федеральный','ЗАКОН':'закон','ПОСТАНОВЛЕНИЕ':'постановление',\
            'УКАЗ':'указ','ПРИКАЗ':'приказ','РАСПОРЯЖЕНИЕ':'распоряжение'}
       weights = {'федеральный закон':6,'закон': 5,'постановление':3,\
            'указ':4,'приказ':2,'распоряжение':3}

       ans = dict()
       for k in range(len(test)):

           ans[k] = dict()
           head_weights = {'федеральный закон':0,'закон': 0,'постановление':0,\
             'указ':0,'приказ':0,'распоряжение':0}
           body_weights = {'федеральный закон':7,'закон': 7,'постановление':7,\
            'указ':7,'приказ':7,'распоряжение':7}
           for i in range(len(train_data_parsed_n[k])):
               if len(train_data_parsed_n[k][i]) and namesnew_n.get(train_data_parsed_n[k][i][0], -1) != -1:
                   if namesnew_n[train_data_parsed_n[k][i][0]] == 'федеральный' and\
                   namesnew_n.get(train_data_parsed_n[k][i][1], -1) != -1 and\
                   namesnew_n[train_data_parsed_n[k][i][1]] == 'закон' and\
                   len(train_data_parsed_n[k][i]) == 3:
                      head_weights['федеральный закон'] = weights['федеральный закон']
                   elif namesnew_n[train_data_parsed_n[k][i][0]] == 'федеральный':
                       continue
                   elif len(train_data_parsed_n[k][i]) == 2:
                      head_weights[namesnew_n[train_data_parsed_n[k][i][0]]] = weights[namesnew_n[train_data_parsed_n[k][i][0]]]
               else:
                  for j in range(len(train_data_parsed_n[k][i])):
                     if  namesnew_n.get(train_data_parsed_n[k][i][j], -1) != -1:
                        head_weights[namesnew_n[train_data_parsed_n[k][i][j]]] = weights[namesnew_n[train_data_parsed_n[k][i][j]]]       
                            
           cur_new = sorted(head_weights.items(), key=lambda x: x[1], reverse=True)
           if cur_new[0][1] == 0:            
              fin = 0
              for i in range(len(train_data_parsed_n[k])):
               #if fin == 1:
                  #break
                 for j in range(len(train_data_parsed_n[k][i])):
                  if namesnew_n.get(train_data_parsed_n[k][i][j], -1) != -1:
                     if namesnew_n[train_data_parsed_n[k][i][j]] == 'федеральный' and\
                     namesnew_n.get(train_data_parsed_n[k][i][j+1], -1) != -1 and\
                     namesnew_n[train_data_parsed_n[k][i][j+1]] == 'закон':
                       head_weights['федеральный закон'] = weights['федеральный закон']
                       fin = 1
                    #break
                     elif namesnew_n[train_data_parsed_n[k][i][j]] == 'федеральный':
                        continue
                     else:
                        head_weights[namesnew_n[train_data_parsed_n[k][i][j]]] = weights[namesnew_n[train_data_parsed_n[k][i][j]]]
                        fin = 1
                        #break
              cur_new = sorted(head_weights.items(), key=lambda x: x[1], reverse=True)
              if cur_new[0][1] == 0: 
           
                   fin = 0
                   for i in range(len(train_data_parsed[k])):
                    #if fin == 1:
                       #break
                      for j in range(len(train_data_parsed_n[k][i])):
                         if namesnew.get(train_data_parsed_n[k][i][j].lower(), -1) != -1:
                            if namesnew[train_data_parsed_n[k][i][j].lower()] == 'федеральный' and\
                            namesnew.get(train_data_parsed_n[k][i][j+1].lower(), -1) != -1 and\
                            namesnew[train_data_parsed_n[k][i][j+1].lower()] == 'закон':
                                body_weights['федеральный закон'] = weights['федеральный закон']
                                fin = 1
                                #break
                            elif namesnew[train_data_parsed_n[k][i][j].lower()] == 'федеральный':
                                continue
                            else:
                                body_weights[namesnew[train_data_parsed_n[k][i][j].lower()]] =\
                                weights[namesnew[train_data_parsed_n[k][i][j].lower()]]
                                fin = 1
                                #break
                   cur_new = sorted(body_weights.items(), key=lambda x: x[1])
                   if cur_new[0][1] == 7: 
                      fin = 0
                      for i in range(len(train_data_parsed[k])):
                        #if fin == 1:
                           #break
                        for j in range(len(train_data_parsed[k][i])):
                          if namesnew.get(train_data_parsed[k][i][j], -1) != -1:
                             if namesnew[train_data_parsed[k][i][j]] == 'федеральный' and\
                                namesnew.get(train_data_parsed[k][i][j+1], -1) != -1 and\
                                namesnew[train_data_parsed[k][i][j+1]] == 'закон':
                                body_weights['федеральный закон'] = weights['федеральный закон']
                                fin = 1
                                #break
                             elif namesnew[train_data_parsed[k][i][j]] == 'федеральный':
                                   continue
                             else:
                               body_weights[namesnew[train_data_parsed[k][i][j]]] =\
                               weights[namesnew[train_data_parsed[k][i][j]]]
                               fin = 1
                               #break
                      cur_new = sorted(body_weights.items(), key=lambda x: x[1])
                      ans[k]['type'] = cur_new[0][0]
                   else:
                    ans[k]['type'] = cur_new[0][0]
      
              else:
                ans[k]['type'] = cur_new[0][0]
           else:
                ans[k]['type'] = cur_new[0][0]
      
           if ans.get(k, -1) == -1:
             ans[k] = dict()
             ans[k]['type'] = 'закон'
           if ans[k]['type'] == 'постановление':
            found_fl = 0
            for i in range(len(train_data_parsed[k])):
                if found_fl:
                    break
                if len(train_data_parsed[k][i])  >= 2:
                    for j in range(len(train_data_parsed[k][i]) - 1):
                        if train_data_parsed[k][i][j] == 'настоящий' and train_data_parsed[k][i][j + 1] == 'закон':
                            ans[k]['type'] = 'закон'
                            found_fl = 1
                            break  
            found_fl = 1
            for i in range(len(train_data_parsed_n[k])):
                if found_fl == 0:
                    break
                for j in range(len(train_data_parsed_n[k][i]) ):
                    if train_data_parsed_n[k][i][j].find('приказываю:') != -1:
                        ans[k]['type'] = 'приказ'
                        found_fl = 0
                        break

       for k in range(len(test)):
        for i in range(len(train_data_parsed[k])):
          for j in range(len(train_data_parsed[k][i])):
            if months.get(train_data_parsed[k][i][j], -1) != -1:
                train_data_parsed[k][i][j]  = months[train_data_parsed[k][i][j]]

       num_l = dict()

       for k in range(len(test)):

          cur = dict()
          for i in range(len(train_data_parsed[k])):
             if ans[k].get('date', -1) != -1:
                break
             if len(train_data_parsed[k][i]) >= 4 and len(train_data_parsed[k][i - 1]) <= 4:
                if train_data_parsed[k][i][0] == 'от' and train_data_parsed[k][i][1].isnumeric() and\
                train_data_parsed[k][i][2].isnumeric() and (train_data_parsed[k][i][3].isnumeric()\
                or train_data_parsed[k][i][3][:-1].isnumeric() and train_data_parsed[k][i][3][-1] == 'г'):
                   if train_data_parsed[k][i][3][:-1].isnumeric() and train_data_parsed[k][i][3][-1] == 'г':
                       train_data_parsed[k][i][3] = train_data_parsed[k][i][3][:-1]
                   if int(train_data_parsed[k][i][1]) > 0 and  int(train_data_parsed[k][i][1]) < 33 \
                   and int(train_data_parsed[k][i][2]) > 0 and  int(train_data_parsed[k][i][2]) <= 12 \
                   and int(train_data_parsed[k][i][3]) > 1990 and  int(train_data_parsed[k][i][3]) < 2022:
                       ans[k]['date'] = train_data_parsed[k][i][1] + '.' +\
                       train_data_parsed[k][i][2] +'.' + train_data_parsed[k][i][3]
                       num_l[k] = dict()
                       num_l[k]['pos'] = i
                       num_l[k]['year'] =  train_data_parsed[k][i][3]
           
             if len(train_data_parsed[k][i]) >= 3  and len(train_data_parsed[k][i - 1]) <= 4:
                if  train_data_parsed[k][i][0].isnumeric() and\
                train_data_parsed[k][i][1].isnumeric() and (train_data_parsed[k][i][2].isnumeric()\
                or train_data_parsed[k][i][2][:-1].isnumeric() and train_data_parsed[k][i][2][-1] == 'г'):
                   if train_data_parsed[k][i][2][:-1].isnumeric() and train_data_parsed[k][i][2][-1] == 'г':
                       train_data_parsed[k][i][2] = train_data_parsed[k][i][2][:-1]
                   if int(train_data_parsed[k][i][0]) > 0 and  int(train_data_parsed[k][i][0]) < 33 \
                   and int(train_data_parsed[k][i][1]) > 0 and  int(train_data_parsed[k][i][1]) <= 12 \
                   and int(train_data_parsed[k][i][2]) > 1990 and  int(train_data_parsed[k][i][2]) < 2022:
                      ans[k]['date'] = train_data_parsed[k][i][0] + '.' +\
                      train_data_parsed[k][i][1] +'.' + train_data_parsed[k][i][2]
                      num_l[k] = dict()
                      num_l[k]['pos'] = i
                      num_l[k]['year'] =  train_data_parsed[k][i][2]

            
        
          for i in range(len(train_data_parsed[k]) - 2, len(train_data_parsed[k])-10, -1): 
              if len(train_data_parsed[k][i]) >= 4 and len(train_data_parsed[k][i - 1]) <= 4 \
              and train_data_parsed[k][i + 1][0].isnumeric():
                 if train_data_parsed[k][i][0] == 'от' and train_data_parsed[k][i][1].isnumeric() and\
                 train_data_parsed[k][i][2].isnumeric() and (train_data_parsed[k][i][3].isnumeric()\
                 or train_data_parsed[k][i][3][:-1].isnumeric() and train_data_parsed[k][i][3][-1] == 'г'):
                   if train_data_parsed[k][i][3][:-1].isnumeric() and train_data_parsed[k][i][3][-1] == 'г':
                       train_data_parsed[k][i][3] = train_data_parsed[k][i][3][:-1]
                   if int(train_data_parsed[k][i][1]) > 0 and  int(train_data_parsed[k][i][1]) < 33 \
                   and int(train_data_parsed[k][i][2]) > 0 and  int(train_data_parsed[k][i][2]) <= 12 \
                   and int(train_data_parsed[k][i][3]) > 1990 and  int(train_data_parsed[k][i][3]) < 2022:
                     ans[k]['date'] = train_data_parsed[k][i][1] + '.' +\
                     train_data_parsed[k][i][2] +'.' + train_data_parsed[k][i][3]
                     num_l[k] = dict()

                     num_l[k]['pos'] = i
                     num_l[k]['year'] =  train_data_parsed[k][i][3]

                     break
             
              if len(train_data_parsed[k][i]) >= 3  and len(train_data_parsed[k][i - 1]) <= 4 \
              and train_data_parsed[k][i + 1][0].isnumeric():
                if  train_data_parsed[k][i][0].isnumeric() and\
                train_data_parsed[k][i][1].isnumeric() and (train_data_parsed[k][i][2].isnumeric()\
                or train_data_parsed[k][i][2][:-1].isnumeric() and train_data_parsed[k][i][2][-1] == 'г'):
                   if train_data_parsed[k][i][2][:-1].isnumeric() and train_data_parsed[k][i][2][-1] == 'г':
                       train_data_parsed[k][i][2] = train_data_parsed[k][i][2][:-1]
                   if int(train_data_parsed[k][i][0]) > 0 and  int(train_data_parsed[k][i][0]) < 33 \
                   and int(train_data_parsed[k][i][1]) > 0 and  int(train_data_parsed[k][i][1]) <= 12 \
                   and int(train_data_parsed[k][i][2]) > 1990 and  int(train_data_parsed[k][i][2]) < 2022:
                      ans[k]['date'] = train_data_parsed[k][i][0] + '.' +\
                      train_data_parsed[k][i][1] +'.' + train_data_parsed[k][i][2]
                      num_l[k] = dict()

                      num_l[k]['pos'] = i
                      num_l[k]['year'] =  train_data_parsed[k][i][2]

                      break
            
          if ans[k].get('date', -1) == -1:
             for i in range(len(train_data_parsed[k]) - 1, -1, -1): 
                if ans[k].get('date', -1) != -1:
                    break
                if len(train_data_parsed[k][i]) >= 4:
                    if train_data_parsed[k][i][0] == 'от' and train_data_parsed[k][i][1].isnumeric() and\
                    train_data_parsed[k][i][2].isnumeric() and train_data_parsed[k][i][3].isnumeric():
                        if int(train_data_parsed[k][i][1]) > 0 and  int(train_data_parsed[k][i][1]) < 33 \
                        and int(train_data_parsed[k][i][2]) > 0 and  int(train_data_parsed[k][i][2]) <= 12 \
                        and int(train_data_parsed[k][i][3]) > 1990 and  int(train_data_parsed[k][i][3]) < 2022:
                           ans[k]['date'] = train_data_parsed[k][i][1] + '.' +\
                           train_data_parsed[k][i][2] +'.' + train_data_parsed[k][i][3]
                           num_l[k] = dict()
                           num_l[k]['pos'] = i
                           num_l[k]['year'] =  train_data_parsed[k][i][3]
        

                if len(train_data_parsed[k][i]) >= 3:
                    if  train_data_parsed[k][i][0].isnumeric() and\
                    train_data_parsed[k][i][1].isnumeric() and train_data_parsed[k][i][2].isnumeric():
                       if int(train_data_parsed[k][i][0]) > 0 and  int(train_data_parsed[k][i][0]) < 33 \
                       and int(train_data_parsed[k][i][1]) > 0 and  int(train_data_parsed[k][i][1]) <= 12 \
                       and int(train_data_parsed[k][i][2]) > 1990 and  int(train_data_parsed[k][i][2]) < 2022:
                          ans[k]['date'] = train_data_parsed[k][i][0] + '.' +\
                          train_data_parsed[k][i][1] +'.' + train_data_parsed[k][i][2]
                          num_l[k] = dict()
                          num_l[k]['pos'] = i
                          num_l[k]['year'] =  train_data_parsed[k][i][2]

                  
          if ans[k].get('date', -1) == -1:
              for i in range(len(train_data_parsed[k])):
                 if ans[k].get('date', -1) != -1:
                     break
                 for j in range(len(train_data_parsed[k][i]) - 2):
                    if  train_data_parsed[k][i][j].isnumeric() and\
                    train_data_parsed[k][i][j + 1].isnumeric() and train_data_parsed[k][i][j + 2].isnumeric():
                        if int(train_data_parsed[k][i][j]) > 0 and  int(train_data_parsed[k][i][j]) < 33 \
                        and int(train_data_parsed[k][i][j + 1]) > 0 and  int(train_data_parsed[k][i][j + 1]) <= 12 \
                        and int(train_data_parsed[k][i][j + 2]) > 1990 and  int(train_data_parsed[k][i][j + 2]) < 2022:
                           ans[k]['date'] = train_data_parsed[k][i][j] + '.' +\
                           train_data_parsed[k][i][j + 1] +'.' + train_data_parsed[k][i][j + 2]
                           num_l[k] = dict()
                           num_l[k]['pos'] = i
                           num_l[k]['year'] =  train_data_parsed[k][i][j + 2]

                           break

       for k in range(len(test)):
          for j in range(len(train_data_parsed_n[k])):
             for i in  range(len(train_data_parsed_n[k][j])):
                train_data_parsed_n[k][j][i] = train_data_parsed_n[k][j][i].replace('_','')     
            
       def hasNumbers(inputString):
         return any(char.isdigit() for char in inputString)
        
       for k in range(len(test)):
           j = num_l[k]['pos'] - 1
        #print('aaaa ',j)
           if j == -1:
              j = 0
           fl = 0
           fin = 0
           h = 0
           while h < 2:
              i = 0
              if fin == 1:
                 break
              if len(train_data_parsed_n[k][j]) == 2 and train_data_parsed_n[k][j][0] ==''and train_data_parsed_n[k][j][1] ==' ':
                   j += 1
                   continue
              if j == len(train_data_parsed_n[k]):
                  break
              while i < len(train_data_parsed_n[k][j]):
                  if len(train_data_parsed_n[k][j][i]) == 0:
                      i += 1
                      continue
                  if fl == 0 and (train_data_parsed_n[k][j][i] == '№'or train_data_parsed_n[k][j][i] == 'N'):
                     fl = 1
                     i += 1
                     continue
                  elif fl == 0 and train_data_parsed_n[k][j][i][0] == '№':
                      if hasNumbers(train_data_parsed_n[k][j][i]):
                         if  '.' in train_data_parsed_n[k][j][i]:
                            i += 1
                            continue
          
                         ans[k]['number'] = train_data_parsed_n[k][j][i][1:]
                         ans[k]['number'] = ''.join(list(filter(lambda x: x.isnumeric() or (x >= 'а' and x <= 'я') or\
                                                           (x >= 'А' and x <= 'Я') \
                                                  or x == '-' or x == '/', ans[k]['number'] )))

                         ans[k]['number'] = ans[k]['number'].lower() 
                         fl = 1
                         fin = 1
                         break
           
                  elif fl == 1 and hasNumbers(train_data_parsed_n[k][j][i][0]):
                    if  '.' in train_data_parsed_n[k][j][i]:
                        i += 1
                        continue
                    ans[k]['number'] = train_data_parsed_n[k][j][i]
                    ans[k]['number'] = ''.join(list(filter(lambda x: x.isnumeric() or (x >= 'а' and x <= 'я') or (x >= 'А' and x <= 'Я') \
                                              or x == '-' or x == '/', ans[k]['number'] )))
           
                    ans[k]['number'] = ans[k]['number'].lower()      
                    fin = 1
                    break
                  elif fl == 1 and len(train_data_parsed_n[k][j][i]) > 1:
                    if hasNumbers(train_data_parsed_n[k][j][i]):
                        ans[k]['number'] = train_data_parsed_n[k][j][i][1:]
                        ans[k]['number'] = ''.join(list(filter(lambda x: x.isnumeric() or (x >= 'а' and x <= 'я') or (x >= 'А' and x <= 'Я') \
                                                  or x == '-' or x == '/', ans[k]['number'] )))

                        ans[k]['number'] = ans[k]['number'].lower()      
                        fin = 1
                        break
                  i += 1
              j += 1
              h += 1
           if ans[k].get('number', -1) == -1:
               j = num_l[k]['pos'] 
               fl = 0
               h = min(num_l[k]['pos'] + 2, len(train_data_parsed_n[k]))

               while j < h:
                   i = 0
                   if fin == 1:
                     break
                   while i < len(train_data_parsed_n[k][j]):
                       if fl == 0 and train_data_parsed_n[k][j][i].find(num_l[k]['year']) != -1:
                           fl = 1
                           i += 1
                           continue
                       if len(train_data_parsed_n[k][j][i]) == 0:
                          i += 1
                          continue
                       elif fl == 1 and hasNumbers(train_data_parsed_n[k][j][i]):
       
                          ans[k]['number'] = train_data_parsed_n[k][j][i]
                          ans[k]['number'] = ''.join(list(filter(lambda x: x.isnumeric() or (x >= 'а' and x <= 'я') or (x >= 'А' and x <= 'Я') \
                                              or x == '-' or x == '/', ans[k]['number'] )))
                   
                          ans[k]['number'] = ans[k]['number'].lower()
                          break
                       i += 1
                   j += 1   
            
           if ans[k].get('number', -1) == -1:
               j = num_l[k]['pos'] 

               while j < len(train_data_parsed_n[k]):
                   if fin == 1:
                      break
                   if train_data_parsed_n[k][j][0] == '№' or train_data_parsed_n[k][j][0] == 'N':
                       i = 1
                       while i <  len(train_data_parsed_n[k][j]):
                          if len(train_data_parsed_n[k][j][i]) == 0:
                             i += 1
                             continue
                          if hasNumbers(train_data_parsed_n[k][j][i]):
                            ans[k]['number'] = train_data_parsed_n[k][j][i]
                            ans[k]['number'] = ''.join(list(filter(lambda x: x.isnumeric() or (x >= 'а' and x <= 'я') or (x >= 'А' and x <= 'Я') \
                                                      or x == '-' or x == '/', ans[k]['number'] )))
                            ans[k]['number'] = ans[k]['number'].lower()
                            fin = 1
                            break
                          i += 1
                   j += 1  
           if ans[k].get('number', -1) == -1:
      
              j = num_l[k]['pos'] +1
              while j < len(train_data_parsed_n[k]):
                 if fin == 1:
                    break
                 if len(train_data_parsed_n[k][j][0]) > 0:
                     if hasNumbers(train_data_parsed_n[k][j][0]):
                        ans[k]['number'] = train_data_parsed_n[k][j][0]
                        ans[k]['number'] = ''.join(list(filter(lambda x: x.isnumeric() or (x >= 'а' and x <= 'я') or (x >= 'А' and x <= 'Я') \
                                                        or x == '-' or x == '/', ans[k]['number'] )))
                        ans[k]['number'] = ans[k]['number'].lower()
                        fin = 1
                        break
                 j += 1   
           if ans[k].get('number', -1) == -1:
               ans[k]['number'] = 'egg'
      
           ans[k]['number'] = ans[k]['number'].replace('0п', 'пп')
           ans[k]['number'] = ans[k]['number'].replace('п0', 'пп')

           ans[k]['number'] = ans[k]['number'].replace('ппп','пп')
           if ans[k]['number'].find('кз') != -1:
               ans[k]['number'] = ans[k]['number'][:ans[k]['number'].find('кз')  + 2]
           if ans[k]['number'].find('оз') != -1:
               ans[k]['number'] = ans[k]['number'][:ans[k]['number'].find('оз')  + 2]
           if ans[k]['number'].find('-пп') != -1:
              if ans[k]['number'][:4].isnumeric():
                 if int(ans[k]['number'][:4]) >= 2000 and int(ans[k]['number'][:4]) < 3000:
                    ans[k]['number'] = ans[k]['number'][1:]
           ll = -1
           for i in range(1, len(ans[k]['number']) - 2):
              if ans[k]['number'][i].upper() != ans[k]['number'][i].lower() \
              and ans[k]['number'][i + 1].upper() != ans[k]['number'][i + 1].lower() \
              and ans[k]['number'][i + 2].upper() != ans[k]['number'][i + 2].lower() \
              and ans[k]['number'][i - 1].isnumeric():
                  ll = i
           if ll != -1:
              ans[k]['number'] = ans[k]['number'][:ll]   
        
       for k in range(len(test)):
          found_fl = 0
          for i in range(len(train_data_parsed_n[k])):
             if found_fl == 1:
                break
             if train_data_parsed_n[k][i][0] == 'О' or train_data_parsed_n[k][i][0] == 'Об' \
             or train_data_parsed_n[k][i][0] == 'Вопросы' or train_data_parsed_n[k][i][0] == '©О' \
             or train_data_parsed_n[k][i][0] == '©Об' or train_data_parsed_n[k][i][0] == '`О' \
             or  train_data_parsed_n[k][i][0] == "'Об" or train_data_parsed_n[k][i][0] == '"Об'\
             or  train_data_parsed_n[k][i][0] == "ОБ" or  train_data_parsed_n[k][i][0] == "об"\
             or train_data_parsed_n[k][i][0] == '"О'  :
                ans[k]['name'] = train_data_parsed_n[k][i]
                m = i + 1
                found_fl = 1
                while train_data_parsed_n[k][m][0] != '':
                    tmp = morph.parse(train_data_parsed_n[k][m][0])[0]
                    #if tmp.tag.POS == 'NOUN':
                    #if tmp.tag.case == 'nomn':
                        #break
                    #if tmp.tag.POS == 'VERB' or tmp.tag.POS == 'INFN':
                       #break
                    if  tmp.tag.POS == 'INFN':
                        break
                    ans[k]['name'] = ans[k]['name'] + train_data_parsed_n[k][m]
                    m += 1
                    if m == len(train_data_parsed_n[k]):
                        break
          if ans[k].get('name', -1) == -1:
               found_fl = 0
               for i in range(len(train_data_parsed_n[k])):
                   if found_fl == 1:
                       break
                   for t in range(len(train_data_parsed_n[k][i])):
                      if train_data_parsed_n[k][i][t] == 'О' or train_data_parsed_n[k][i][t] == 'Об' \
                      or train_data_parsed_n[k][i][t] == 'Вопросы' or train_data_parsed_n[k][i][t] == '©О' \
                      or train_data_parsed_n[k][i][t] == '©Об' or train_data_parsed_n[k][i][t] == '`О' \
                      or  train_data_parsed_n[k][i][t] == "'Об" or train_data_parsed_n[k][i][t] == '"Об'\
                      or  train_data_parsed_n[k][i][t] == "ОБ"  or train_data_parsed_n[k][i][t] == '"О' :
                          ans[k]['name'] = train_data_parsed_n[k][i][t:]
                          m = i + 1
                          found_fl = 1
                          while train_data_parsed_n[k][m][0] != '':
                             tmp = morph.parse(train_data_parsed_n[k][m][0])[0]
                             #if tmp.tag.POS == 'NOUN':
                             #if tmp.tag.case == 'nomn':
                                #break
                             if  tmp.tag.POS == 'INFN':
                                 break
                             ans[k]['name'] = ans[k]['name'] + train_data_parsed_n[k][m]
                             m += 1
                             if m == len(train_data_parsed_n[k]):
                               break
          if ans[k].get('name', -1) == -1:
              found_fl = 0
              for j in range(4, 0, -1): 
                 co = 0
                 if found_fl == 1:
                    break  
                 for i in range(len(train_data_parsed_n[k])):
                     if found_fl == 1:
                         break  
                     if train_data_parsed_n[k][i][0] == '':
                         co += 1
                         continue
                     if co == j:
                        ans[k]['name'] = train_data_parsed_n[k][i]
                        m = i + 1
                        found_fl = 1
                        while train_data_parsed_n[k][m][0] != '':
                           tmp = morph.parse(train_data_parsed_n[k][m][0])[0]
                           #if tmp.tag.POS == 'NOUN':
                           #if tmp.tag.case == 'nomn':
                                #break
                           #if tmp.tag.POS == 'VERB' or tmp.tag.POS == 'INFN':
                            #break
                           ans[k]['name'] = ans[k]['name'] + train_data_parsed_n[k][m]
                           m += 1
                        if m == len(train_data_parsed_n[k]):
                           break
          if ans[k].get('name', -1) == -1:                         
                ans[k]['name'] = 'Об'
                           
       for k in range(len(test)):
          ans[k]['name'] = list(filter(lambda x:x !='' and x != ' ', ans[k]['name']))
          ans[k]['name'] = ' '.join(ans[k]['name'])
          if ans[k]['name'][-1] == '"':
             ans[k]['name'] =  ans[k]['name'][:-1] 
          if ans[k]['name'][0] == '©' or ans[k]['name'][0] == '"' or ans[k]['name'][0] == '`' or ans[k]['name'][0] == "'":
             ans[k]['name'] =  ans[k]['name'][1:] 

       subjects = ['города', 'области','края','округа','федерации','района', 'республики','г.','обл.']
       rulers = ['мэр','глава','совет','собрание','президент','губернатор', 'правительство','служба','дума', 'управление','министр','администрация','совет',                               'конституционный','кабинет','комитет','министерство','департамент','агентство']
       con_sub = ['города','г.','республики']
       regex = re.compile('[^а-яА-Я\-]')

       for k in  range(len(test)):


           found_fl = 0
           for i in range(0, len(train_data_parsed_n[k])):
               if  found_fl == 1:
                 break
               if regex.sub('',train_data_parsed_n[k][i][0].lower()) == 'принят':
                   tmp_ans = []
                   a = i
                   b = 1
                   while a < i + 2:
                     if b == len(train_data_parsed_n[k][a]):
                        a = a + 1
                        b = 0
                     if a  == len(train_data_parsed_n[k]):
                                break
                     if train_data_parsed_n[k][a][b].lower() == 'думой':
                                found_fl = 1
                                tmp_ans.append(train_data_parsed_n[k][a][b].lower())
                                ans[k]['authority'] = tmp_ans
                                b = b + 1
                                if len(ans[k]['authority']) <= 2:
                                    while a < len(train_data_parsed_n[k]):
                                        if b == len(train_data_parsed_n[k][a]):
                                            a = a + 1
                                            b = 0
                                        if a  == len(train_data_parsed_n[k]):
                                            break
                                        if train_data_parsed_n[k][a][b].lower()  in subjects:
                                            ans[k]['authority'].append( train_data_parsed_n[k][a][b])
                                            break
                                        if train_data_parsed_n[k][a][b] != '' and train_data_parsed_n[k][a][b] != ' ':
                                            tmp_ans.append(train_data_parsed_n[k][a][b])
                                        b = b + 1
                                        
                                break
                     if train_data_parsed_n[k][a][b].lower()  == 'собранием':
                        found_fl = 1
                        tmp_ans.append('собрание')
                        tmp_ans.append(train_data_parsed_n[k][a][b + 1].lower())
                        #tmp_ans.append(train_data_parsed_n[k][a][b + 2].lower())

                        ans[k]['authority'] = tmp_ans
                        break
                    
                     if train_data_parsed_n[k][a][b].lower()  == 'советом':
                        found_fl = 1
                        tmp_ans.append('совет')
                        lim = 2
                        b = b + 1
                        while lim > 0:
                            if b == len(train_data_parsed_n[k][a]):
                                a = a + 1
                                b = 0
                                if a  == len(train_data_parsed_n[k]):
                                    break 
                            if train_data_parsed_n[k][a][b] != '' and train_data_parsed_n[k][a][b] != ' ':
                                tmp_ans.append(train_data_parsed_n[k][a][b])
                                lim = lim - 1
                            b = b + 1

                        ans[k]['authority'] = tmp_ans
                        break
                            
                     if train_data_parsed_n[k][a][b] != '' and train_data_parsed_n[k][a][b] != ' ':
                        tmp_ans.append(train_data_parsed_n[k][a][b])
                     b = b + 1

           if ans[k].get('authority', -1) == -1:

             for i in range(0, len(train_data_parsed_n[k])):
                if  found_fl == 1:
                    break
                for j in range(0,len(train_data_parsed_n[k][i]) , 1):
                    if found_fl == 1:
                        break
                    if morph.parse(regex.sub('',train_data_parsed_n[k][i][j].lower()))[0].normal_form in rulers\
                    and train_data_parsed_n[k][i][j].upper() == train_data_parsed_n[k][i][j]:
                       
                        t = 5
                        if train_data_parsed_n[k][i][j].lower() == 'комитет' or train_data_parsed_n[k][i][j].lower() == 'департамент'\
                        or train_data_parsed_n[k][i][j].lower() == 'агентство':
                            t = 10
                        a = i
                        b = j + 1
                        tmp_ans = [ train_data_parsed_n[k][i][j]]
                        if train_data_parsed_n[k][i][j].lower() == 'совет' or train_data_parsed_n[k][i][j].lower() == 'дума':
                             tmp_ans =  train_data_parsed_n[k][i][:j + 1]
                        while a <len(train_data_parsed_n[k]) and t > 0:
                            if b == len(train_data_parsed_n[k][a]):
                                    a = a + 1
                                    b = 0    
                            if a  == len(train_data_parsed_n[k]):
                                break
                            if train_data_parsed_n[k][a][b].lower()  in subjects\
                            and  train_data_parsed_n[k][a][b] ==  train_data_parsed_n[k][a][b].upper():
                                found_fl = 1
                                tmp_ans.append(train_data_parsed_n[k][a][b].lower())
                                if train_data_parsed_n[k][a][b].lower() in con_sub:
                                    tmp_ans.append(train_data_parsed_n[k][a][b + 1].lower())
                                ans[k]['authority'] = tmp_ans
                                break
                            else:
                                if namesnew_n.get(train_data_parsed_n[k][a][b], -1) != -1 :
                                    found_fl = 1
                                    ans[k]['authority'] = tmp_ans
                                    break
                                if train_data_parsed_n[k][a][b] != '' and train_data_parsed_n[k][a][b] != ' ':
                                    tmp_ans.append(train_data_parsed_n[k][a][b])
                                    t -= 1
                                if train_data_parsed_n[k][a][b] !=  train_data_parsed_n[k][a][b].upper():
                                    break
                            b += 1
                        if t == 0 or a == len(train_data_parsed_n[k]):
                            break
                        if ans[k].get('authority',-1) != -1:
                            if any( (len(x) <= 1 and x != '' and x != 'и' and x.isalpha())or morph.parse(x)[0].tag.POS == 'VERB' or morph.parse(x)[0].tag.POS == 'INFN'\
                                  for x in  list(filter(lambda x: x != '' and x != ' ',ans[k]['authority'])))\
                               or len(list(filter(lambda x: x != '' and x != ' ',ans[k]['authority']))) <= 2 \
                               or not any( morph.parse(x.lower())[0].normal_form in rulers for x in ans[k]['authority']):
                                   
                                    found_fl = 0
                                    del ans[k]['authority']
                                    break

           if ans[k].get('authority', -1) == -1:

             for i in range(0, len(train_data_parsed_n[k])):
                if  found_fl == 1:
                    break
                for j in range(0,len(train_data_parsed_n[k][i]) , 1):
                    if found_fl == 1:
                        break
                    if morph.parse(regex.sub('',train_data_parsed_n[k][i][j].lower()))[0].normal_form in rulers:
                       
                        t = 5
                        if train_data_parsed_n[k][i][j].lower() == 'комитет' or train_data_parsed_n[k][i][j].lower() == 'департамент'\
                        or train_data_parsed_n[k][i][j].lower() == 'агентство':
                            #print('aaaaa')
                            t = 10
                        a = i
                        b = j + 1
                        tmp_ans = [ train_data_parsed_n[k][i][j]]
                        if train_data_parsed_n[k][i][j].lower() == 'совет' or train_data_parsed_n[k][i][j].lower() == 'дума':
                             #print('tt ',k)
                             tmp_ans =  train_data_parsed_n[k][i][:j + 1]
                        while a <len(train_data_parsed_n[k]) and t > 0:
                            if b == len(train_data_parsed_n[k][a]):
                                    a = a + 1
                                    b = 0    
                            if a  == len(train_data_parsed_n[k]):
                                break
                            if train_data_parsed_n[k][a][b].lower()  in subjects:
                                found_fl = 1
                                tmp_ans.append(train_data_parsed_n[k][a][b].lower())
                                if train_data_parsed_n[k][a][b].lower() in con_sub:
                                    tmp_ans.append(train_data_parsed_n[k][a][b + 1].lower())
                                ans[k]['authority'] = tmp_ans
                                break
                            else:
                                if namesnew.get(train_data_parsed_n[k][a][b].lower(), -1) != -1 :
                                    found_fl = 1
                                    ans[k]['authority'] = tmp_ans
                                    break
                                if train_data_parsed_n[k][a][b] != '' and train_data_parsed_n[k][a][b] != ' ':
                                    tmp_ans.append(train_data_parsed_n[k][a][b])
                                    t -= 1    
                            b += 1
                        if t == 0 or a == len(train_data_parsed_n[k]):
                            break
                 
                        if any( (len(x) <= 1 and x != '' and x != 'и' and x.isalpha())or morph.parse(x)[0].tag.POS == 'VERB' or morph.parse(x)[0].tag.POS == 'INFN'\
                              for x in  list(filter(lambda x: x != '' and x != ' ',ans[k]['authority'])))\
                           or len(list(filter(lambda x: x != '' and x != ' ',ans[k]['authority']))) <= 2 \
                           or not any( morph.parse(x.lower())[0].normal_form in rulers for x in ans[k]['authority']):
                                #print(k)
                                #print(ans[k]['authority'])
                                found_fl = 0
                                del ans[k]['authority']
                                break
           if ans[k].get('authority', -1) == -1:
               qq = max(0, len(train_data_parsed_n[k])-10)
               for i in range(len(train_data_parsed_n[k]) -1,qq, -1):
                  if  found_fl == 1:
                     break
                  if len(train_data_parsed_n[k][i]):
                     continue
                  for j in range(len(train_data_parsed_n[k][i]) -1, -1, -1):
                       if found_fl == 1:
                           break
                       if train_data_parsed_n[k][i][j].lower() in subjects or morph.parse(train_data_parsed_n[k][i][j])[0].normal_form== 'дума':
                           found_fl = 1
                           if train_data_parsed_n[k][i][j] =='г.' or train_data_parsed_n[k][i][j] =='города'\
                           or train_data_parsed_n[k][i][j] == 'республики':
                               ans[k]['authority'] = train_data_parsed_n[k][i][:j + 2]
                           else:
                               ans[k]['authority'] = train_data_parsed_n[k][i][:j + 1]
                           if len(list(filter(lambda x: x != '' and x != ' ',ans[k]['authority']))) <= 2 :
                                t = 0
                                p = i
                                while p >= 0 and t < 1:
                                   if len(train_data_parsed_n[k][p]) > 2:
                                      if train_data_parsed_n[k][p][0].isalpha():
                                         ans[k]['authority'] += train_data_parsed_n[k][p]
                                         t += 1
                                   p -= 1
                    
                           if  any( len(x) <= 1 or morph.parse(x)[0].tag.POS == 'VERB' or morph.parse(x)[0].tag.POS == 'INFN'\
                           or not x.isalpha()  for x in  list(filter(lambda x: x != '' and x != ' ',ans[k]['authority'])))\
                           or len(list(filter(lambda x: x != '' and x != ' ',ans[k]['authority']))) <= 2\
                           or not any( morph.parse(x.lower())[0].normal_form in rulers for x in ans[k]['authority']):
                        
                             found_fl = 0
                             del ans[k]['authority']
                             break
                                
           if ans[k].get('authority', -1) == -1:

              for i in range(0, len(train_data_parsed_n[k])):
                   if  found_fl == 1:
                       break
   
                   for j in range(len(train_data_parsed_n[k][i]) -1, -1, -1):
                      if found_fl == 1:
                        break
                      if train_data_parsed_n[k][i][j].lower() in subjects  or morph.parse(train_data_parsed_n[k][i][j])[0].normal_form== 'дума':
                        found_fl = 1
                        if train_data_parsed_n[k][i][j] =='г.' or train_data_parsed_n[k][i][j] =='города'\
                        or train_data_parsed_n[k][i][j] == 'республики':
                            ans[k]['authority'] = train_data_parsed_n[k][i][:j + 2]
                        else:
                            ans[k]['authority'] = train_data_parsed_n[k][i][:j + 1]
                        m = i + 1
                        while m < 10:
                           if len(train_data_parsed_n[k][m]) <= 4:
                               ans[k]['authority'] = train_data_parsed_n[k][m] + ans[k]['authority']
                           else:
                              break
                           m = m + 1
                        if  any( len(x) <= 1 or morph.parse(x)[0].tag.POS == 'VERB' or morph.parse(x)[0].tag.POS == 'INFN'\
                        or not x.isalpha()    for x in  list(filter(lambda x: x != '' and x != ' ',ans[k]['authority'])))\
                        or len(list(filter(lambda x: x != '' and x != ' ',ans[k]['authority']))) <= 2\
                        or not any( morph.parse(x.lower())[0].normal_form in rulers for x in ans[k]['authority']):
                            found_fl = 0
                            del ans[k]['authority']
                            break
                            
           if ans[k].get('authority', -1) == -1:

             for i in range(0, len(train_data_parsed_n[k])):
                if  found_fl == 1:
                  break
                for j in range(len(train_data_parsed_n[k][i])):
                   if  found_fl == 1:
                       break
                   if morph.parse(train_data_parsed_n[k][i][j])[0].normal_form in rulers and\
                   train_data_parsed_n[k][i][j] == train_data_parsed_n[k][i][j].upper():
                      ans[k]['authority'] =  train_data_parsed_n[k][i]
                      found_fl = 1
                      if i > 0:
                        if train_data_parsed_n[k][i-1][0].upper() == train_data_parsed_n[k][i-1][0]\
                        and regex.sub('',train_data_parsed_n[k][i-1][0]) != '' and\
                        namesnew_n.get(train_data_parsed_n[k][i-1][0], -1) == -1:
                            ans[k]['authority'] = train_data_parsed_n[k][i-1] + ans[k]['authority'] 
                      if i < len( train_data_parsed_n[k])-1:
                        if train_data_parsed_n[k][i+1][0].upper() == train_data_parsed_n[k][i+1][0]\
                        and regex.sub('',train_data_parsed_n[k][i+1][0]) != '' and\
                        namesnew_n.get(train_data_parsed_n[k][i+1][0], -1) == -1:
                            ans[k]['authority'] = ans[k]['authority'] + train_data_parsed_n[k][i+1] 
                            
           if ans[k].get('authority', -1) == -1:

             for i in range(0, len(train_data_parsed_n[k])):
               if  found_fl == 1:
                break
               for j in range(len(train_data_parsed_n[k][i])):
                 if  found_fl == 1:
                    break
           
                 if morph.parse(train_data_parsed_n[k][i][j].lower())[0].normal_form in rulers:
                    if j > 0:
                        ans[k]['authority'] =  train_data_parsed_n[k][i][j - 1: j + 2]
                    else:
                        ans[k]['authority'] =  train_data_parsed_n[k][i][j : j + 2]

                    found_fl = 1
           if ans[k].get('authority', -1) == -1:
               ans[k]['authority'] = ['президент','путин']

       bad_pos = ['VERB', 'INFN']   
       regex1 = re.compile('ои')
       for k in  range(len(test)):

          for t in range(len(ans[k]['authority'])):
             ans[k]['authority'][t] = regex.sub('',  ans[k]['authority'][t])

          ans[k]['authority'] = list(filter(lambda x:x !='' and x != ' ' and  morph.parse(x.lower())[0].tag.POS not in bad_pos\
                                      and x.lower() != 'тогтавр' and x.lower() != 'уласай'\
                                      and months.get(morph.parse(x.lower())[0].normal_form, -1) == -1 and\
                                      morph.parse(x.lower())[0].normal_form != 'год', ans[k]['authority']))
   
          ans[k]['authority'][0] = morph.parse( ans[k]['authority'][0])[0].normal_form  
          for t in range(len(ans[k]['authority'])):
              ans[k]['authority'][t] = regex1.sub('ой',ans[k]['authority'][t].lower())
              if  ans[k]['authority'][t].lower() == 'суда':
                  ans[k]['authority'][t] = 'суд'
          if morph.parse( ans[k]['authority'][-1])[0].normal_form == 'дума':
            for s in range(len( ans[k]['authority']) - 1):
                ans[k]['authority'][s] =  morph.parse( ans[k]['authority'][s])[0].normal_form
                ans[k]['authority'][s] = ans[k]['authority'][s][:-2] + 'ая'
            ans[k]['authority'][-1] =  morph.parse( ans[k]['authority'][-1])[0].normal_form
          if ans[k]['authority'][0] == 'законодательный' and ans[k]['authority'][1] == 'собрание':
            ans[k]['authority'][0] = 'законодательное'
          ans[k]['authority'] = ' '.join(ans[k]['authority'])
    
       for q in  range(len(test)):
         if ans[q]['authority'].find('государственный думой') != -1:
             ans[q]['authority'] = 'Государственная Дума Федерального собрания Российской Федерации'

         if ans[q]['authority'] == 'государственный совет - хасэ':
            ans[q]['authority'] = 'Государственный Совет - Хасэ Республики Адыгея'
    
         if  ans[q]['authority'].find('ханты-мансийского автономного округа') != -1:
             ans[q]['authority'] =  ans[q]['authority'] +' - Югры'
             
       for q in  range(len(test)):
         if ans[q]['authority'].find('собрание') ==0:
             ans[q]['authority'] = 'законодательное ' + ans[q]['authority']   
           
       results = []
       for k in range(len(test)):
            prediction = {"type": "",
                          "date": "",
                          "number": "",
                          "authority": "",
                          "name": ""}
            prediction['type'] = ans[k]['type']
            prediction['date'] = ans[k]['date']
            prediction['number'] = ans[k]['number']
            prediction['name'] = ans[k]['name']
            prediction['authority'] = ans[k]['authority']
            results.append(prediction)
       return results
        
        
        
import os

#directory = os.fsencode('../oot/tpc2020train/train/txts/')
#trainn_data = []
#names = []
#for file in os.listdir(directory):
    #with open('../oot/tpc2020train/train/txts/' + file.decode('utf-8')) as f:
        #trainn_data.append(f.read())
#sol = Solution()
#k = sol.predict(trainn_data)
#print(len(k))
