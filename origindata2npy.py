# z网格节点 501 温度 组分68 进度变量 进步变量源项 
import os
import numpy as np

grid = 501
# 路径
orgin_file = "AllData/"
# 文件列表
file_list = os.listdir(orgin_file)
# 文件数
file_num = len(file_list)
# 数据开始位置 温度
body_start = 136 - 1
# 物料表数组
spe_list = []
# z
z = np.linspace(0,1,grid)
# 包含源文件所有数据的numpy数组(文件数，温度1+68组分+1c+1源项,网格数)
alldata = np.ones([file_num,71,grid],dtype = float)

def read_line(filename):
	with open(orgin_file+filename) as f:
		content = f.readlines()
		return content

def split_spe(start):
	spe_data = ""
	for i in range(start+1,start+102):
		spe_data = spe_data + content[i].rstrip()
	spe_data = spe_data.strip()
	spe_data = spe_data.split("\t")
	return spe_data

def data_to_numpy(start,num,spe_num):
	spe_list.append(content[start].rstrip())
	alldata[num][spe_num] = split_spe(start)

for i in range(file_num):
	content = read_line(file_list[i])
	# 存入c 
	c_start = 8398 - 1
	data_to_numpy(c_start,i,0)
	# 存入t yi 等
	for j in range(68+1):
		data_to_numpy(body_start + j * 102,i,j+1)
	# 存入c源项
	data_to_numpy(c_start + 102,i,70)

max_temp = []
for i in range(file_num):
	max_temp.append(alldata[i][1].max())

# 排序 温度高的文件在前
alldata_sort = np.zeros([file_num,71,grid],dtype = float)
for i in range(file_num):
	pos = max_temp.index(max(max_temp))
	alldata_sort[i] = alldata[pos]
	max_temp[pos] = 0

np.save("alldata_sort.npy",alldata_sort)
spe_list = np.array(spe_list)
np.save("spe_list.npy",spe_list)
