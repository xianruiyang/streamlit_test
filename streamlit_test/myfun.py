import numpy as np
#import jieba

matchnum = ['单行','须','使','畏','恶','反']

def compare_str(str,list):#计算符合度,list为排序词，str为排序项
    c = 0
    for i in list:
        c+=str.count(i)
    return c

def sort_list(list,inp,fun = compare_str):#关键词搜索排序
    count = []
    '''
    inp = jieba.cut(inp,cut_all = True)
    inp = '.'.join(inp)
    inp = inp.split('.')
    '''
    for i in list:
        count.append(fun(i["name"],inp))
    return sorted(list,key = lambda x:-count[list.index(x)])

