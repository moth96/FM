import sys
import os
import re

dirpath = "C:\\Users\\312041716\\Desktop\\new\\out"
pathdir = os.listdir(dirpath)
filepath = []
for i in pathdir:
    filepath.append(dirpath + "\\" + i)

data = {}
chi_num = []
chi = []
for j in filepath:
    with open(j) as f:
        content = f.read()
        chist = re.findall("chi_st = (.*) \[1/s\]",content)
        fla = content[content.find('Z\n'):content.find('W\n')]
        chi_num.append(float(chist[0]))
        chi.append(chist[0])
        data[chist[0]] = fla

print(chi_num)
print(chi)

with open('68.fla','w') as g:
    for i in range(len(chi)):
        g.write('HEADER\n')
        g.write('STOICH_SCADIS\t%s\n' %str(min(chi_num)))
        g.write('NUMOFSPECIES	68\n')
        g.write('GRIDPOINTS	101\n')
        g.write('STOICH_Z	4.387207E-02\n')
        g.write('PRESSURE	1.013250E+05\n')
        g.write('BODY\n')
        g.write(data[chi[chi_num.index(min(chi_num))]])
        g.write('\n')
        chi_num.remove(min(chi_num))
        chi.remove(chi[chi_num.index(min(chi_num))])
 
