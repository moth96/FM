import numpy as np
import os

def read_file_lines(dir):
    with open(dir,'r') as f:
        content = f.readlines()
    return content

def split_species(content_lines,start_p,spe_leap):
    species = ""
    for i in range(start_p + 1,start_p + 2 + spe_leap - 2):
        species = species + content_lines[i].replace('\n','')
    species = species.strip()
    species = species.split("\t")
    return species

def spe_to_array(content_lines,spe,start):
    # 存入除了c进度变量和z之外所有数据
    data = np.ones([spe - 2,n],dtype = float)
    for i in range(spe - 3):
        data[i] = split_species(content_lines,start + i * spe_leap,spe_leap)
    data[69] = split_species(content_lines,10,spe_leap)
    return data

# 线性插值后网格数
n = 41
spe_leap = n//5 + 2
# 物料数
spe = 72
# z分布
z = np.linspace(0,1,501)
# 进度变量分布
progvar = np.linspace(0,1,41)
'''
content_lines = read_file_lines("out_interp\\z_%.3f"%z[10])
data = spe_to_array(content_lines,spe,30)
print(data)
'''
all_data_zc = np.array([])
# 将目录下所有文件打包成一个数组并存为文件
for i in range(501):
    now_content = read_file_lines("out_interp\\z_%.3f"%z[i])
    all_data_zc = np.append(all_data_zc,spe_to_array(now_content,spe,30))

all_data_zc = all_data_zc.reshape(501,spe - 2,n)

np.save('all_data_zc.npy',all_data_zc)


