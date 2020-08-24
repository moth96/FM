import tkinter as tk
import os

def run1():
    str1 = '''
############
# Numerics #
############

#### Newton solver ####

#TimeDepFlag = TRUE
DeltaTStart = 1.0e-4

DampFlag = TRUE
LambdaMin = 1.0e-2

UseNumericalJac is TRUE
#UseSecOrdJac is TRUE
UseModifiedNewton = TRUE

MaxIter = 50
TolRes = 1.0e-12
TolDy = 1.0e-8


#### grid ####

DeltaNewGrid = 15
'''

    if samemesh.get() == 1:
        str2 = '''#OneSoluOneGrid is TRUE'''
    else:
        str2 = '''OneSoluOneGrid is TRUE'''
    
    str3 = '''
initialgridpoints = %s
maxgridpoints = %s
q = -0.25
R = 60


########################
# Sensitivity Analysis #
########################

ReactionFluxAnal is TRUE

'''%(mesh_number.get(),mesh_number.get())

    str4 = '''

#######
# I/O #
#######

OutputPath is ./%s

WriteRes is TRUE
#WriteFullRes is TRUE
WriteEverySolution is TRUE

StartProfilesFile is ./%s

#############
# Chemistry #
#############

globalReaction is NC7H16 + 11O2 == 8H2O + 7CO2;
MechanismFile is nHeptane_68.pre

fuel is NC7H16
oxidizer is O2

#########
# Flame #
#########

Flame is CounterFlowDiffusion
#StrainRate = 100
'''%(outputfile.get(),startfile.get())

    if ArclengthCont.get() == 1:
        str5 = "ArclengthCont = TRUE"
    else:
        str5 = "#ArclengthCont = TRUE"
        
    str6 = '''
ConstLewisNumber is TRUE
LewisNumberFile is LewisNumberOne
Flame is Counterflow Diffusion in Mixture Fraction Space

'''

    chists = dissipationrate.get('1.0','1.end')
    chists = chists.split(" ")
    str7 = ""
    for i in chists:
        str6 = str6 + "Scalar DissipationRate = %s \n" %i
        
    str8 = '''
#ComputeWithRadiation is TRUE

pressure = %s

#######################
# Boundary conditions #
#######################

#ToSpecies N2
#FromSpecies NC7H16
#ContType is Temperature
#ContInc = -10
#ContSide is left
#ContBound = 330

Fuel Side {
	dirichlet {
		t = %s
		y->NC7H16 = 1
	}
}
			
Oxidizer Side {
	dirichlet {
		t = %s
        x->co2 = %s
		x->o2 = %s
		x->n2 = %s
	}
}

''' %(pressure.get(),fuel_temp.get(),air_temp.get(),m_co2.get(),m_o2.get(),m_n2.get())

    fm = str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8

    with open("fm.txt","w") as f:
        f.write(fm)
    print("网格数目为：%s" %mesh_number.get())
    print(samemesh.get())
    print("输出文件目录为：%s" %outputfile.get())
    print("初始化文件为：%s" %startfile.get())
    print(ArclengthCont.get())
    print("标量耗散率为:%s" %dissipationrate.get('1.0','1.end'))
    print("压力为:%s" %pressure.get())
    print("燃料口温度：%s" %fuel_temp.get())
    print("氧化剂组分温度：%s" %air_temp.get())
    print(m_n2.get())
    print(m_o2.get())
    print(m_co2.get())
    print(m_h2o.get())

def run2():

    bat = '''
    @CD "%~dp0"
    @CALL Bin\\bin\\Source.BAT 1

    @ECHO. 
    @ECHO Run steady diffusion flames...
    @ECHO.
    @ECHO.

    @ECHO.
    @ECHO.
    @ECHO.
    @ECHO ###################################
    @ECHO #  Running examples for NHeptane  #
    @ECHO ###################################
    @ECHO.
    @ECHO.
    @ECHO.

    @ECHO.
    @ECHO.
    @ECHO.
    @ECHO Running 1st case...
    @ECHO.
    @ECHO.
    @ECHO.
    "%FM_BIN%\\FlameMan.exe" -i fm.txt
    pause
    '''
    with open("run.bat","w") as f:
        f.write(bat)

    os.system("C:\\FlameMaster\\run.bat")  

    
root = tk.Tk()
root.title("FlameMaster")
#窗口大小
root.geometry('360x480')    

#网格数目设置，默认值为100
tk.Label(root,text='网格数目:',relief=tk.FLAT).place(relx=0.05,rely=0)
mesh_number = tk.Entry(root)
mesh_number.place(relx=0.4,y=0)
mesh_number.insert(0,'100')

#选择是否使用同一套网格，是返回var.get()值为1，否返回0
tk.Label(root,text='是否使用同一套网格:').place(relx=0.05,rely=0.05)
samemesh = tk.IntVar()
rd1 = tk.Radiobutton(root,text="是",variable=samemesh,value=1)
rd1.place(relx=0.4,rely=0.05)
rd2 = tk.Radiobutton(root,text="否",variable=samemesh,value=0)
rd2.place(relx=0.5,rely=0.05)

#输出文件目录 默认为Out
tk.Label(root,text='输出文件目录：').place(relx=0.05,rely=0.1)
outputfile = tk.Entry(root)
outputfile.place(relx=0.4,rely=0.1)
outputfile.insert(0,'Out')

#选择初始化文件 
tk.Label(root,text='初始化文件为：').place(relx=0.05,rely=0.15)
startfile = tk.Entry(root)
startfile.place(relx=0.4,rely=0.15)
startfile.insert(0,'NC7H16_p01_0chi0.001tf0373to0330')

#选择是否使用弧长延拓法，若不使用返回0，FM将按照给定的耗散率进行计算，若使用返回1，FM将自动求解完整的S曲线
tk.Label(root,text='是否使用弧长延拓法:').place(relx=0.05,rely=0.20)
ArclengthCont = tk.IntVar()
rd1 = tk.Radiobutton(root,text="是",variable=ArclengthCont,value=1)
rd1.place(relx=0.4,rely=0.20)
rd2 = tk.Radiobutton(root,text="否",variable=ArclengthCont,value=0)
rd2.place(relx=0.5,rely=0.20)

#输入边界条件
#压力
tk.Label(root,text='压力：').place(relx=0.05,rely=0.25)
pressure = tk.Entry(root)
pressure.place(relx=0.4,rely=0.25)
pressure.insert(0,'101325')
#燃料口
tk.Label(root,text='燃料口温度').place(relx=0.05,rely=0.3)
tk.Label(root,text='温度：').place(relx=0.05,rely=0.35)
fuel_temp = tk.Entry(root)
fuel_temp.place(relx=0.4,rely=0.35)
fuel_temp.insert(0,'373')
#氧化剂口
tk.Label(root,text='氧化剂组分温度').place(relx=0.05,rely=0.4)
tk.Label(root,text='温度：').place(relx=0.05,rely=0.45)
air_temp = tk.Entry(root)
air_temp.place(relx=0.4,rely=0.45)
air_temp.insert(0,'330')
tk.Label(root,text='组分:').place(relx=0.05,rely=0.5)
tk.Label(root,text='N2').place(relx=0.3,rely=0.5)
tk.Label(root,text='O2').place(relx=0.3,rely=0.55)
tk.Label(root,text='CO2').place(relx=0.3,rely=0.6)
tk.Label(root,text='H2O').place(relx=0.3,rely=0.65)
m_n2 = tk.Entry(root)
m_o2 = tk.Entry(root)
m_co2 = tk.Entry(root)
m_h2o = tk.Entry(root)
m_n2.place(relx=0.4,rely=0.5)
m_o2.place(relx=0.4,rely=0.55)
m_co2.place(relx=0.4,rely=0.6)
m_h2o.place(relx=0.4,rely=0.65)
m_n2.insert(0,'0.730567729')
m_o2.insert(0,'0.153459965')
m_co2.insert(0,'0.115972306')
m_h2o.insert(0,'0')

#输入要计算的标量耗散率
tk.Label(root,text='请输入要计算的标量耗散率:').place(relx=0.05,rely=0.75)
dissipationrate = tk.Text(root)
dissipationrate.place(relx=0.05,rely=0.8,relheight=0.1,relwidth=0.9)
dissipationrate.insert(tk.INSERT,'0.001 0.01 0.1 1 2 3 5 10 30 100')

btn1 = tk.Button(root, text='生成input文件', command=run1)
btn1.place(relx=0.2, rely=0.92, relwidth=0.3, relheight=0.05)

btn2 = tk.Button(root, text='开始计算', command=run2)
btn2.place(relx=0.6, rely=0.92, relwidth=0.2, relheight=0.05)



root.mainloop()



'''
############
# Numerics #
############

#### Newton solver ####

#TimeDepFlag = TRUE
DeltaTStart = 1.0e-4

DampFlag = TRUE
LambdaMin = 1.0e-2

UseNumericalJac is TRUE
#UseSecOrdJac is TRUE
UseModifiedNewton = TRUE

MaxIter = 50
TolRes = 1.0e-12
TolDy = 1.0e-8

#### grid ####

DeltaNewGrid = 15
#OneSoluOneGrid is TRUE
initialgridpoints = 498
maxgridpoints = 498
q = -0.25
R = 60


########################
# Sensitivity Analysis #
########################

ReactionFluxAnal is TRUE

#######
# I/O #
#######

OutputPath is ./Out

WriteRes is TRUE
#WriteFullRes is TRUE
WriteEverySolution is TRUE

StartProfilesFile is ./NC7H16_p01_0chi0.001tf0373to0330

#############
# Chemistry #
#############

globalReaction is NC7H16 + 11O2 == 8H2O + 7CO2;
MechanismFile is nHeptane_68.pre

fuel is NC7H16
oxidizer is O2

#########
# Flame #
#########

Flame is CounterFlowDiffusion
#StrainRate = 100

ArclengthCont = TRUE
ConstLewisNumber is TRUE
LewisNumberFile is LewisNumberOne

Flame is Counterflow Diffusion in Mixture Fraction Space

Scalar DissipationRate = 0.001
Scalar DissipationRate = 0.002
Scalar DissipationRate = 0.003
Scalar DissipationRate = 0.004
Scalar DissipationRate = 0.005
Scalar DissipationRate = 0.006
Scalar DissipationRate = 0.007
Scalar DissipationRate = 0.008
Scalar DissipationRate = 0.009
Scalar DissipationRate = 0.01
Scalar DissipationRate = 0.02
Scalar DissipationRate = 0.03
Scalar DissipationRate = 0.04
Scalar DissipationRate = 0.05
Scalar DissipationRate = 0.06
Scalar DissipationRate = 0.07
Scalar DissipationRate = 0.08
Scalar DissipationRate = 0.09
Scalar DissipationRate = 0.1
Scalar DissipationRate = 0.2
Scalar DissipationRate = 0.3
Scalar DissipationRate = 0.4
Scalar DissipationRate = 0.5
Scalar DissipationRate = 0.6
Scalar DissipationRate = 0.7
Scalar DissipationRate = 0.8
Scalar DissipationRate = 0.9
Scalar DissipationRate = 1.0
Scalar DissipationRate = 1.1
Scalar DissipationRate = 1.2
Scalar DissipationRate = 1.3
Scalar DissipationRate = 1.4
Scalar DissipationRate = 1.5
Scalar DissipationRate = 1.6
Scalar DissipationRate = 1.7
Scalar DissipationRate = 1.8
Scalar DissipationRate = 1.9
Scalar DissipationRate = 2.0
Scalar DissipationRate = 2.1
Scalar DissipationRate = 2.2
Scalar DissipationRate = 2.3
Scalar DissipationRate = 2.4
Scalar DissipationRate = 2.5
Scalar DissipationRate = 2.6
Scalar DissipationRate = 2.7
Scalar DissipationRate = 2.8
Scalar DissipationRate = 2.9
Scalar DissipationRate = 3
Scalar DissipationRate = 5
Scalar DissipationRate = 10
Scalar DissipationRate = 30
Scalar DissipationRate = 50
Scalar DissipationRate = 100
Scalar DissipationRate = 1000



#ComputeWithRadiation is TRUE

pressure = 1.0e5

#######################
# Boundary conditions #
#######################

#ToSpecies N2
#FromSpecies NC7H16
#ContType is Temperature
#ContInc = -10
#ContSide is left
#ContBound = 330

Fuel Side {
	dirichlet {
		t = 373
		y->NC7H16 = 1.0
	}
}
			
Oxidizer Side {
	dirichlet {
		t = 330
        x->co2 = 0.115972306
		x->o2 = 0.153459965
		x->n2 = 0.730567729
	}
}


'''