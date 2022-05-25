import clr

#添加dll引用
clr.AddReference('IdeaOptics') 
from IdeaOptics import Wrapper

#创建光谱仪对象
wrapper = Wrapper()

#获取已连接的光谱仪数
spec_num = wrapper.OpenAllSpectrometers() 
print("已连接光谱仪数量:" + str(spec_num))

#获取光谱仪名字
name = wrapper.getName(0)
print("光谱仪名字:" + name)

#获取光谱仪序列号
serial_num = wrapper.getSerialNumber(0)
print("光谱仪序列号:" + serial_num)

#获取光谱仪像素数
pixels = wrapper.getNumberOfPixels(0)
print("光谱仪像素数:" + str(pixels))

#设置平滑次数
wrapper.setBoxcarWidth(0,3)
print("设置平滑次数：3次")

#设置积分时间
wrapper.setIntegrationTime(0,100)
print("设置积分时间:100ms")

#设置平均次数
wrapper.setScansToAverage(0,3)
print("设置平均次数:3次")

#获取波长值
wavelengths = wrapper.getWavelengths(0)
print("最小波长值:"+str(wavelengths[0]))
print("最大波长值:"+str(wavelengths[len(wavelengths)-1]))

#是否支持制冷
istec = wrapper.isTECControl(0)
if istec:
    print("支持制冷")
    #设置制冷温度
    wrapper.setDetectorSetPointCelsius(0,-10)
    print("设置制冷温度：-10度")

    #获取制冷温度
    temp = wrapper.getFeatureControllerBoardTemperature(0)
    print("当前温度：" + str(temp))
else:
    print("不支持制冷")
#获取光谱值
specs = wrapper.getSpectrum(0)
print("波长"+str(wavelengths[0])+ "对应的强度值:" + str(specs[0]))

