import numpy as np 

alldata = np.load("alldata_sort.npy")

# 转置为 （501结点，物料71，文件数/不同耗散率
newdata = alldata.transpose(2,1,0)
(grid,spe_num,chi) = newdata.shape

# 过程变量节点数 
n = 41
pragvar = np.linspace(0,1,n)
# zc分布的全数据
data_zc = np.zeros([grid,spe_num - 1,n],dtype = float)

# for i in range(grid):
i = 50
# 过程变量归一化
print(newdata[i][0])
newdata[i][0] = np.interp(newdata[i][0],[newdata[i][0].min(),newdata[i][0].max()],[0.0,1.0])
print(newdata[i][0])
'''
# 70物料循环插值
for j in range(spe_num - 1):
	data_zc[i][j] = np.interp(pragvar,newdata[i][0][::-1],newdata[i][j + 1][::-1])


np.save("alldata_zc.npy",data_zc)'''
