/******************** (C) COPYRIGHT 2013 宁波研宏科技有限公司 *****************
* File Name          : adhon_PMC_Lib.h
* Author             : WangJiangZhu
* Version            : V1.0.0
* Date               : 9/24/2014
* Description        : pmc控制器软件开发接口
* Modify Record      :
*******************************************************************************/
#ifndef __PMC_56MT6_LIB_INTERFACE_H__
#define __PMC_56MT6_LIB_INTERFACE_H__

#ifdef  __cplusplus
extern "C" {
#endif

#ifdef _USRDLL
    #define ADHON_PMC_LIB_API  __declspec(dllexport)
#else
    #define ADHON_PMC_LIB_API  __declspec(dllimport)
#endif

/* 错误码定义 */
#define     SUCCEED                     0    //操作成功
#define     FAILED                      1    //操作失败
#define     OPEN_SERICAL_FAIL           2    //打开串口失败
#define     RECEIVE_FAILED              3    //从串口读取数据失败
#define     SEND_FAILED                 4    //发送数据失败
#define     INVALID_PAR                 5    //用户输入参数非法
#define     ERR_CANNOT_EXCUTE_COMMAND   6    //命令执行失败

//下载单个命令失败
#define     ERR_DOWNLOAD_ONE_FAILED     2


/* 程序运行模式 */
typedef enum tagProgramWorkMod
{
    WORK_MODE_PROGRAM     = 1,       /* 程序运行模式 */
    WORK_MODE_COMMAND     = 2,       /* PC命令执行方式 */
    WORK_MODE_DOWN        = 3,       /* 应用程序下载 */
    WORK_MODE_STEP        = 4        /* 单步仿真模式 */
}PROGRAM_WORK_MODE_E;

/* 移动轴类型定义 */
typedef enum tagAxisType
{
    AXIS_X                = 1,
    AXIS_Y                = 2,
    AXIS_Z                = 4,
    AXIS_U                = 8,
    AXIS_V                = 16,
    AXIS_W                = 32
}AXIS_TYPE_E;

/* 编码器的作用 */
typedef enum tagControlForType
{
    CONTROL_FOR_NONE            = 0,
    CONTROL_FOR_SPEED_SYNC_X    = 1,
    CONTROL_FOR_POS_SYNC_X      = 2,
    CONTROL_FOR_CLOSED_CTRL_X   = 3,
    CONTROL_FOR_READ_SPEED_X    = 4,
    CONTROL_FOR_READ_POS_X      = 5,
    CONTROL_FOR_SPEED_SYNC_Y    = 6,
    CONTROL_FOR_POS_SYNC_Y      = 7,
    CONTROL_FOR_CLOSED_CTRL_Y   = 8,
    CONTROL_FOR_READ_SPEED_Y    = 9,
    CONTROL_FOR_READ_POS_Y      = 10,
    CONTROL_FOR_SPEED_SYNC_Z    = 11,
    CONTROL_FOR_POS_SYNC_Z      = 12,
    CONTROL_FOR_CLOSED_CTRL_Z   = 13,
    CONTROL_FOR_READ_SPEED_Z    = 14,
    CONTROL_FOR_READ_POS_Z      = 15,
    CONTROL_FOR_SPEED_SYNC_A    = 16,
    CONTROL_FOR_POS_SYNC_A      = 17,
    CONTROL_FOR_CLOSED_CTRL_A   = 18,
    CONTROL_FOR_READ_SPEED_A    = 19,
    CONTROL_FOR_READ_POS_A      = 20,
    CONTROL_FOR_SPEED_SYNC_B    = 21,
    CONTROL_FOR_POS_SYNC_B      = 22,
    CONTROL_FOR_CLOSED_CTRL_B   = 23,
    CONTROL_FOR_READ_SPEED_B    = 24,
    CONTROL_FOR_READ_POS_B      = 25,
    CONTROL_FOR_SPEED_SYNC_C    = 26,
    CONTROL_FOR_POS_SYNC_C      = 27,
    CONTROL_FOR_CLOSED_CTRL_C   = 28,
    CONTROL_FOR_READ_SPEED_C    = 29,
    CONTROL_FOR_READ_POS_C      = 30
}CONTROL_FOR_TYPE_E;

/*===========================================
          modbus 协议定义的地址信息
===========================================*/

/*====================================================
Modbus Memory:

System Parameter Memory:
0 -- 100

Modbus保存在
101 -- 10240

后续用户代码与视教功能保存在
10240 = 10K后面进行保存用户程序
====================================================*/
#define MODBUS_MAX_LEN      256
#define MODBUS_MIN_LEN      8
#define MODBUS_TIME_OVER    4
#define MAX_USER_POINT      200
#define MOTOR_HISTORY_POS_X 6000
#define MOTOR_HISTORY_POS_Y 6100
#define MOTOR_HISTORY_POS_Z 6200

/*====================================================
Modbus Memory:

System Parameter Memory:
0 -- 100

Modbus保存在
101 -- 10240

后续用户代码与视教功能保存在
10240 = 10K后面进行保存用户程序
====================================================*/

#define MODBUS_MAX_LEN      256
#define MODBUS_MIN_LEN      8
#define MODBUS_TIME_OVER    4
#define MAX_USER_POINT      200

/*=============================
         高速脉冲变量
=============================*/
#define MOTOR_HIGH_FRE_IN1  6300
#define MOTOR_HIGH_FRE_IN2  6302
#define MOTOR_HIGH_FRE_IN3  6304
#define MOTOR_HIGH_FRE_IN4  6306
#define MOTOR_HIGH_FRE_IN5  6308
#define MOTOR_HIGH_FRE_IN6  6310
#define MOTOR_PLUS_CNT_IN1  6312
#define MOTOR_PLUS_CNT_IN2  6314
#define MOTOR_PLUS_CNT_IN3  6316
#define MOTOR_PLUS_CNT_IN4  6318
#define MOTOR_PLUS_CNT_IN5  6320
#define MOTOR_PLUS_CNT_IN6  6322

/*==============================
    定时器剩余时间相关数据
==============================*/
#define DM_REMAIN_TIMER_0       6400  //定时器0的剩余值
#define DM_REMAIN_TIMER_1       6402
#define DM_REMAIN_TIMER_2       6404
#define DM_REMAIN_TIMER_3       6406
#define DM_REMAIN_TIMER_4       6408
#define DM_REMAIN_TIMER_5       6410
#define DM_REMAIN_TIMER_6       6412
#define DM_REMAIN_TIMER_7       6414

/*==============================
       编码器相关数据定义
==============================*/
#define DM_ENCODER_READ_SPEED_X      6450
#define DM_ENCODER_READ_SPEED_Y      6452
#define DM_ENCODER_READ_SPEED_Z      6454
#define DM_ENCODER_READ_SPEED_A      6456
#define DM_ENCODER_READ_SPEED_B      6458
#define DM_ENCODER_READ_SPEED_C      6460
#define DM_ENCODER_READ_POSITION_X   6462
#define DM_ENCODER_READ_POSITION_Y   6464
#define DM_ENCODER_READ_POSITION_Z   6466
#define DM_ENCODER_READ_POSITION_A   6468
#define DM_ENCODER_READ_POSITION_B   6470
#define DM_ENCODER_READ_POSITION_C   6472

/*=============================
   外设一些实时测量值的读取
==============================*/
#define DM_AD_VALUE_1       6500
#define DM_AD_VALUE_2       6502

//Coil相关宏定义
#define  COIL_COMMON_IO_IN   0
#define  COIL_IN1_ADDR       COIL_COMMON_IO_IN + 1
#define  COIL_IN2_ADDR       COIL_COMMON_IO_IN + 2
#define  COIL_IN3_ADDR       COIL_COMMON_IO_IN + 3
#define  COIL_IN4_ADDR       COIL_COMMON_IO_IN + 4
#define  COIL_IN5_ADDR       COIL_COMMON_IO_IN + 5
#define  COIL_IN6_ADDR       COIL_COMMON_IO_IN + 6
#define  COIL_IN7_ADDR       COIL_COMMON_IO_IN + 7
#define  COIL_IN8_ADDR       COIL_COMMON_IO_IN + 8
#define  COIL_IN9_ADDR       COIL_COMMON_IO_IN + 9
#define  COIL_IN10_ADDR      COIL_COMMON_IO_IN + 10
#define  COIL_IN11_ADDR      COIL_COMMON_IO_IN + 11
#define  COIL_IN12_ADDR      COIL_COMMON_IO_IN + 12
#define  COIL_IN13_ADDR      COIL_COMMON_IO_IN + 13
#define  COIL_IN14_ADDR      COIL_COMMON_IO_IN + 14
#define  COIL_IN15_ADDR      COIL_COMMON_IO_IN + 15
#define  COIL_IN16_ADDR      COIL_COMMON_IO_IN + 16
#define  COIL_IN17_ADDR      COIL_COMMON_IO_IN + 17
#define  COIL_IN18_ADDR      COIL_COMMON_IO_IN + 18
#define  COIL_IN19_ADDR      COIL_COMMON_IO_IN + 19
#define  COIL_IN20_ADDR      COIL_COMMON_IO_IN + 20
#define  COIL_IN21_ADDR      COIL_COMMON_IO_IN + 21
#define  COIL_IN22_ADDR      COIL_COMMON_IO_IN + 22
#define  COIL_IN23_ADDR      COIL_COMMON_IO_IN + 23
#define  COIL_IN24_ADDR      COIL_COMMON_IO_IN + 24
#define  COIL_IN25_ADDR      COIL_COMMON_IO_IN + 25
#define  COIL_IN26_ADDR      COIL_COMMON_IO_IN + 26
#define  COIL_IN27_ADDR      COIL_COMMON_IO_IN + 27
#define  COIL_IN28_ADDR      COIL_COMMON_IO_IN + 28
#define  COIL_IN29_ADDR      COIL_COMMON_IO_IN + 29
#define  COIL_IN30_ADDR      COIL_COMMON_IO_IN + 30
#define  COIL_IN31_ADDR      COIL_COMMON_IO_IN + 31
#define  COIL_IN32_ADDR      COIL_COMMON_IO_IN + 32

#define  COIL_COMMON_IO_OUT  32
#define  COIL_OUT1_ADDR      COIL_COMMON_IO_OUT + 1
#define  COIL_OUT2_ADDR      COIL_COMMON_IO_OUT + 2
#define  COIL_OUT3_ADDR      COIL_COMMON_IO_OUT + 3
#define  COIL_OUT4_ADDR      COIL_COMMON_IO_OUT + 4
#define  COIL_OUT5_ADDR      COIL_COMMON_IO_OUT + 5
#define  COIL_OUT6_ADDR      COIL_COMMON_IO_OUT + 6
#define  COIL_OUT7_ADDR      COIL_COMMON_IO_OUT + 7
#define  COIL_OUT8_ADDR      COIL_COMMON_IO_OUT + 8
#define  COIL_OUT9_ADDR      COIL_COMMON_IO_OUT + 9
#define  COIL_OUT10_ADDR     COIL_COMMON_IO_OUT + 10
#define  COIL_OUT11_ADDR     COIL_COMMON_IO_OUT + 11
#define  COIL_OUT12_ADDR     COIL_COMMON_IO_OUT + 12
#define  COIL_OUT13_ADDR     COIL_COMMON_IO_OUT + 13
#define  COIL_OUT14_ADDR     COIL_COMMON_IO_OUT + 14
#define  COIL_OUT15_ADDR     COIL_COMMON_IO_OUT + 15
#define  COIL_OUT16_ADDR     COIL_COMMON_IO_OUT + 16
#define  COIL_OUT17_ADDR     COIL_COMMON_IO_OUT + 17
#define  COIL_OUT18_ADDR     COIL_COMMON_IO_OUT + 18
#define  COIL_OUT19_ADDR     COIL_COMMON_IO_OUT + 19
#define  COIL_OUT20_ADDR     COIL_COMMON_IO_OUT + 20
#define  COIL_OUT21_ADDR     COIL_COMMON_IO_OUT + 21
#define  COIL_OUT22_ADDR     COIL_COMMON_IO_OUT + 22
#define  COIL_OUT23_ADDR     COIL_COMMON_IO_OUT + 23
#define  COIL_OUT24_ADDR     COIL_COMMON_IO_OUT + 24

#define  COIL_MOTOR_COIL     60
//电机状态定制
#define  COIL_MOTOR_X_DIR    COIL_MOTOR_COIL + 1  //0标识向左，1标识向右
#define  COIL_MOTOR_Y_DIR    COIL_MOTOR_COIL + 2  //0标识向左，1标识向右
#define  COIL_MOTOR_Z_DIR    COIL_MOTOR_COIL + 3  //0标识向左，1标识向右
#define  COIL_MOTOR_A_DIR    COIL_MOTOR_COIL + 4  //0标识向左，1标识向右
#define  COIL_MOTOR_B_DIR    COIL_MOTOR_COIL + 5  //0标识向左，1标识向右
#define  COIL_MOTOR_C_DIR    COIL_MOTOR_COIL + 6  //0标识向左，1标识向右
#define  COIL_MOTOR_X_S      COIL_MOTOR_COIL + 7  //0标识电机停止,1标识电机在运行
#define  COIL_MOTOR_Y_S      COIL_MOTOR_COIL + 8  //0标识电机停止,1标识电机在运行
#define  COIL_MOTOR_Z_S      COIL_MOTOR_COIL + 9  //0标识电机停止,1标识电机在运行
#define  COIL_MOTOR_A_S      COIL_MOTOR_COIL + 10  //0标识电机停止,1标识电机在运行
#define  COIL_MOTOR_B_S      COIL_MOTOR_COIL + 11  //0标识电机停止,1标识电机在运行
#define  COIL_MOTOR_C_S      COIL_MOTOR_COIL + 12  //0标识电机停止,1标识电机在运行
#define  COIL_MOTOR_LEFT_X   COIL_MOTOR_COIL + 13  //启动电机手动向左运行
#define  COIL_MOTOR_RIGHT_X  COIL_MOTOR_COIL + 14  //启动电机手动向右运行
#define  COIL_MOTOR_LEFT_Y   COIL_MOTOR_COIL + 15  //启动电机手动向左运行
#define  COIL_MOTOR_RIGHT_Y  COIL_MOTOR_COIL + 16  //启动电机手动向右运行
#define  COIL_MOTOR_LEFT_Z   COIL_MOTOR_COIL + 17  //启动电机手动向左运行
#define  COIL_MOTOR_RIGHT_Z  COIL_MOTOR_COIL + 18  //启动电机手动向右运行
#define  COIL_MOTOR_LEFT_A   COIL_MOTOR_COIL + 19  //启动电机手动向左运行
#define  COIL_MOTOR_RIGHT_A  COIL_MOTOR_COIL + 20  //启动电机手动向右运行
#define  COIL_MOTOR_LEFT_B   COIL_MOTOR_COIL + 21  //启动电机手动向左运行
#define  COIL_MOTOR_RIGHT_B  COIL_MOTOR_COIL + 22  //启动电机手动向右运行
#define  COIL_MOTOR_LEFT_C   COIL_MOTOR_COIL + 23  //启动电机手动向左运行
#define  COIL_MOTOR_RIGHT_C  COIL_MOTOR_COIL + 24  //启动电机手动向右运行
#define  COIL_MOTOR_CLEAR_X  COIL_MOTOR_COIL + 25  //X轴位置清零
#define  COIL_MOTOR_CLEAR_Y  COIL_MOTOR_COIL + 26  //Y轴位置清零
#define  COIL_MOTOR_CLEAR_Z  COIL_MOTOR_COIL + 27  //Z轴位置清零
#define  COIL_MOTOR_CLEAR_A  COIL_MOTOR_COIL + 28  //A轴位置清零
#define  COIL_MOTOR_CLEAR_B  COIL_MOTOR_COIL + 29  //B轴位置清零
#define  COIL_MOTOR_CLEAR_C  COIL_MOTOR_COIL + 30  //C轴位置清零

#define  COIL_PERICAL_STATUS  100
#define  COIL_PWM_1_STATUS   (COIL_PERICAL_STATUS + 1) //PWM1外设操作
#define  COIL_PWM_2_STATUS   (COIL_PERICAL_STATUS + 2) //PWM2外设操作
#define  COIL_LIMIT_TRIGER_LEVEL    (COIL_PERICAL_STATUS + 10) //限位开关的电平信息

#define  SYSTEM_OTHER_COIL   150
/* 系统参数位定义 */
#define  COIL_SYS_PAUSE      SYSTEM_OTHER_COIL + 1  //暂停
#define  COIL_SYS_CONTINUE   SYSTEM_OTHER_COIL + 2  //继续运行
#define  COIL_SYS_RESET      SYSTEM_OTHER_COIL + 3  //复位
#define  COIL_SET_STEP_MODE  SYSTEM_OTHER_COIL + 4  //设置为单步工作模式
#define  COIL_RUN_STEP_CODE  SYSTEM_OTHER_COIL + 5  //单步运行一行
#define  COIL_EARSE_DM_DATA  SYSTEM_OTHER_COIL + 6  //将用户区的DM值全部清空，赋值为0

/* 视教功能相关变量 */
#define  COIL_VIDEO_TEACH_BEGIN    SYSTEM_OTHER_COIL + 7   //启动视教录屏功能
#define  COIL_VIDEO_TEACH_END      SYSTEM_OTHER_COIL + 8   //停止视教录屏功能
#define  COIL_VIDEO_SAVE_POINT     SYSTEM_OTHER_COIL + 9   //保存一个录屏点

/* 用户模拟输入输出按键 */
#define  COIL_SIMULATE_INPUT_1     SYSTEM_OTHER_COIL + 10
#define  COIL_SIMULATE_INPUT_32    SYSTEM_OTHER_COIL + 41

#define  COIL_CUSTOM_DEFINE        200  //用户自定义,其中前面的32个虚拟位可以作为虚拟按键

/* 常用DM数据区表 */
#define  DM_MOTOR_ACC_X      1   //SHORT
#define  DM_MOTOR_ACC_Y      2   //SHORT
#define  DM_MOTOR_ACC_Z      3   //SHORT
#define  DM_MOTOR_ACC_A      4   //SHORT
#define  DM_MOTOR_ACC_B      5   //SHORT
#define  DM_MOTOR_ACC_C      6   //SHORT
#define  DM_MOTOR_DEC_X      7   //SHORT
#define  DM_MOTOR_DEC_Y      8   //SHORT
#define  DM_MOTOR_DEC_Z      9   //SHORT
#define  DM_MOTOR_DEC_A      10  //SHORT
#define  DM_MOTOR_DEC_B      11  //SHORT
#define  DM_MOTOR_DEC_C      12  //SHORT
#define  DM_MOTOR_PITH_X     13  //FLOAT
#define  DM_MOTOR_PITH_Y     15  //FLOAT
#define  DM_MOTOR_PITH_Z     17  //FLOAT
#define  DM_MOTOR_PITH_A     19  //FLOAT
#define  DM_MOTOR_PITH_B     21  //FLOAT
#define  DM_MOTOR_PITH_C     23  //FLOAT
#define  DM_MOTOR_DIV_X      25  //ULONG
#define  DM_MOTOR_DIV_Y      27  //ULONG
#define  DM_MOTOR_DIV_Z      29  //ULONG
#define  DM_MOTOR_DIV_A      31  //ULONG
#define  DM_MOTOR_DIV_B      33  //ULONG
#define  DM_MOTOR_DIV_C      35  //ULONG
#define  DM_MOTOR_MAX_SPD_X  37   //FLOAT
#define  DM_MOTOR_MAX_SPD_Y  39   //FLOAT
#define  DM_MOTOR_MAX_SPD_Z  41   //FLOAT
#define  DM_MOTOR_MAX_SPD_A  43   //FLOAT
#define  DM_MOTOR_MAX_SPD_B  45   //FLOAT
#define  DM_MOTOR_MAX_SPD_C  47   //FLOAT
#define  DM_MOTOR_MIN_SPD_X  49   //FLOAT X电机最小速度
#define  DM_MOTOR_MIN_SPD_Y  51   //FLOAT Y电机最小速度
#define  DM_MOTOR_MIN_SPD_Z  53   //FLOAT Z电机最小速度
#define  DM_MOTOR_MIN_SPD_A  55   //FLOAT X电机最小速度
#define  DM_MOTOR_MIN_SPD_B  57   //FLOAT Y电机最小速度
#define  DM_MOTOR_MIN_SPD_C  59   //FLOAT Z电机最小速度
#define  DM_MOTOR_POS_X      61  //FLOAT
#define  DM_MOTOR_POS_Y      63  //FLOAT
#define  DM_MOTOR_POS_Z      65  //FLOAT
#define  DM_MOTOR_POS_A      67  //FLOAT
#define  DM_MOTOR_POS_B      69  //FLOAT
#define  DM_MOTOR_POS_C      71  //FLOAT
#define  DM_MOTOR_MOVE_X     73  //FLOAT
#define  DM_MOTOR_MOVE_Y     75  //FLOAT
#define  DM_MOTOR_MOVE_Z     77  //FLOAT
#define  DM_MOTOR_MOVE_A     79  //FLOAT
#define  DM_MOTOR_MOVE_B     81  //FLOAT
#define  DM_MOTOR_MOVE_C     83  //FLOAT

//电机限位信号
#define  DM_MOTOR_LIMIT_LEFT_X  85  //USHORT
#define  DM_MOTOR_LIMIT_RIGHT_X 86  //USHORT
#define  DM_MOTOR_LIMIT_LEFT_Y  87  //USHORT
#define  DM_MOTOR_LIMIT_RIGHT_Y 88  //USHORT
#define  DM_MOTOR_LIMIT_LEFT_Z  89  //USHORT
#define  DM_MOTOR_LIMIT_RIGHT_Z 90  //USHORT
#define  DM_MOTOR_LIMIT_LEFT_A  91  //USHORT
#define  DM_MOTOR_LIMIT_RIGHT_A 92  //USHORT
#define  DM_MOTOR_LIMIT_LEFT_B  93  //USHORT
#define  DM_MOTOR_LIMIT_RIGHT_B 94  //USHORT
#define  DM_MOTOR_LIMIT_LEFT_C  95  //USHORT
#define  DM_MOTOR_LIMIT_RIGHT_C 96  //USHORT

//外设信息操作(电位器,编码器)
#define  DM_AD_MIN_1            120  //FLOAT
#define  DM_AD_MAX_1            122  //FLOAT
#define  DM_AD_MIN_2            124  //FLOAT
#define  DM_AD_MAX_2            126  //FLOAT
#define  DM_AD_MODE_1           128
#define  DM_AD_MODE_2           130
#define  DM_ENCODER_LINE_1      132
#define  DM_ENCODER_LINE_2      134
#define  DM_ENCODER_LINE_3      136
#define  DM_ENCODER_SCALE_1     138  //FLOAT
#define  DM_ENCODER_SCALE_2     140  //FLOAT
#define  DM_ENCODER_SCALE_3     142
#define  DM_ENCODER_MODE_1      144  //ULONG 编码器工作模式
#define  DM_ENCODER_MODE_2      146  //ULONG 编码器工作模式
#define  DM_ENCODER_MODE_3      148  //ULONG 编码器工作模式

//系统相关参数定义
#define  DM_CONTROL_ADDR                200  //SHORT 控制器地址信息
#define  DM_PROGRAM_NO                  201  //SHORT 应用程序编号
#define  DM_WORK_MODE                   202  //SHORT 控制器工作模式
#define  DM_PROGRAM_CODE_LINE           203  //SHORT 读取代码运行行号
#define  DM_USE_TRY_TOTAL_TIMES         204  //FLOAT 用户可以使用总时间(S)
#define  DM_USE_HAVE_RUN_TIME           206  //FLOAT 用户已经运行总时间(S)
#define  DM_USE_PASSWD                  208  //ULONG 用户原始密码

//视教功能
#define  DM_VIDEO_TEACHSTART_POINT_X    350  //FLOAT 矩形视教起始地址
#define  DM_VIDEO_TEACHSTART_POINT_Y    352  //FLOAT 矩形视教起始地址
#define  DM_VIDEO_TEACHVER_NUM          354  //SHORT 垂直点数
#define  DM_VIDEO_TEACHHER_NUM          355  //SHORT 水平点数
#define  DM_VIDEO_TEACHVER_DIST         356  //FLOAT 垂直间距
#define  DM_VIDEO_TEACHHER_DIST         358  //FLOAT 水平间距
#define  DM_VIDEO_TEACH_TOTAL_POINT     360  //USHORT 视教总点数
#define  DM_VIDEO_TEACH_CUR_POINT       361  //USHORT 水平总点数
#define  DM_VIDEO_TEACH_MASK_INPUT      362  //ULONG 哪些输入IO口状态起效
#define  DM_VIDEO_TEACH_MASK_OUTPUT     364  //ULONG 哪些输出IO口状态起效
#define  DM_VIDEO_TEACH_DELAY_TIME      366  //FLOAT 示教点操作延时时间

//应用程序尺寸,代码行数
#define  DM_MAX_USER_CNT                5
#define  DM_USER_PROGRAM_INDEX          378  //当前应用程序执行下标值
#define  DM_USER_PROGRAM_SIZE_0         380
#define  DM_USER_PROGRAM_SIZE_1         382
#define  DM_USER_PROGRAM_SIZE_2         384
#define  DM_USER_PROGRAM_SIZE_3         386
#define  DM_USER_PROGRAM_SIZE_4         387

#define  DM_CUSTOM_DEFINE               400  //用户自定义的单元从400开始
/***
   描述: 控制器全局初始化
  输入1: 无
 返回值: 初始化是否成功
*/
ADHON_PMC_LIB_API int __stdcall PMC_GlobalInit(void);

/***
   描述: 控制器全局资源释放函数
  输入1: 无
 返回值: 释放资源是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GlobalRelease(void);

/***
   描述: 打开串口
  输入1: iPort  需要打开的串口编号
 返回值: 打开端口是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_OpenSericalPort(int iPort);

/***
   描述: 关闭串口
  输入1: 无
 返回值: 无
*/
ADHON_PMC_LIB_API void __stdcall PMC_CloseSericalPort(void);

/***
   描述: 将用户程序下载到SDK中
  输入1: pucProgramData 应用程序起始地址
  输入2: usUserProgramLines 用户程序代码行
 返回值: 无
*/
ADHON_PMC_LIB_API int __stdcall PMC_SetUserProgram(unsigned char *pucProgramData, unsigned short usUserProgramLines);

/***
   描述: 将用户程序下载到控制器上面
  输入1: ucProgramIndex 下载应用程序到代码行的第几行
 返回值: 无
*/
ADHON_PMC_LIB_API int __stdcall PMC_DownLoadProgram(unsigned char ucProgramIndex);

/***
   描述: 获取控制器版本号
  输入1: ucControllerAddr 控制器地址信息
  输出2: pulVersion 控制器版本信息(前两个字节为SDK版本信息，后两位为PMC固件版本信息
                    如:0x01020502表示SDK版本为1.2版本，固件为5.2版本)
 返回值: 获取控制器版本号
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetControllerVersion(unsigned char ucControllerAddr, unsigned long *pulVersion);

/***
   描述: 设置控制器工作模式
  输入1: ucControllerAddr 控制器地址
  输入2: enWorkMode       控制器工作模式
  输入3: ucProgramIndex   暂不使用
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetWorkMode(unsigned char ucControllerAddr, PROGRAM_WORK_MODE_E enWorkMode, unsigned char ucProgramIndex);

/***
   描述: 获取控制器工作模式
  输入1: ucControllerAddr 控制器地址
  输入2: penWorkMode 控制器工作模式
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetWorkMode(unsigned char ucControllerAddr, PROGRAM_WORK_MODE_E *penWorkMode);

/***
   描述: 设置控制器地址
  输入1: ucControllerAddr 控制器原地址
  输入2: ucNewControllerAddr 控制器新地址
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetControllerAddr(unsigned char ucControllerAddr, unsigned char ucNewControllerAddr);

/***
   描述: 获取控制器地址
  输入1: pucControllerAddr 获取控制器地址
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetControllerAddr(unsigned char *pucControllerAddr);

/***
   描述: 暂停控制器运行
  输入1: ucControllerAddr 控制器地址
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_PauseController(unsigned char ucControllerAddr);

/***
   描述: 恢复控制器继续运行
  输入1: ucControllerAddr 控制器地址
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_ContinueController(unsigned char ucControllerAddr);

/***
   描述: 蜂鸣器
  输入1: ucControllerAddr 控制器地址
  输入2: ulBeepTimeMs 蜂鸣器鸣叫时间，单位为ms
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Beeper(unsigned char ucControllerAddr, unsigned long ulBeepTimeMs);

/***
   描述: 在指定端口上面输出电平
  输入1: ucControllerAddr 控制器地址
  输入2: ucOutputNo  输出端口号
  输入3: bHLevel     输出的电平值
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetIOPinLevel(unsigned char ucControllerAddr, unsigned char ucOutputNo, bool bHLevel);

/***
   描述: 读取输入端口的状态信息
  输入1: ucControllerAddr 控制器地址
  输入2: pucInputPortStatus 输入端口电平值(从低位到高位依次为:X0-X5,IN1-IN6)
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetIOPinLevel(unsigned char ucControllerAddr, unsigned char ucOutputNo, bool *pbHLevelunsigned);


/***
   描述: 获取IO口上所有的电平状态
  输入1: ucControllerAddr 控制器地址
  输入2: 开始读取的位地址
  输入3: pucInputPortStatus 输入端口电平值(从低位到高位依次为:X0-X5,IN1-IN6)
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetAllIOPinLevel(unsigned char ucControllerAddr, unsigned short usCoilAddr, unsigned long *pulAllLevel);

/***
   描述: 设置驱动器细分数
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType  操作的轴
  输入3: ulDriverDiv 驱动器细分数
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetMotorDriveDiv(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, unsigned long ulDriverDiv);

/***
   描述: 获取驱动器细分数
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType   操作的轴
  输入3: pulDriverDiv 驱动器细分数
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetMotorDriveDiv(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, unsigned long *pulDriverDiv);

/***
   描述: 设置前进的螺距
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType   操作的轴
  输入3: fPitch       螺距
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetMotorPitch(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float fPitch);

/***
   描述: 获取前进的螺距
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType   操作的轴
  输入3: pfPitch      螺距
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetMotorPitch(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float *pfPitch);

/***
   描述: 设定电机加速系数
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType   操作的轴
  输入3: ulAccPar     加速系数(数值越大加速时间越长)
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetMotorAcc(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, unsigned long ulAccPar);

/***
   描述: 获取电机加速系数
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType         操作的轴
  输入3: pulUserAccPar      电机加速系数
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetMotorAcc(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, unsigned long *pulUserAccPar);

/***
   描述: 设定电机减速系数
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType   操作的轴
  输入3: ulDecPar     减速系数(数值越大减速时间越长)
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetMotorDec(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, unsigned long ulDecPar);

/***
   描述: 获取电机减速系数
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType         操作的轴
  输入3: pulUserDecPar      电机减速系数
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetMotorDec(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, unsigned long *pulUserDecPar);

/***
   描述: 设置轴运行最大速度
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType  操作轴
  输入3: fMaxSpeed  最大速度
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetMotorMaxSpeed(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float fMaxMotorSpeed);

/***
   描述: 设置轴运行最小速度
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType  操作轴
  输入3: fMaxSpeed  最小速度
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SetMotorMinSpeed(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float fMinMotorSpeed);

/***
   描述: 获取步进电机的当前速度
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType  操作轴
  输入3: plMotorPostion 当前位置
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetMotorCurSpeed(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float *pfMotorSpeed);

/***
   描述: 设置步进电机相对运行距离
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType  操作轴
  输入3: fMoveDist   相对移动距离
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_MotorMove(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float fMoveDist);

/***
   描述: 步进电机手动左移
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType  操作轴
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_ManualLeftMove(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType);

/***
   描述: 步进电机手动右移
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType  操作轴
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_ManualRightMove(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType);


/***
   描述: 设置步进电机运行位置
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType  操作轴
  输入3: fPostion    绝对坐标
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_MotorGoPos(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float fPostion);

/***
   描述: 设置步进电机运行位置
  输入1: ucControllerAddr   控制器地址
  输入2: enAxisType  操作轴
  输入3: ucMotorLeftLimit  左限位信号
  输入4: ucMotorRightLimit 右限位信号
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall SetMotorLimitSignal(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, unsigned char ucMotorLeftLimit, unsigned char ucMotorRightLimit);


/***
   描述: 快速停止莫个电机运行
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType  操作轴
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_QuickStopMotor(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType);

/***
   描述: 平稳停止莫个电机运行
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType  操作轴
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_SlowStopMotor(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType);

/***
   描述: 判断某个电机是否在运行
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType  操作轴
 返回值: 某个电机是否在运行
*/
ADHON_PMC_LIB_API int  __stdcall PMC_MotorIsRunning(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, BOOL *pbIsRunning);

/***
   描述: 将当前位置设置为零点位置
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType       操作轴
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_ClearMotorPosition(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType);

/***
   描述: 获取当前位置
  输入1: ucControllerAddr 控制器地址
  输入2: enAxisType  操作轴
  输入3: plMotorPostion 当前位置
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_GetMotorPosition(unsigned char ucControllerAddr, AXIS_TYPE_E enAxisType, float *pfMotorPostion);

/***
   描述: 进行XY平面直线插补
  输入1: ucControllerAddr 控制器地址
  输入2: usMotorPosX  X轴相对移动的X坐标
  输入3: usMotorPosY  Y轴先对移动的Y坐标
 返回值: 操作是否成功，移动成功的为从当前位置再叠加后的位置值
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line2Move(unsigned char ucControllerAddr, float fAxis1, float fAxis2);

/***
   描述: 进行XY平面直线插补
  输入1: ucControllerAddr 控制器地址
  输入2: usMotorPosX  移动到X轴的坐标
  输入3: usMotorPosY  移动到Y轴的坐标
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line2Goto(unsigned char ucControllerAddr, float fAxis1, float fAxis2);

/***
 描述: 使用DM作为直线查补增量位置信息
输入1: ucControllerAddr 控制器地址
输入2: usMoveXDmIndex  X轴相对移动的X坐标
输入3: usMoveYDmIndex  Y轴先对移动的Y坐标
返回值: 操作是否成功，移动成功的为从当前位置再叠加后的位置值
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line2MoveDM(unsigned char ucControllerAddr, unsigned short usAxis1DmIndex,  unsigned short usAxis2DmIndex);

/***
 描述: 使用DM作为绝对位置信息
输入1: ucControllerAddr 控制器地址
输入2: usGotoXDmIndex  X轴相对移动的X坐标
输入3: usGotoYDmIndex  Y轴先对移动的Y坐标
返回值: 操作是否成功，移动成功的为从当前位置再叠加后的位置值
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line2GotoDM(unsigned char ucControllerAddr, unsigned short usAxis1DmIndex,  unsigned short usAxis2DmIndex)
;
/***
 描述: 进行XYZ平面直线插补
输入1: ucControllerAddr 控制器地址
输入2: usMotorPosX  X轴相对移动的X坐标
输入3: usMotorPosY  Y轴先对移动的Y坐标
输入4: usMotorPosZ  Z轴先对移动的Y坐标
返回值: 操作是否成功，移动成功的为从当前位置再叠加后的位置值
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line3Move(unsigned char ucControllerAddr, float fAxis1, float fAxis2, float fAxis3);

/***
 描述: 进行XYZ平面直线插补
输入1: ucControllerAddr 控制器地址
输入2: usMotorPosX  X轴相对移动的X坐标
输入3: usMotorPosY  Y轴先对移动的Y坐标
输入4: usMotorPosZ  Z轴先对移动的Y坐标
返回值: 操作是否成功，移动成功的为从当前位置再叠加后的位置值
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line3Goto(unsigned char ucControllerAddr, float fAxis1, float fAxis2, float fAxis3);

/***
 描述: 进行XY平面直线插补
输入1: ucControllerAddr 控制器地址
输入2: usMotorPosX  X轴相对移动的X坐标
输入3: usMotorPosY  Y轴先对移动的Y坐标
输入4: usMotorPosZ  Z轴先对移动的Y坐标
返回值: 操作是否成功，移动成功的为从当前位置再叠加后的位置值
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line3MoveDM(unsigned char ucControllerAddr, unsigned short usAxis1DmIndex,  unsigned short usAxis2DmIndex, unsigned short usAxis3DmIndex);

/***
 描述: 进行XY平面直线插补
输入1: ucControllerAddr 控制器地址
输入2: usMotorPosX  X轴相对移动的X坐标
输入3: usMotorPosY  Y轴先对移动的Y坐标
返回值: 操作是否成功，移动成功的为从当前位置再叠加后的位置值
*/
ADHON_PMC_LIB_API int  __stdcall PMC_Line3GotoDM(unsigned char ucControllerAddr, unsigned short usAxis1DmIndex,  unsigned short usAxis2DmIndex, unsigned short usAxis3DmIndex);

/***
   描述: 进行XY平面两点与半径进行圆弧插补(顺时针)
  输入1: ucControllerAddr 控制器地址
  输入2: sCircleRadius  圆弧半径
  输入3: usMotorPosX    目标X轴位置
  输入4: usMotorPosY    目标Y轴位置
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_CircleMoveG2_Pos(unsigned char ucControllerAddr, float fCircleRadius, float fAxis1Pos, float fAxis2Pos);

/***
   描述: 进行XY平面两点与半径进行圆弧插补(逆时针)
  输入1: ucControllerAddr 控制器地址
  输入2: usAngle        转动角度
  输入3: usCenterPosX   圆心X轴坐标
  输入4: usCenterPosY   圆心Y轴坐标
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_CircleMoveG3_Pos(unsigned char ucControllerAddr, float fAngle, float fAxis1CenterPos, float fAxis2CenterPos);


/***
 描述: 进行XY平面两点与半径进行圆弧插补(顺时针)
输入1: ucControllerAddr 控制器地址
输入2: usAngle        转动角度
输入3: usCenterPosX   圆心X轴坐标
输入4: usCenterPosY   圆心Y轴坐标
返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_CircleMoveG2_Angle(unsigned char ucControllerAddr, unsigned short usAngleDmIndex, unsigned short usCenterPos1DmIndex, unsigned short usCenterPos2DmIndex);

/***
   描述: 进行XY平面角度与圆心进行圆弧插补(逆时针)
  输入1: ucControllerAddr 控制器地址
  输入2: sCircleRadius  圆弧半径
  输入3: usMotorPosX    目标X轴位置
  输入4: usMotorPosY    目标Y轴位置
 返回值: 操作是否成功
*/
ADHON_PMC_LIB_API int  __stdcall PMC_CircleMoveG3_Angle(unsigned char ucControllerAddr, unsigned short usAngleDmIndex, unsigned short usCenterPos1DmIndex, unsigned short usCenterPos2DmIndex);

/*=======================================================
                标准外设操作指令
========================================================*/
/*
*   描述: 设置电位器的控制方式
   参数1: 指定准对哪个电位器进行设置
   参数2: 电位器的控制方式
* 返回值: 无
*/
LONG PMC_SetADWorlMode(unsigned char ucControllerAddr, unsigned char ucADNo, CONTROL_FOR_TYPE_E enControlForType);

/*
*   描述: 设置电位器的范围
   参数1: 指定准对哪个电位器进行设置
   参数2: 电位器对应的最小值
   参数3: 电位器对应的最大值
* 返回值: 无
*/
LONG PMC_SetADValueScale(unsigned char ucControllerAddr, unsigned char ucADNo, float fMinADValue, float fMaxADValue);

/*
*   描述: 读取指定电位器的值，已经根据设定的范围进行转换后的值
   参数1: 需要读取哪个电位器的值
* 返回值: 无
*/
FLOAT PMC_ReadADValue(unsigned char ucControllerAddr, unsigned char ucADNo);

/*
*   描述: 设置编码器线数，多少线的编码器
   参数1: 编码器接入的哪个编码器
   参数2: 多少线编码器
* 返回值: 无
*/
LONG PMC_SetEncodeLineNum(unsigned char ucControllerAddr, unsigned char  ucEncoderNo, unsigned long ulEncoderLineNums, float fScaleValue);

/*
*   描述: 设置编码器的工作模式
   参数1: 编码器接入的哪个编码器
   参数2: 编码器的作用或者工作方式
   参数3: 编码器与步进电机的比例系数
* 返回值: 无
*/
LONG PMC_SetEncodeMode(unsigned char ucControllerAddr, unsigned char  ucEncoderNo, CONTROL_FOR_TYPE_E enEncodeUseType);

/*=======================================================
                Modbus相关指令定义
=======================================================*/
/***
    描述: 使用串口编码打开一个串口同时读取控制器的地址信息
    输入1: 串口编码
    输入2: 链接到这个串口的控制器地址信息
*/
ADHON_PMC_LIB_API int  __stdcall  Modbus_OpenSerical(unsigned char ucSericalNo, unsigned char *pucControllerAddr);

/***
    描述: 使用串口编码打开一个串口同时读取控制器的地址信息
    输入1: 串口编码
*/
ADHON_PMC_LIB_API int  __stdcall  Modbus_CloseSerical(unsigned char ucSericalNo);


/***
    描述: 使用modbus协议进行位操作
    输入1: 控制器地址
    输入2:位操作地址
    输入3:高低电平值
*/
ADHON_PMC_LIB_API int  __stdcall  Modbus_WriteCoil(unsigned char ucControllerAddr, unsigned short usCoilAddr, bool bLevelValue);

/***
    描述: 使用modbus协议进行位操作
    输入1: 控制器地址
    输入2:控制器中通道地址，参考modbus通道定义文档
    返回值:读取的浮点数
*/
ADHON_PMC_LIB_API bool  __stdcall  Modbus_ReadCoil(unsigned char ucControllerAddr, unsigned short usChannelAddr);

/***
    描述: 使用modbus协议进行浮点数写入
    输入1: 控制器地址
    输入2:控制器中通道地址，参考modbus通道定义文档
    输入3:需要写入的浮点数
*/
ADHON_PMC_LIB_API int  __stdcall  Modbus_WriteFloat(unsigned char ucControllerAddr, unsigned short usChannelAddr, float fWriteData);

/***
    描述: 使用modbus协议进行浮点数读取
    输入1: 控制器地址
    输入2:控制器中通道地址，参考modbus通道定义文档
    返回值:读取的浮点数
*/
ADHON_PMC_LIB_API float  __stdcall  Modbus_ReadFloat(unsigned char ucControllerAddr, unsigned short usChannelAddr);

/***
    描述: 使用modbus协议进行双通道整数写入
    输入1: 控制器地址
    输入2:控制器中通道地址，参考modbus通道定义文档
    输入3:需要写入的整数
*/
ADHON_PMC_LIB_API int  __stdcall  Modbus_WriteLong(unsigned char ucControllerAddr, unsigned short usChannelAddr, unsigned  long ulWriteData);

/***
    描述: 使用modbus协议进行双通道整数读取
    输入1: 控制器地址
    输入2:控制器中通道地址，参考modbus通道定义文档
    返回值:读取的双通道整数
*/
ADHON_PMC_LIB_API unsigned long  __stdcall  Modbus_ReadLong(unsigned char ucControllerAddr, unsigned short usChannelAddr);

/***
   描述: 使用modbus协议进行单通道整数
  输入1: 控制器地址
  输入2:控制器中通道地址，参考modbus通道定义文档
  输入3:需要写入的浮点数
*/
ADHON_PMC_LIB_API int  __stdcall  Modbus_WriteShort(unsigned char ucControllerAddr, unsigned short usChannelAddr, unsigned short usWriteData);

/***
  描述:使用modbus协议进行浮点数读取
 输入1:控制器地址
 输入2:控制器中通道地址，参考modbus通道定义文档
返回值:读取的浮点数
*/
ADHON_PMC_LIB_API unsigned short  __stdcall  Modbus_ReadShort(unsigned char ucControllerAddr, unsigned short usChannelAddr);

/***
   描述: 将数据发送给控制器
  输入1: 控制器地址
  输入2: 需要发送数据给控制器
  输入3: 发送数据给控制器的长度
*/
ADHON_PMC_LIB_API int  __stdcall  PMC_CommandRawData(unsigned char ucCommandCode,  unsigned long * pulUserData1, unsigned long * pulUserData2, unsigned long * pulUserData3);

#ifdef  __cplusplus
}
#endif

#endif
