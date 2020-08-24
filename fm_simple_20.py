import numpy as np

all_data_zc = np.load('all_data_zc.npy')
species_list = np.load('species_list.npy')

simple_slist = ['TEMPERTURE','massfraction-H2','massfraction-O2','massfraction-H2O','massfraction-CO','massfraction-CO2','massfraction-NC7H16','massfraction-N2']
# 网格数，物料数，进度变量数
(grid,spe,n) = all_data_zc.shape
#print(species_list)
# z分布
#print(grid,spe,n)

z = np.linspace(0,1,grid)
# 进度变量分布
progvar = np.linspace(0,1,n)

# 将500网格缩减为100
# new_z = np.append(np.linspace(0,0.1,51),np.linspace(0.118,1,50))
new_z = np.zeros([21])
new_data = np.ones([21,spe,n],dtype = float)
for i in range(10):
    new_z[i] = z[5 * i]
    new_data[i] = all_data_zc[i]
for i in range(11):
    new_z[10 + i] = z[50 + 45 * i]
    new_data[10 + i] = all_data_zc[50 + 45 * i]
#print(new_z)
#print(new_data[5][68])

nn_z = new_z
nn_data = np.ones([21,len(simple_slist),n],dtype = float)
for j in range(21):
    nn_data[j][0] = new_data[j][0]

for i in range(len(simple_slist) - 1):
    for j in range(21):
        nn_data[j][i+1] = new_data[j][np.where(species_list == simple_slist[i+1])[0][0] - 3]

#print(nn_data[5][6])

grid = len(nn_z)
with open("fm_cz_simple_20.fla","w") as f:
    for i in range(0,n,2):
        # 火焰面头部
        f.write("HEADER\n")
        f.write("STOICH_SCADIS\t%s\n"%str(round(progvar[i],3)))
        f.write("NUMOFSPECIES\t6\n")
        f.write("GRIDPOINTS\t%s\n"%str(grid))
        f.write("STOICH_Z\t0.0438432\n")
        f.write("PRESSURE\t1.013250E+05\n")
        f.write("BODY\n")
        f.write("%s\n"%species_list[2])
        for j in range(grid):
            # z
            f.write("%s\t"%str(round(nn_z[j],3)))
            if (j+1)%5 == 0:
                f.write('\n')
        f.write('\n')
        for j in range(len(simple_slist)):
            # 其他物料
            f.write("%s\n"%str(simple_slist[j]))
            for k in range(grid):
                f.write("%s\t"%str(nn_data[k][j][i]))
                if (k+1)%5 == 0:
                    f.write('\n')
            f.write("\n")
        '''
        # 进度变量源项
        f.write("massfraction-AR\n")
        for j in range(grid):
            f.write("%s\t"%new_data[j][-1][i])
            if (j+1)%5 == 0:
                f.write('\n')
        '''
        f.write('\n\n')
