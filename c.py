import os

def gridpoints(content):
    z = content[content.find("Z\n"):content.find("temperature")]
    z.strip()
    z = z.replace("\n","")
    z = z.replace("\t\t","\t")
    z = z.split("\t")
    grid = len(z) - 1
    return grid
    
def split_spcies(num1,grid):
    str = ""
    for i in range(num1,num1+int(grid/5)+1):
        str = str + lines[i].rstrip()
    str = str.strip()
    str = str.split("\t")
    return str

def filelist(path):
    filename = os.listdir(path)
    filepath = []
    for i in filename:
        filepath.append(path + "\\" + i)
    return filepath

  
with open("out100\\NC7H16_p01_0chi000.1tf0373to0330") as f:
    content = f.read()    
    g = gridpoints(content)

line_space = int(g/5) + 2
file = filelist("C:\\Users\\312041716\\Desktop\\study\\003 study\\python\\FlameLEt Process Variable\\out100")

#chist = []   
for i in range(g):
    data = [[] for i in range(len(file))]
    for j in range(len(file)):
        with open(file[j]) as f:
            lines = f.readlines()
            for k in range(34,34 + 69*line_space,line_space):
                a = split_spcies(k,g)
                data[j].append(a[i])
            b = split_spcies(34+82*line_space,g)
            data[j].append(b[i])
            #chist.append(float(b[i]))
#print(max(chist))
#print(min(chist))
    with open("out100\\NC7H16_p01_0chi000.1tf0373to0330") as f:
        lines = f.readlines()
        with open("outC\\z_%s"%str(data[0][0]),"w") as c:
            c.write("Z %s\n"%str(data[0][0]))
            c.write(lines[34+82*line_space-1])
            for l in range(len(file)):
                c.write(data[l][-1])
                c.write("\t")
            c.write("\n\n")
            for k in range(69):
                c.write(lines[55 + line_space * k])
                for l in range(len(file)):
                    c.write(data[l][k+1])
                    c.write("\t")
                c.write("\n\n")

          
'''
with open("out100\\NC7H16_p01_0chi000.1tf0373to0330") as f:    
    lines = f.readlines()
    str = split_spcies(34,g)
    print(str)
'''

#f = filelist("C:\\Users\\312041716\\Desktop\\study\\003 study\\python\\FlameLEt Process Variable\\out100")
'''
data = [[] for i in range(3)]
for i in range(3):
    data[i].append(1)
    data[i].append(2)
    data[i].append(3)
    data[i].append(4)
print(data)
'''