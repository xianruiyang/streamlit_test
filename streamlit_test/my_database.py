import json
import random
import uuid

RELATION_LIST = ['单行','须','使','畏','恶','反']
DANXING = 0
XU = 1
SHI = 2
WEI = 3
WU = 4
FAN = 5

def copy_list(inp):
    rt = list(inp)
    if len(rt) and (isinstance(rt[0],list) or isinstance(rt[0],tuple)):
        for i in range(len(rt)):
            rt[i] = copy_list(rt[i])
    return rt

class herb_db:  #中药数据库
    def __init__(self,url):
        self.data = {'index':{},'herb':{},'relation':{},'recipe':{}}
        self.url = url
        return

    def load(self,url): #用json起始化数据库
        f = open(url)
        self.data = json.load(f)
        f.close()
    def save(self,url=""): #保存数据库到json
        if url == "":
            if self.url == "":
                return
            f = open(self.url,'w+')
            json.dump(self.data,f)
            f.close()
            return
        f = open(url,'w+')
        json.dump(self.data,f)
        f.close()
    def update(self):
        self.load(self.url)
        return

    def add_realherb(self,name,compose,intro="无"):    #生成实际药草
        id = str(uuid.uuid1())
        self.data['herb'][id] = {'name':name,'all_name':[name],'intro':intro,'compose':compose,'relation':[],'recipe':[]}
        return id
    def del_realherb(self,id):  #删除实际药草
        for i in copy_list(self.data['herb'][id]['relation']):  #删除对应配伍关系
            self.del_relation(i)
        for i in copy_list(self.data['herb'][id]['recipe']):  #删除对应配方
            self.del_recipe(i)
        for i in self.data['herb'][id]['all_name']:
            self.data['index'].pop(i)   #删除对应名称索引
        self.data['herb'].pop(id)   #删除主体
    def change_realherb(self,id,all_name,compose,intro):
        for i in self.data['herb'][id]['all_name']:
            self.data['index'].pop(i)
        self.data['herb'][id]['name'] = all_name[0]
        self.data['herb'][id]['all_name'] = all_name
        for i in self.data['herb'][id]['all_name']:
            self.link_herb(i,id)
        self.data['herb'][id]['compose'] = compose
        self.data['herb'][id]['intro'] = intro

    def check_herb(self,name):  #检查药草存在
        return name in self.data['index'].keys()
    def add_herb(self,name,compose=[],intro="无"): #生成药草
        if name in self.data['index'].keys():
            return False
        self.data['index'][name] = self.add_realherb(name,compose,intro)
        return True
    def del_herb(self,name):    #删除药草
        if name not in self.data['index'].keys():
            return False
        id = self.data['index'][name]
        self.del_realherb(id)   #删除主体
    def link_herb(self,name,id):
        if name in self.data['index'].keys():
            return False
        self.data['index'][name] = id
        return True
    def merge_herb(self,h1,h2): #合并药草
        if not self.check_herb(h1):
            return False
        if not self.check_herb(h2):
            return False
        rh1 = self.data['index'][h1]
        rh2 = self.data['index'][h2]
        if rh1 == rh2:
            return False
        for i in copy_list(self.data['herb'][rh2]['relation']):
            temp = copy_list(self.data['relation'][i])
            if temp[0]==rh2:
                temp[0]=rh1
            if temp[1]==rh2:
                temp[1]=rh1
            self.data['relation'][i] = temp
        for i in self.data['herb'][rh2]['all_name']: #重药材定向索引
            self.data['index'][i] = rh1
        for i in copy_list(self.data['herb'][rh2]['relation']):  #合并配伍关系
            temp = copy_list(self.data['relation'][i])
            if temp[0]==rh2:
                temp[0]=rh1
            if temp[1]==rh2:
                temp[1]=rh1
            for j in self.data['herb'][rh1]['relation']:    
                if ((temp[0] == j[0] and temp[1] == j[1]) or (temp[0] == j[1] and temp[1] == j[0])) and temp[1] == j[1]: #完全相同则删除
                    self.del_relation(i)
                    break
            else:
                self.data['relation'][i] = temp
                self.data['herb'][rh1]['relation'].append(i)    #生成索引
        for i in copy_list(self.data['herb'][rh2]['recipe']):    #合并配方
            for j in range(len(self.data['recipe'][i][1])):
                if self.data['recipe'][i][1][j][0] == rh2:
                    self.data['recipe'][i][1][j][0] = rh1
                    break
            self.data['herb'][rh1]['recipe'].append(i)
        self.data['herb'][rh1]['all_name'] = copy_list(set(self.data['herb'][rh1]['all_name']+self.data['herb'][rh2]['all_name']))   #合并名称
        self.data['herb'][rh1]['all_name'].sort()
        self.data['herb'][rh1]['relation'] = list(set(self.data['herb'][rh1]['relation']))
        self.data['herb'][rh1]['relation'].sort()
        self.data['herb'][rh1]['recipe'] = list(set(self.data['herb'][rh1]['recipe']))
        self.data['herb'][rh1]['recipe'].sort()
        self.data['herb'].pop(rh2)  #清除旧主体

    def add_relation(self,h1,h2,re):    #增加配伍关系
        self.add_herb(h1)
        self.add_herb(h2)
        if self.data['index'][h1]==self.data['index'][h2] and re!=0:
            return False
        if re == 0:
            h2 = h1
        if re == 6:
            temp = h1
            h1 = h2
            h2 = temp
            re = 3
        id = str(uuid.uuid1())
        self.data['relation'][id] = [self.data['index'][h1],self.data['index'][h2],re]
        self.data['herb'][self.data['index'][h1]]['relation'].append(id)    #生成配伍索引
        self.data['herb'][self.data['index'][h1]]['relation'].sort()
        if re!=0:
            self.data['herb'][self.data['index'][h2]]['relation'].append(id)
            self.data['herb'][self.data['index'][h2]]['relation'].sort()
        return True
    def del_relation(self,id):  #删除配伍关系
        h1 = self.data['relation'][id][0]
        h2 = self.data['relation'][id][1]
        self.data['herb'][h1]['relation'].remove(id)    #删除配伍索引
        if h2!=h1:
            self.data['herb'][h2]['relation'].remove(id)
        self.data['relation'].pop(id)

    def add_recipe(self,recipe):    #生成药方
        id = str(uuid.uuid1())
        for i in range(len(recipe[1])): #为药材建立配方索引
            self.add_herb(recipe[1][i][0])
            if id not in self.data['herb'][self.data['index'][recipe[1][i][0]]]['recipe']:
                self.data['herb'][self.data['index'][recipe[1][i][0]]]['recipe'].append(id)
                self.data['herb'][self.data['index'][recipe[1][i][0]]]['recipe'].sort()
            recipe[1][i][0] = self.data['index'][recipe[1][i][0]]
        self.data['recipe'][id] = recipe
    def del_recipe(self,id):    #删除配方
        temp =set()
        for i in self.data['recipe'][id][1]:    #删除配方索引
            if i[0] not in temp:
                self.data['herb'][i[0]]['recipe'].remove(id)
                temp.add(i[0])
        self.data['recipe'].pop(id)
    def change_recipe(self,id,recipe):
        self.del_recipe(id)
        for i in range(len(recipe[1])): #为药材建立配方索引
            self.add_herb(recipe[1][i][0])
            if id not in self.data['herb'][self.data['index'][recipe[1][i][0]]]['recipe']:
                self.data['herb'][self.data['index'][recipe[1][i][0]]]['recipe'].append(id)
                self.data['herb'][self.data['index'][recipe[1][i][0]]]['recipe'].sort()
            recipe[1][i][0] = self.data['index'][recipe[1][i][0]]
        self.data['recipe'][id] = recipe


    def herb_com(self,herb,inp_list):
        rt = 0
        for i in inp_list:
            for j in herb[1]['all_name']:
                rt+=j.count(i)
        return rt
    def relation_com(self,relation,inp_list):
        rt = 0
        for i in inp_list:
            rt+=self.data['herb'][relation[1][0]]['all_name'].count(i)
            rt+=self.data['herb'][relation[1][1]]['all_name'].count(i)
        return rt
    def recipe_com(self,recipe,inp_list):
        rt = 0
        for i in inp_list:
            for j in recipe[1][0]:
                rt+=j.count(i)
            for j in recipe[1][1]:
                rt+=self.data['herb'][j[0]]['all_name'].count(i)
        return rt

    def get_herb_id(self,name):
        if name in self.data['index'].keys():
            return self.data['index'][name]
        return False
    def get_herb_name(self,id):
        if id in self.data['herb'].keys():
            return self.data['herb'][id]['name']
        return "药材数据丢失"
    def get_herbs(self,str=""):
        rt = copy_list(self.data['herb'].items())
        return rt
    def get_relation(self,id):
        return self.data['relation'][id]
    def get_relations(self,str=""):
        rt = copy_list(self.data['relation'].items())
        return rt
    def get_recipes(self,str=""):
        rt = copy_list(self.data['recipe'].items())
        return rt

    def find_relation(self,name):
        if not self.check_herb(name):
            return False
        return copy_list(self.data['herb'][self.data['index'][name]]['relation'])
    def find_relations(self,name_list):
        rt_in_index = set()
        rt_out_index = set()
        temp = []
        for i in name_list:
            temp.append(set(self.find_relation(i)))
        for i in range(0,len(temp)):
            rt_out_index.update(temp[i])
            for j in range(i+1,len(temp)):
                rt_in_index.update(temp[i]&temp[j])
        rt_out_index -= rt_in_index
        rt_out = []
        rt_in = []
        for i in rt_out_index:
            temp = self.get_relation(i)
            if temp[2]==0:
                rt_in.append(temp)
            else:
                rt_out.append(temp)
        for i in rt_in_index:
            temp = self.get_relation(i)
            rt_in.append(temp)
        return [rt_in,rt_out]

class recipe_input_helper:  #配方输入辅助
    def __init__(self):
        self.reset()
    def reset(self):
        self.name = ""
        self.usage = ""
        self.dipose = ""
        self.use = ""
        self.compose = []
    def set_name(self,name):
        self.name = name
    def set_usage(self,usage):
        self.usage = usage
    def set_dipose(self,dipose):
        self.dipose = dipose
    def set_use(self,use):
        self.use = use
    def add_herb(self,name,dipose,weight):
        for i in range(len(self.compose)):
            if name==self.compose[i][0]:
                self.compose[i][2]+=weight
                return
        else:
            self.compose.append([name,dipose,weight])
    def delete_herb(self,id):
        self.compose.pop(id)
    def set_herb(self,list):
        for i in list:
            self.add_herb(i[0],i[1],i[2])
    def change_herb(self,name,dipose,weight):
        for i in range(len(self.compose)):
            if name == self.compose[i][0]:
                self.compose[i][1] = dipose
                self.compose[i][2] = weight
                return
    def clear(self):
        self.compose = []
    def check(self):
        return self.name == "" or self.usage == "" or self.dipose == "" or self.use == "" or self.compose == []
    def output(self):
        if self.check():
            return False
        return [[self.name,self.usage,self.dipose,self.use],self.compose]






