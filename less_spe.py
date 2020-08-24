# 将组分的最大值小于1e-4的删去
import numpy as np

all_data_zc = np.load("all_data_zc.npy")
spe_list = np.load("spe_68_name.npy")

spe_max = np.zeros([68],dtype = float)

(grid,spe,n) = all_data_zc.shape

# 除温度 源项 之后 遍历
for j in range(len(spe_list)):
	for i in range(grid):
		for k in range(n):
			if all_data_zc[i][j+1][k] > spe_max[j]:
				spe_max[j] = all_data_zc[i][j+1][k]

with open("spe_max.txt","w") as f:
	for i in range(len(spe_list)):
		f.write("%s\t%s\n"%(str(spe_list[i]),str(spe_max[i])))

spe_less = []
for i in range(len(spe_list)):
	if (spe_max[i] > 1e-4):
		spe_less.append(spe_list[i])

spe_less_name = np.array(spe_less)
np.save("spe_less_name",spe_less_name)