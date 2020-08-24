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

def spe_to_array(content_lines,spe,grid,start):
    data = np.ones([spe,chi],dtype = float)
    for i in range(spe):
        data[i] = split_species(content_lines,start + i * spe_leap,spe_leap)
    data = data.T[np.lexsort(data[::-1,:])].T
    return data

path_dir = 'OutZ\\'
file_list = os.listdir(path_dir)

# 读取所有数据和物料列表
all_data = np.load('all_data.npy')
species_list = np.load('species_list.npy')

# chi 原文件数 spe 物料数 grid 网格数
(chi,spe,grid) = all_data.shape
# z 的分布
z = np.linspace(0,1,grid)
# 物料行数间隔
spe_leap = chi//5 + 2
for i in range(grid):
    content_lines = read_file_lines("outZ\\z_%.3f"%z[i])
    data = spe_to_array(content_lines,spe,grid,0)
    with open("outZ_sort\\z_%.3f"%z[i],'w') as f:
        # 72 物料循环
        for j in range(spe):
            f.write(species_list[j])
            f.write('\n')
            # 129 文件循环
            for k in range(chi):
                f.write(str(data[j][k]))
                f.write('\t')
                # 每隔五个数据换行
                if (k + 1)%5 == 0:
                    f.write('\n')
            f.write('\n')
        print("outZ_sort\\z_%.3f 输出完成\n"%z[i])
