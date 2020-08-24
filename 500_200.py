import os

def data_p(num1):
    str = ""
    for i in range(num1,num1+101):
        str = str + lines[i].rstrip()
    str = str.strip()
    str = str.split("\t")
    data = []
    for i in range(50):
        data.append(str[i])
    for i in range(51):
        data.append(str[50 + 9 * i])
    return data

filename = os.listdir("C:\\Users\\312041716\\Desktop\\study\\003 study\\python\\500_200\\out")
filepath = []
newfilepath = []
for i in filename:
    filepath.append("C:\\Users\\312041716\\Desktop\\study\\003 study\\python\\500_200\\out\\" + i)
    newfilepath.append("C:\\Users\\312041716\\Desktop\\study\\003 study\\python\\500_200\\out100\\" + i)

for i in range(len(filepath)):
    with open(filepath[i]) as f:
        lines = f.readlines()
    with open(newfilepath[i],"w") as g:
        for i in range(33):
            g.write(lines[i])
        
        for i in range(33,65211,102):
            g.write(lines[i])
            a = data_p(i+1)
            for j in range(20):
                g.write('\t')
                for k in range(5):
                    g.write(a[5 * j + k])
                    g.write('\t')
                g.write('\n')
            g.write('\t')
            g.write(a[100]) 
            
            g.write("\n")
        for i in range(65313,65382):
            g.write(lines[i])