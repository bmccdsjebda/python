¬¬一次修改
# 分支2
# 分支1  修改1 修改2
# 分支4 修改1
# -*- coding: utf-8-sig -*-
import os
import numpy as np
import pandas as pd
import jieba.posseg as pseg
import jieba
import jieba.analyse
import sys
import re

os.chdir('E:\PWork\\tousu')
sys.path.append('E:/PWork/tousu')
jieba.load_userdict("userdict.txt")
jieba.analyse.set_idf_path("useridf.txt")


#####文件输入，第一处修改
tousu=pd.read_excel('usd1201-1231.xlsx', '1', index_col=None, na_values=['NA'])




##正则去掉无用信息
##pattern="(?:a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,4}|(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])" 
#pattern="(?:[a-zA-Z]{3,5}://){0,1}(?:(?:(?:[a-zA-Z0-9-/]+\\.)+[a-zA-Z]{2,4})|(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9]))" 
pattern = "(?:[a-zA-Z]{3,5}://){0,1}(?:(?:(?:[a-zA-Z0-9\._-]+\\.[a-zA-Z]{2,6})|(?:[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}))(?::[0-9]{1,4})*(?:/[a-zA-Z0-9\&%_\./-~-]*)?|(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9])\\.(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|[1-9]))" 

f1 = lambda x:re.sub(r"\n","",x) ##去掉回车换行符
f_lower = lambda x:x.lower() ##大写转换成小写
f_zw = lambda x:re.sub(r"：",":",x)#####中文冒号换成英文冒号
f_space = lambda x:re.sub("(?<=[a-z]) (?=[a-z])","",x) ###去掉英文间的空格
f2 = lambda x:re.sub("问卷名称|记录客户投诉的具体网址|安装事宜|分公司eoms|分公司\（emos\）|代理渠道办理|电子渠道办理|微信等电子渠道\（ds\）|促销活动具体内容|机顶盒相关问题","%",x) ###“问券名称”和“记录客户投诉的具体网址”变成%
f3 = lambda x:re.sub("(?<=%)[\\s\\S]*(?=%)","",x)  ##2个%之间的内容删掉
f4 = lambda x:re.sub("宽带账号:|投诉内容:","#",x)  ##“宽带账号”和“投诉内容”变成#
f5 = lambda x:re.sub("(?<=#)[\\s\\S]*(?=#)","",x)  ##2个#之间的内容删掉
######文本分类
hw = lambda x:",".join(re.findall("(?:错误|代码|提示)\\d{3}|los|pon|xpon|lan|猫|灯|闪|灭|亮|断了|咬断|弄断|刮断|网线|光纤|水晶头|宽带线|电缆|光缆|接头|路由器|水晶插头|挪线|走线|布线|改线|重置|线路|重启|装线|碰到线|移机|装机|接口",x))
#speed = lambda x:",".join(re.findall("慢|测速|速度|速率|kb|网速|丢包|卡顿|卡",x))
speed = lambda x:bool(re.findall("慢|测速|速度|速率|kb|网速|丢包|卡顿|卡",x))
#service = lambda x:",".join(re.findall("视频|邮箱|电视|游戏|软件",x))


f6 = lambda x:re.sub("(错误|代码|提示)\\d{3}|同单\\d{3}x|(6|7)\\d{2}|\\d+(月份|日|小时|点|分钟|号|月)|\\d+x\\d+|\\d{18}|\\d{17}x|\\d{12|\\d{11}|\\d{8}|\\d+\\w{0,2}kb{0,1}|\\d+m|kb|#|%|@~|重要服务保障客户|是否有重复工单|:提交|请详细记录客户故障现象（游戏名称等。派单至宽带业务处理组|工单回复内容与客户实际情况是否相符:|无重复工单|导航结束，请选择提交方式|客户故障现象:|（若所有网页无法打开或全局网速慢，此处不填）","",x)
########去除地址和姓名信息
f7 = lambda x:re.sub("((?<=\\W)|^)[\\w-]*(平谷|大兴|朝阳|昌平|密云|怀柔|东城|西城|海淀|石景山|丰台|通州|顺义|延庆|门头沟|宣武|崇文|区|镇|庄|村|路|条|街|大厦|楼|里|门|单元|号楼|胡同|号院)[\\w-]*(镇|庄|村|路|条|街|大厦|楼|门|里|层|单元|号楼|胡同|号院|园)[\\w-]*((?=\\W)|$)","",x)
f8 = lambda x:re.sub("((?<=\\W)|^)[\\w-]*地址\\w+区[\\w-]*((?=\\W)|$)","",x)
f9 = lambda x:re.sub("^(平谷|大兴|朝阳|昌平|密云|怀柔|东城|西城|海淀|石景山|丰台|通州|顺义|延庆|门头沟|宣武|崇文).*$","",x)
f10 = lambda x:re.sub("((?<=姓名)：?\\w{2,3})|((?<=信息为)，?\\w{2,3})","",x) ###姓名
##\\d{12}x\\d{8}：2015,2161,3483,5,X8205,7383 工单号 2015,1213,2200,35X8146,7164
##\\d{18}|\\d{17}x 身份证
##\\d{11} 手机号
##\\d{8}工单号
##工单回复内容与客户实际情况是否相符：符合导航结束，请选择提交方式|工单回复内容与客户实际情况是否相符：导航结束，请选择提交方式，                                               请详细记录客户故障现象（游戏名称等。派单至宽带业务处理组）

f_name = lambda x:re.sub(pattern,"",x)
f_name1 = lambda x:re.sub("com|cn|http|https|org|net|dns|nat|pin","",x)

tousu['new'] = tousu['投诉描述'].map(f1)      
tousu['new'] = tousu['new'].map(f_lower)    
tousu['new'] = tousu['new'].map(f_zw)   
#tousu['new'] = tousu['new'].map(f_space)
tousu['new'] = tousu['new'].map(f2)
tousu['new'] = tousu['new'].map(f3)
tousu['new'] = tousu['new'].map(f4)
tousu['new'] = tousu['new'].map(f5)
tousu['new'] = tousu['new'].map(f6)

########实现分类
tousu['class'] = tousu['new'].map(hw)
tousu['class'][tousu['class']!='']='hw'##表示硬件问题

tousu['class'][tousu['class']=='']=tousu['new'][tousu['class']==''].map(speed)
tousu['class'][tousu['class']==True]='speed'##表示速度问题
tousu['class'][tousu['class']==False]=''

#tousu['class'][tousu['class']=='']=tousu['new'][tousu['class']==''].map(service)


########实现url和name提取
tousu['new1'] = tousu['new'][tousu['class']!='hw'].map(f7)
tousu['new1'] = tousu['new1'][tousu['class']!='hw'].map(f8)
tousu['new1'] = tousu['new1'][tousu['class']!='hw'].map(f9)
tousu['new1'] = tousu['new1'][tousu['class']!='hw'].map(f10)
tousu['new2'] = tousu['new1'][tousu['class']!='hw'].map(f_name)  ###关键词里去掉域名、ip
tousu['new2'] = tousu['new2'][tousu['class']!='hw'].map(f_name1) 
tousu['new2'] = tousu['new2'][tousu['class']!='hw'].map(f_space) ###userdict不能有空格，对应这里也不能有空格

##提取网址、ip    
f_url = lambda x:re.findall(pattern,x)
tousu['url'] = tousu['new'].map(f_url)



##提取名称
def extract_idf1(line):
	freq1 = {}
	word_list=[]
	seg=jieba.cut(line)  ###分词结果，例如：魔兽世界 王者荣耀 龙之谷 英雄联盟
	for w in seg:   ###获得整体分词词频结果，例如：{'账号': 1.0, '15201049724': 1.0, '宽带': 1.0,............}
		if len(w.strip()) < 2:  ##strip() 移除字符串头尾指定字符（默认空格）
			continue ###长度小于2的词汇跳过
		freq1[w] = freq1.get(w, 0.0) + 1.0  ##出现频率 get(key,default=None) 返回w的值，默认为0.0
		word_list.append(w)  ###append() 在末尾添加对象，例如：['宽带', '账号', '15201049724',..........]
	tk_list=[]
	tk = jieba.tokenize(line)  ###把所有可以成词的词语描述出来，并确定位置
	for t in tk:
		tk_list.append((t[0],t[1],t[2]))   ###t[0]为分词，t[1]为分片起始位置，t[2]为分词结束位置+1，结果如：[('宽带', 0, 2), ('账号', 2, 4),...................]
	tk_dict={}  ###目的是标识分词及分词出现在第k个，例如：{'宽带': 0,...............}
	length1=len(tk_list)   ###len()计算列表元素的个数，例如：某一投诉内容共分词数：383
	for k in range(0,length1):  ###例如：k在0-383
		tk_dict[tk_list[k][0]]=k	###tk_list[k]是tk_list中第k个分词及词语的位置，例如：('宽带', 0, 2)；tk_list[k][0]为第k个分词，例如'宽带'，作为字典tk_dict的键key,值为该词是第k个词，即key=宽带，value=0，例如：{'宽带': 0,...............}
	
	
	list_len=len(word_list)  ###长度大于2的分词的数量，本例中：200
	tags=jieba.analyse.extract_tags(line,list_len, withWeight=True) ###只会保留2字以上的词汇。jieba.analyse.extract_tags(sentence,topK)，sentence为待提取文本，topK为返回几个权重最大的关键词，默认20。本例中，topK=list_len=200，即只返回2字以上的词。withWeight=True，给出权重值。例如：[('询问', 0.382242465), ('结果', 0.2225527515), ('客户', 0.18),..................]
	
	
	psegList = ['ns','n','nt','vn','j','i','nz','eng']  ###使用的词性列表
	tags10=[]
	list_test=[]
	for k in tags:
		idf_value=k[1]*list_len/freq1[k[0]]  ###k[1]*list_len/freq1[k[0]]=tags中某词的权重*分词数（200）/该词出现的次数
		words=pseg.cut(k[0])   ###pseg.cut() 分词、词性标注 
		tk_value=tk_dict[k[0]] ###某词出现在第n个位置 tk_dict是词典，k[0]是key，tk_value是key的值，即位置
		#print(k[0],idf_value,tk_value)
		if idf_value<5:    ###位置小于5 跳过？
			continue
		#if idf_value==10:        ###没理解这句
			#continue
		for w in words:
			if w.flag not in psegList:       ###根据词性，只需要包含在psegList里的词性的词
				continue
			#tags10.append((k[0],idf_value,w.flag)) ##返回值带idf值和词性
			tags10.append([k[0],tk_value])           ###结果如：[['IP', 135], ['BAS', 57], ['ONU', 138],..........]
			#tags10.append((k[0]))
			list_test=sorted(tags10,key=lambda x:x[1], reverse = False )       ###对tags10排序，具体参数含义不理解，结果并没有排序？？？如：[['IP', 135], ['BAS', 57], ['ONU', 138],.............]
	
	#######连接字符串
	t1 = []
	t2 = []
	t3 = ''
	list_name=[]
	list_no=[]
	for x in list_test:
		#list_name.append(x[0])
		list_no.append(x[1])     ###按序排列的分词的位置
	for x in list_test:
		t1.append(x)           ###[['BJJZTY', 41], ['PA', 43], ['CMNET', 45],............]
		if x[1]+1 not in list_no:
			for t in t1:
				t3=t3+str(t[0])
			t2.append(t3)
			t1 = []
			t3=''
	return t2
tousu['name'] = tousu['new2'][tousu['class']!='hw'].map(extract_idf1)

###再筛选
 
f_action = lambda x:bool(re.search("游戏|软件名称|玩|上不去(^网)|打不开|无法打开|进不去|使用|下载|只有|登录|登陆|例如|访问|唯独|其他|连接|打开|用不了|登不上|但是|(?<=客户投诉的网址:)\\w+", x))###句子动作

tousu['name1']=tousu['name'][tousu['new2'].fillna(value='').map(f_action)==True]


'''找出idf值=10的词语
def extract_idf2(line):
	freq1 = {}
	word_list=[]
	seg=jieba.cut(line)
	psegList = ['ns', 'n', 'nt','vn','j','i','nz','eng','m']
	for w in seg:
		if len(w.strip()) < 2:
			continue
		freq1[w] = freq1.get(w, 0.0) + 1.0  ##出现频率
		word_list.append(w)
		
	list_len=len(word_list)
	tags=jieba.analyse.extract_tags(line,list_len, withWeight=True)

	tags11=[]
	for k in tags:
		idf_value=k[1]*list_len/freq1[k[0]]
		words=pseg.cut(k[0])
		#print(k[0],idf_value)
		if idf_value!=10:
			continue
		#tags11 = k
		for w in words:
			if w.flag not in psegList:
				continue
			#tags11.append((k[0],idf_value,w.flag))
			tags11.append((k[0]))
		
	return tags11

tousu['name1'] = tousu['new2'][tousu['class']!='hw'].map(extract_idf2)
'''
#f_unic = lambda x:list(set(x))
#tousu['name'] = tousu['name'][tousu['class']!='hw'].map(f_unic)



###写入文件，第二处修改
tousu.to_excel('jiakuan12_res.xlsx',sheet_name='Sheet1')
