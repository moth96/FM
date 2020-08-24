import numpy as np

all_data_zc = np.load('all_data_zc.npy')
species_list = np.load('species_list.npy')

# 网格数，物料数，进度变量数
(grid,spe,n) = all_data_zc.shape
#print(species_list)
# z分布
z = np.linspace(0,1,grid)
# 进度变量分布
progvar = np.linspace(0,1,n)

with open("fm_cz_500.fla","w") as f:
    for i in range(n):
        # 火焰面头部
        f.write("HEADER\n")
        f.write("STOICH_SCADIS\t%s\n"%str(round(progvar[i],3)))
        f.write("NUMOFSPECIES\t69\n")
        f.write("GRIDPOINTS\t%s\n"%str(grid))
        f.write("STOICH_Z\t0.0438432\n")
        f.write("PRESSURE\t1.013250E+05\n")
        f.write("BODY\n")
        f.write("%s\n"%species_list[2])
        for j in range(grid):
            # z
            f.write("%s\t"%str(round(z[j],3)))
            if (j+1)%5 == 0:
                f.write('\n')
        f.write('\n')
        for j in range(spe - 1):
            # 其他物料
            f.write("%s\n"%str(species_list[j+3]))
            for k in range(grid):
                f.write("%s\t"%str(all_data_zc[k][j][i]))
                if (k+1)%5 == 0:
                    f.write('\n')
            f.write("\n")
        # 进度变量源项
        f.write("massfraction-AR\n")
        for j in range(grid):
            f.write("%s\t"%all_data_zc[j][-1][i])
            if (j+1)%5 == 0:
                f.write('\n')
        f.write('\n\n')


