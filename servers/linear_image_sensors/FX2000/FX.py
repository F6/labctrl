import clr

#添加dll引用
clr.AddReference('IdeaOptics') 
from IdeaOptics import Wrapper


class FX2000:
    def __init__(self) -> None:
        self.wrapper = Wrapper()
        
        #获取已连接的光谱仪数
        self.spec_num = self.wrapper.OpenAllSpectrometers() 
        print("已连接光谱仪数量:" + str(self.spec_num))

        #获取光谱仪名字
        self.name = self.wrapper.getName(0)
        print("光谱仪名字:" + self.name)

        #获取光谱仪序列号
        self.serial_num = self.wrapper.getSerialNumber(0)
        print("光谱仪序列号:" + self.serial_num)

        #获取光谱仪像素数
        self.pixels = self.wrapper.getNumberOfPixels(0)
        print("光谱仪像素数:" + str(self.pixels))

        #获取波长值
        self.wavelengths = list(self.wrapper.getWavelengths(0))
        print("最小波长值:"+str(self.wavelengths[0]))
        print("最大波长值:"+str(self.wavelengths[-1]))

        #是否支持制冷
        istec = self.wrapper.isTECControl(0)
        if istec:
            print("支持制冷")
            #设置制冷温度
            self.wrapper.setDetectorSetPointCelsius(0,-10)
            print("设置制冷温度：-10度")

            #获取制冷温度
            temp = self.wrapper.getFeatureControllerBoardTemperature(0)
            print("当前温度：" + str(temp))
        else:
            print("不支持制冷")

    def set_boxcar_width(self, n):
        #设置平滑次数
        self.wrapper.setBoxcarWidth(0,n)
        print("设置平滑次数：{n}次".format(n=n))

    def set_integration_time(self, t):
        #设置积分时间
        self.wrapper.setIntegrationTime(0,t)
        print("设置积分时间:{t}ms".format(t=t))

    def set_average_times(self, n):
        #设置平均次数
        self.wrapper.setScansToAverage(0,n)
        print("设置平均次数:{n}次".format(n=n))

    def get_spectrum(self):
        #获取光谱值
        specs = list(self.wrapper.getSpectrum(0))
        return specs

spectrometer = FX2000()


