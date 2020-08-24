import os
import re
import numpy as np

# 读取文件内容并返回
def read_file(list_dir):
    with open(list_dir,'r') as f:
        content = f.read()
    return content

# 按行的方式读取文件并返回
def read_file_lines(list_dir):
    with open(list_dir,'r') as f:
        content = f.readlines()
    return content    

# 返回组分数目，整型
def num_of_species(content):
    return int(re.findall("numOfSpecies = ([0-9]+)",content)[0])

# 返回网格数，整型
def grid_points(content):
    return int(re.findall("gridPoints = ([0-9]+)",content)[0])

# 返回文件正文开始的位置
def body_start(content_lines):
    for i in content_lines:
        if 'body' in i:
            return content_lines.index(i)
            break

# 将一种物料分布存入大小为501的数组
def split_species(content_lines,start_p,specie_leap):
    species = ""
    for i in range(start_p + 2,start_p + 2 + specie_leap - 1):
        species = species + content_lines[i].rstrip()
    species = species.strip()
    species = species.split("\t")
    return species

# 将所有数据存入一个二维数组
def species_to_array(content_lines,num_of_species,grid_points,start):
    # 创建一个行为物料数+4，列为网格数的二维数组
    data = np.ones([num_of_species + 4,grid_points],dtype = float)
    # 存入各物料的名字
    specie_names = []
    pointer = start + 1
    # 将过程变量和过程变量源项存入数组
    for i in range(2):
        specie_names.append(content_lines[8396 + 1 + i * specie_leap].strip())
        data[i] = split_species(content_lines , 8396 + i * specie_leap, specie_leap)
    
    # 存Z,T,Yi入数组
    for i in range(num_of_species + 2):
        specie_names.append(content_lines[start + 1 + i * specie_leap].strip())
        data[2 + i] = split_species(content_lines,start + i * specie_leap,specie_leap)

    return specie_names,data

# 文件目录
file_dir = "Origin_Data\\"
file_list = os.listdir(file_dir)
# 样例文件，用于读取这一批文件中的物料数，网格数
file_exm = file_dir + file_list[0]

content = read_file(file_exm)
# 物料数
num_of_species = num_of_species(content)
# 网格数
grid_points = grid_points(content)

# 物料名称之间的行数间隔
specie_leap = grid_points // 5 + 2

content_lines = read_file_lines(file_exm)
# 正文开始的地方
start = body_start(content_lines)

'''
# all_data = np.ones([len(file_list),num_of_species + 4,grid_points],dtype = float)
all_data = np.array([])
# 将目录下所有文件打包成一个数组并存为文件
for i in file_list:
    now_content = read_file_lines(file_dir + i)
    all_data = np.append(all_data,species_to_array(now_content,num_of_species,grid_points,start)[1])

all_data = all_data.reshape(len(file_list),num_of_species + 4,grid_points)
np.save('all_data.npy',all_data)
'''
species = np.array(species_to_array(content_lines,num_of_species,grid_points,start)[0])
np.save('species_list.npy',species)






