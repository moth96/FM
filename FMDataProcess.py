#这是一个用来处理FlameMaster产生数据的类
import numpy as np
import os
import shutil

class DataProcess:
	def __init__(self,inputDataDir):
		#文件目录
		self.dataDir = inputDataDir
		#文件列表
		self.fileList = self.getFileList()
		#文件数目
		self.fileNum = len(self.fileList)
		#物料数
		self.SpeNum = self.getSpeNum()
		#网格数
		self.grid = self.getGridPoints()
		#Zst
		self.Zst = self.getZst()

	#如果目录不存在，检测是否存在含有上支数据的up目录和中支数据的mid目录
	#如存在，将数据复制到inputDataDir内
	def moveFile(self):
		if not os.path.exists(self.dataDir):
			print("目标路径不存在，将创建路径\n")
			os.makedirs(self.dataDir)
			if os.path.exists("up") and os.path.exists("mid"):
				file_dir = "up/"
				new_dir = "AllData/"
				file_list = os.listdir(file_dir)

				for i in file_list:
					new_filename = file_dir[:-1] + "_" + i[12:20]
					shutil.copy(file_dir+i,new_dir+new_filename)

				file_dir = "mid/"
				new_dir = "AllData/"
				file_list = os.listdir(file_dir)

				for i in file_list:
					new_filename = file_dir[:-1] + "_" + i[12:20]
					shutil.copy(file_dir+i,new_dir+new_filename)

			else:
				print("上支或中支数据不存在\n")
		else:
			pass

	#返回文件目录
	def getFileList(self):
		self.moveFile()
		return os.listdir(self.dataDir)

	#返回第num文件的内容
	def readlineFile(self,num = 0):
		with open(self.dataDir + self.fileList[num]) as f:
			content = f.readlines()
			return content

	#返回物料数节点数
	def getSpeNum(self):
		content = self.readlineFile(0)
		for elem in content:
			if elem[:12] == "numOfSpecies":
				return int(elem[14:-1])

	#返回节点网格数
	def getGridPoints(self):
		content = self.readlineFile(0)
		for elem in content:
			if elem[:10] == "gridPoints":
				return int(elem[13:-1])

	#返回Zst
	def getZst(self):
		content = self.readlineFile(0)
		for elem in content:
			if elem[:4] == "Z_st":
				return float(elem[7:-6])

	#返回第num个文件的耗散率
	def getChist(self,num):
		content = self.readlineFile(num)
		for elem in content:
			if elem[:6] == "chi_st":
				return float(elem[9:-6])

	#返回第num个文件的最大温度
	def getTmax(self,num):
		content = self.readlineFile(num)
		for elem in content:
			if elem[:4] == "Tmax":
				return float(elem[7:-4])

	#返回温度数据所在的位置
	def getTempPosition(self):
		content = self.readlineFile(0)
		for i in range(len(content)):
			if content[i] == "temperature [K]\n":
				return i

	#返回过程变量所在的位置
	def getProgVarPosition(self):
		content = self.readlineFile(0)
		for i in range(len(content)):
			if content[i] == "ProgVar\n":
				return i

	def speSplit(self,dataStart,content):
		speData = ""
		for i in range(dataStart + 1,dataStart + 1 + self.grid // 5 + 1):
			speData = speData + content[i].rstrip()
		speData = speData.strip()
		speData = speData.split("\t")
		return speData

	#将原始数据按最高温度高低顺序存入allData中，返回三维矩阵
	def orginData2npy(self):
		print("正在读取源数据....\n")
		#建立一个三维numpy矩阵，x为文件数，y为物料+温度+过程变量+过程变量源项，z为网格数目
		allData = np.ones([self.fileNum,self.SpeNum + 3,self.grid],dtype = float)
		#温度开始的位置
		dataStart = self.getTempPosition()
		#过程变量数据开始的位置
		progVarStart = self.getProgVarPosition()
		#建立一个数组将最高温度的数据存入其中
		chiTmax = []
		for i in range(self.fileNum):
			chiTmax.append(self.getTmax(i))
		i = 0
		while(i < self.fileNum):
			#最高温度所在位置
			pos = chiTmax.index(max(chiTmax))
			if chiTmax[pos] == 0:
				break
			#读取该位置的文件
			content = self.readlineFile(pos)
			#存入过程变量
			allData[i][0] = self.speSplit(progVarStart,content)
			#存入温度和各组分
			for j in range(self.SpeNum + 1):
				allData[i][j+1] = self.speSplit(dataStart + j * (self.grid // 5 + 2),content)

			#存入过程变量源项
			allData[i][-1] = self.speSplit(progVarStart + (self.grid // 5 +2),content)
			#递增 最高温度置0
			i = i + 1
			chiTmax[pos] = 0.0
		#np.save(orginData,allData)
		print("数据读取完毕...\n")
		return allData

	#返回物料组分表
	def getSpeList(self):
		speList = []
		#进度变量
		speList.append("REACTION_PROGRESS")
		#温度
		speList.append("TEMPERATURE")
		#各种组分
		content = self.readlineFile(0)
		dataStart = self.getTempPosition()
		step = self.grid // 5 + 2
		for i in range(dataStart + step,dataStart + step * self.SpeNum + 1,step):
			speList.append(content[i].strip())
		#进度变量源项
		speList.append("PREMIX_YCDOT")
		return speList

	#将耗散率与质量分数为基的数据转换为质量分数和进度变量
	def chistToProgVar(self,progVarNum = 41):
		print("正在处理数据...\n")
		#载入数据
		allData = self.orginData2npy()
		#转置为 x 为 grid，y 为 组分，z为文件数/不同耗散率
		newData = allData.transpose(2,1,0)
		progVar = np.linspace(0,1,progVarNum)
		#zc分布的全部数据 
		dataZC = np.zeros([self.grid,self.SpeNum + 2,progVarNum],dtype = float)
		#节点循环
		for i in range(self.grid):
			#过程变量归一化
			newData[i][0] = np.interp(newData[i][0],[newData[i][0].min(),newData[i][0].max()],[0.0,1.0])
			# 各组分循环插值 各组分+温度+进度变量源项
			for j in range(self.SpeNum + 2):
				dataZC[i][j] = np.interp(progVar,newData[i][0][::-1],newData[i][j + 1][::-1])

		np.save("alldataZC.npy",dataZC)
		print("数据处理完毕...\n")
		return dataZC


	#写火焰面文件，文件名为flaName，网格数为outputGridPoint
	def writeFlameletFile(self,flaName = "fm.fla",outputGridPoint = 101):
		print("正在写入火焰面数据...\n")
		#获得火焰面数据和组分数据
		dataZC = self.chistToProgVar()
		speList = self.getSpeList()

		(grid,spe,n) = dataZC.shape

		z = np.linspace(0,1,grid)
		c = np.linspace(0,1,n)

		with open(flaName,"w") as f:
			for i in range(0,grid,self.grid // outputGridPoint):
				# 头文件
				f.write("HEADER\n")
				f.write("PREMIX_STOICH_SCADIS\t0.000000E+00\n")
				f.write("z\t%s\n"%str(round(z[i],3)))
				f.write("NUMOFSPECIES\t%d\n"%self.SpeNum)
				f.write("GRIDPOINTS\t%s\n"%str(n))
				f.write("STOICH_Z\t%s\n"%str(self.Zst))
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
					f.write("%s\n"%str(speList[j + 1]))
					for k in range(n):
						f.write(str(dataZC[i][j][k]))
						f.write('\t')
						if (k%5 == 4):
							f.write('\n')
					f.write('\n')

				# 进度变量源项
				f.write("PREMIX_YCDOT\n")
				for k in range(n):
					f.write(str(dataZC[i][-1][k]))
					f.write('\t')
					if (k%5 == 4):
						f.write('\n')

				f.write('\n\n')
		print("火焰面文件已生成\n")
		print("文件为%s\n"%(os.getcwd() + '\\' +flaName))


	#写火焰面文件，火焰面在当量质量分数附近加密，网格数为101
	def writeMsehRefineFlameletFile(self,flaName = "fm.fla"):
		print("正在写入火焰面数据...\n")
		#获得火焰面数据和组分数据
		dataZC = self.chistToProgVar()
		speList = self.getSpeList()

		(grid,spe,n) = dataZC.shape

		z = np.linspace(0,1,grid)
		c = np.linspace(0,1,n)

		with open(flaName,"w") as f:
			for i in range(0,grid//10):
				# 头文件
				f.write("HEADER\n")
				f.write("PREMIX_STOICH_SCADIS\t0.000000E+00\n")
				f.write("z\t%s\n"%str(round(z[i],3)))
				f.write("NUMOFSPECIES\t%d\n"%self.SpeNum)
				f.write("GRIDPOINTS\t%s\n"%str(n))
				f.write("STOICH_Z\t%s\n"%str(self.Zst))
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
					f.write("%s\n"%str(speList[j + 1]))
					for k in range(n):
						f.write(str(dataZC[i][j][k]))
						f.write('\t')
						if (k%5 == 4):
							f.write('\n')
					f.write('\n')

				# 进度变量源项
				f.write("PREMIX_YCDOT\n")
				for k in range(n):
					f.write(str(dataZC[i][-1][k]))
					f.write('\t')
					if (k%5 == 4):
						f.write('\n')

				f.write('\n\n')

			for i in range(grid//10,grid,9):
				# 头文件
				f.write("HEADER\n")
				f.write("PREMIX_STOICH_SCADIS\t0.000000E+00\n")
				f.write("z\t%s\n"%str(round(z[i],3)))
				f.write("NUMOFSPECIES\t%d\n"%self.SpeNum)
				f.write("GRIDPOINTS\t%s\n"%str(n))
				f.write("STOICH_Z\t%s\n"%str(self.Zst))
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
					f.write("%s\n"%str(speList[j + 1]))
					for k in range(n):
						f.write(str(dataZC[i][j][k]))
						f.write('\t')
						if (k%5 == 4):
							f.write('\n')
					f.write('\n')

				# 进度变量源项
				f.write("PREMIX_YCDOT\n")
				for k in range(n):
					f.write(str(dataZC[i][-1][k]))
					f.write('\t')
					if (k%5 == 4):
						f.write('\n')

				f.write('\n\n')


		print("火焰面文件已生成\n")
		print("文件为%s\n"%(os.getcwd() + '\\' +flaName))


	