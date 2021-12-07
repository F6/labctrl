# Linear Stage KXL06100

控制小平移台的 web API

银色的那个小平移台，型号 KXL06100, 日本 Suruga Seiki 产。附件只安装了零点光电开关

驱动器连的是 Autonics KR-55MC，拨码开关设定为

    TEST: OFF
    1/2CLK: OFF
    CURRENT DOWN: OFF
    CHECK FUNCTION: OFF

    MS1: 8
    MS2: 0
    RUN CURRENT: 3
    STOP CURRENT: 3


由北京阿尔泰的 usb1020 工控板控制。控制板说明书见 docs。测试之后感觉加速度最多给到 5000, 倍率30倍, 超过可能会抖

注意阿尔泰的驱动和软件都比较山寨，驱动无签名，在 windows10 上容易掉，最好单独用一台小电脑装上之后关掉更新，只用内网 web API 访问。驱动安装软件打包环境是 gb2312 或者 gbk 之类，在英文 windows 上安装和使用会乱码，可以模拟解决。

这款驱动板没有提供官方 python 库, 但给了头文件和 dll, 因此我根据头文件生成了相应的 python 库, 即 USB1020_64.py, 使用的时候, 需要和 USB1020_64.dll 放在一起. USB1020_64.h 放在这里主要用来参考, 并无实际作用, 可以删除.

