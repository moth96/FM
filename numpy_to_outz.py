import numpy as np

# 读取所有数据和物料列表
all_data = np.load('all_data.npy')
species_list = np.load('species_list.npy')

# chi 原文件数 spe 物料数 grid 网格数
(chi,spe,grid) = all_data.shape
# z 的分布
z = np.linspace(0,1,grid)

# 501 网格循环
for i in range(grid):
    with open("outZ\\z_%.3f"%z[i],'w') as f:
        # 72 物料循环
        for j in range(spe):
            f.write(species_list[j])
            f.write('\n')
            # 129 文件循环
            for k in range(chi):
                f.write(str(all_data[k][j][i]))
                f.write('\t')
                # 每隔五个数据换行
                if (k + 1)%5 == 0:
                    f.write('\n')
            f.write('\n')
        print("outZ\\z_%.3f 输出完成\n"%z[i])
        
                
        
