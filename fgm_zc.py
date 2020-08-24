import numpy as np

all_data_zc = np.load('all_data_zc.npy')
spe_list = np.load('species_list.npy')

(grid,spe,n) = all_data_zc.shape
# z 501 spe 70 c 41
# spe = 70 0.温度 1-68 species 69 源项 
# print(all_data_zc[0])
# print(grid,spe,n)
# print(spe_list)

z = np.linspace(0,1,grid)
c = np.linspace(0,1,n)


with open("fgm_style_c41_z101.fla","w") as f:
	for i in range(0,grid,5):
		# 头文件
		f.write("HEADER\n")
		f.write("PREMIX_STOICH_SCADIS\t0.000000E+00\n")
		f.write("z\t%s\n"%str(round(z[i],3)))
		f.write("NUMOFSPECIES\t68\n")
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

		# 物料
		for j in range(spe - 1):
			f.write("%s\n"%str(spe_list[j + 3]))
			for k in range(n):
				f.write(str(all_data_zc[i][j][k]))
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

