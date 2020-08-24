# 将37组分 101 z 41 c 输出为fgm类型火焰面

import numpy as np

all_data_zc = np.load('all_data_zc.npy')
spe_list = np.load('species_list.npy')
spe_write = np.load('spe_less_name.npy')

(grid,spe,n) = all_data_zc.shape

z = np.linspace(0,1,grid)
c = np.linspace(0,1,n)


with open("fgm_spe37_c41_z101.fla","w") as f:
	for i in range(0,grid,5):
		# 头文件
		f.write("HEADER\n")
		f.write("PREMIX_STOICH_SCADIS\t0.000000E+00\n")
		f.write("z\t%s\n"%str(round(z[i],3)))
		f.write("NUMOFSPECIES\t37\n")
		f.write("GRIDPOINTS\t%s\n"%str(n))
		f.write("STOICH_Z\t0.0438432\n")
		f.write("PRESSURE\t1.013250E+05\n")
		# 主体
		f.write("BODY\n")
		# 进度变量
		f.write("REACTION_PROGRESS\n")
		for j in range(n):
			f.write(str(round(c[j],3)))
			f.write('\t')
			if (j%5 == 4):
				f.write('\n')
		f.write('\n')
		# 温度
		f.write("TEMPERATURE\n")
		for j in range(n):
			f.write(str(all_data_zc[i][0][j]))
			f.write('\t')
			if(j%5 == 4):
				f.write('\n')
		f.write('\n')

		# 物料
		for j in range(spe - 2):
			if (spe_list[j + 4] in spe_write):
				f.write("%s\n"%str(spe_list[j + 4]))
				for k in range(n):
					f.write(str(all_data_zc[i][j+1][k]))
					f.write('\t')
					if (k%5 == 4):
						f.write('\n')
				f.write('\n')

		# 进度变量源项
		f.write("PREMIX_YCDOT\n")
		for k in range(n):
			f.write(str(all_data_zc[i][-1][k]))
			f.write('\t')
			if (k%5 == 4):
				f.write('\n')

		f.write('\n\n')

