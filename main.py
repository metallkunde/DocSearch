# -*- coding: utf-8 -*-
import os
import jieba
import time
import functools
import sys

class word_segmentation:
    stopwords = [line.strip() for line in open('stopwords.txt', encoding='utf-8').readlines()]
    docu_list = []
    def jieba_seg(self, inputS):
        output=''
        depart=jieba.cut(inputS.strip())
        for word in depart:
            if word not in self.stopwords:
                if word !='\t':
                    output=output+word+" "
        return output

    def doc_dic(self, path):
        docu_set=dict()
        files=os.listdir(path)
        print("正在进行分词...")
        i=1
        for file in files:
            position=path+file
            with open(position, "r", encoding='gbk') as f:
                data = f.read()  # 读取文件
                ret = self.jieba_seg(data)
                docu_set[i] = ret
                self.docu_list.append(file)
                i=i+1
        return docu_set

class inverted_index:
    my_idx=dict()
    words=[]
    count=1
    def __init__(self, my_dataset):
        self.my_dataset=my_dataset
        self.count_matrix=[]
        for i in range(50000):
            self.count_matrix.append([0]*120)
        self.Weight2=[0]*120

    def construction(self):
        for i in self.my_dataset.values():
            cut=i.split()
            self.words.extend(cut)
        words_set=set(self.words)
        for j in words_set:
            self.my_idx[j]=self.count
            self.count=self.count+1
        for i in self.my_dataset.keys():
            mytemp=self.my_dataset[i].split()
            for temp in mytemp:
                self.count_matrix[self.my_idx[temp]][i] += 1
            mytemp=set(mytemp)
            for temp in mytemp:
                v=self.count_matrix[self.my_idx[temp]][i]
                self.Weight2[i] += v*v


if __name__=="__main__":
    path = './sanguoyanyi/'
    seg1=word_segmentation()
    dataset=seg1.doc_dic(path)
    index1 = inverted_index(dataset)
    index1.construction()
    print("分词成功!")
    print("请输入要查询的内容，退出请输入quit：")
    string_input = input()
    #string_input="曹植"
    while( string_input != "quit" ):
        string_input = seg1.jieba_seg(string_input).split()
        print(string_input)
        matrix1=[]
        value=0
        for i in range(120):
            matrix1.append({"id": i, "score": 0})
        for str in string_input:
            if str in index1.my_idx:
                value = value+1
                idx=index1.my_idx[str]
                for j in range(120):
                    #print(matrix1[j]['score'])
                    matrix1[j]['score'] += index1.count_matrix[idx][j]
        if value == 0:
            print("没找到相关内容")
            break
        for i in range(120):
            if index1.Weight2[i] !=0:
                matrix1[i]['score'] = matrix1[i]['score']/((index1.Weight2[i] * value) ** 0.5)
            else:
                matrix1[i]['score'] = 0
        def cmp(w1, w2):
            return w2['score'] - w1['score']
        matrix1.sort(key=functools.cmp_to_key(cmp))
        count=0
        for i in range(120):
            if (matrix1[i]['score'] != 0):
                count += 1
                print("相关度： %s" % (matrix1[i]['score']))
                filename = seg1.docu_list[matrix1[i]['id'] - 1]
                with open(path + filename, "r", encoding='gbk') as fp:
                    url = fp.readline()
                    title = fp.readline()
                    path_temp = path + filename
                    modifiedTime = time.localtime(os.stat(path_temp).st_mtime)
                    createdTime = time.localtime(os.stat(path_temp).st_ctime)
                    mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)
                    cTime = time.strftime('%Y-%m-%d %H:%M:%S', createdTime)
                    print("修改时间: %s" % (mTime))
                    print("创建时间: %s" % (cTime))
                    print("url链接：%s" % (url))
                    print("标题：%s" % (title))
                    print("\n")
        print("共找到%d条相关内容" % (count))
        string_input=input()
    print("bye")