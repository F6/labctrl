#ifndef _USB1020_DEVICE_
#define _USB1020_DEVICE_
/**************************************************************************
// 硬件设置参数
**************************************************************************/
#include "windows.h"

// 公用参数 
#ifndef _USB1020_PARA_DataList
typedef struct _USB1020_PARA_DataList
{
	LONG Multiple;				// 倍率 (1~500)
	LONG StartSpeed;			// 初始速度(1~8000)
	LONG DriveSpeed;			// 驱动速度(1~8000)
	LONG Acceleration;			// 加速度(125~1000000)
	LONG Deceleration;			// 减速度(125~1000000)
	LONG AccIncRate;			// 加速度变化率(954~62500000)
	LONG DecIncRate;			// 减速度变化率(954~62500000)
} USB1020_PARA_DataList, *PUSB1020_PARA_DataList;
#endif

// 直线和S曲线参数
#ifndef _USB1020_PARA_LCData
typedef struct _USB1020_PARA_LCData
{
	LONG AxisNum;				// 轴号 (X轴 | Y轴 | X、Y轴)
	LONG LV_DV;					// 驱动方式  (连续 | 定长 )
	LONG DecMode;				// 减速方式  (自动减速 | 手动减速)	
	LONG PulseMode;				// 脉冲方式 (CW/CCW方式 | CP/DIR方式)
	LONG PLSLogLever;			// 设定驱动脉冲的方向（默认正方向）
	LONG DIRLogLever;			// 设定方向信号输出的逻辑电平（0：低电平为正向，1：高电平为正向）	
	LONG Line_Curve;			// 运动方式	(直线 | 曲线)
	LONG Direction;				// 运动方向 (正方向 | 反方向)
	LONG nPulseNum;		    	// 定量输出脉冲数(0~268435455)
} USB1020_PARA_LCData, *PUSB1020_PARA_LCData;
#endif

// 插补轴
#ifndef _USB1020_PARA_InterpolationAxis
typedef struct _USB1020_PARA_InterpolationAxis
{	
	LONG Axis1;					// 主轴
	LONG Axis2;					// 第二轴
	LONG Axis3;					// 第三轴
} USB1020_PARA_InterpolationAxis, *PUSB1020_PARA_InterpolationAxis;
#endif

// 直线插补和固定线速度直线插补参数
#ifndef _USB1020_PARA_LineData
typedef struct _USB1020_PARA_LineData	
{	
	LONG Line_Curve;			// 运动方式	(直线 | 曲线)
	LONG ConstantSpeed;			// 固定线速度 (不固定线速度 | 固定线速度)
	LONG n1AxisPulseNum;		// 主轴终点脉冲数 (-8388608~8388607)
	LONG n2AxisPulseNum;		// 第二轴轴终点脉冲数 (-8388608~8388607)
	LONG n3AxisPulseNum;		// 第三轴轴终点脉冲数 (-8388608~8388607)		
} USB1020_PARA_LineData, *PUSB1020_PARA_LineData;
#endif

// 正反方向圆弧插补参数
#ifndef _USB1020_PARA_CircleData
typedef struct _USB1020_PARA_CircleData	
{
	LONG ConstantSpeed;			// 固定线速度 (不固定线速度 | 固定线速度)
	LONG Direction;				// 运动方向 (正方向 | 反方向)
	LONG Center1;				// 主轴圆心坐标(脉冲数-8388608~8388607)
    LONG Center2;				// 第二轴轴圆心坐标(脉冲数-8388608~8388607)
	LONG Pulse1;				// 主轴终点坐标(脉冲数-8388608~8388607)	
	LONG Pulse2;				// 第二轴轴终点坐标(脉冲数-8388608~8388607)
} USB1020_PARA_CircleData, *PUSB1020_PARA_CircleData;
#endif

/***************************************************************/
// 轴号
#define		USB1020_XAXIS			0X0				// X轴
#define		USB1020_YAXIS			0x1				// Y轴
#define		USB1020_ZAXIS			0x2				// Z轴
#define		USB1020_UAXIS			0x3				// U轴
#define		USB1020_ALLAXIS			0xF				// 所有轴

/***************************************************************/
// 驱动方式
#define		USB1020_DV				0x0				// 定长驱动
#define		USB1020_LV				0x1				// 连续驱动

/***************************************************************/
// 减速方式
#define		USB1020_AUTO			0x0				// 自动减速
#define		USB1020_HAND			0x1				// 手动减速

/***************************************************************/
// 脉冲输出方式
#define 	USB1020_CWCCW			0X0				// CW/CCW方式 
#define 	USB1020_CPDIR 			0X1				// CP/DIR方式

/***************************************************************/
// 脉冲输入方式
#define 	USB1020_A_B			    0X0				// A/B相方式
#define 	USB1020_U_D 			0X1				// 上/下脉冲输入方式

/***************************************************************/
// 脉冲输入时的脉冲倍频数
#define 	USB1020_DIVRATIO_1		0X0				// 1倍频
#define 	USB1020_DIVRATIO_2 		0X1				// 2倍频
#define 	USB1020_DIVRATIO_4 		0X2				// 4倍频

/***************************************************************/
// 运动方式
#define		USB1020_LINE			0X0				// 直线运动
#define		USB1020_CURVE			0X1				// S曲线运动

/***************************************************************/
// 运动方向
#define		USB1020_MDIRECTION		0x0				// 反方向
#define		USB1020_PDIRECTION		0x1				// 正方向

/***************************************************************/
//固定线速度
#define		USB1020_NOCONSTAND		0X0				// 不固定线速度
#define		USB1020_CONSTAND		0X1				// 固定线速度

/***************************************************************/
// 软件限位的逻辑实位计数器选择和设置外部越限信号的停止方式和设置外部停止信号的停止号选择
/***************************************************************/
// 计数器类别
#define		USB1020_LOGIC			0x0				// 逻辑位计数器
#define		USB1020_FACT			0x1				// 实位计数器

/***************************************************************/
// 外部停止信号
#define 	USB1020_IN0				0X0				// 停止信号0
#define 	USB1020_IN1				0X1				// 停止信号1
#define 	USB1020_IN2				0X2				// 停止信号2
#define 	USB1020_IN3				0X3				// 停止信号3

/***************************************************************/
// 停止方式
#define		USB1020_SUDDENSTOP		0x0				// 立即停止
#define		USB1020_DECSTOP			0X1				// 减速停止

/********************************************************************/
// 输出切换
#define		USB1020_GENERALOUT		0x0				// 通用输出
#define		USB1020_STATUSOUT		0X1				// 状态输出

/********************************************************************/
#define		USB1020_ERROR			0XFF			// 错误

/****************************************************************/
// 设置中断位使能
#ifndef _USB1020_PARA_Interrupt
typedef struct _USB1020_PARA_Interrupt      
{
	UINT PULSE;			// 1：中断使能，中断信号由各输出的脉冲上升沿触发 0：禁止中断
	UINT PBCM;			// 1：中断使能，当逻辑/实际位置计数器的值大于等于COMP-寄存器的值时发中断信号 0：禁止中断
	UINT PSCM;			// 1：中断使能，当逻辑/实际位置计数器的值小于COMP-寄存器的值时发中断信号 0：禁止中断
	UINT PSCP;			// 1：中断使能，当逻辑/实际位置计数器的值小于COMP+寄存器的值时发中断信号 0：禁止中断
	UINT PBCP;			// 1：中断使能，当逻辑/实际位置计数器的值大于等于COMP+寄存器的值发中断信号 0：禁止中断
	UINT CDEC;			// 1：中断使能，在加/减速驱动中，当开始减速时发中断信号 0：禁止中断
	UINT CSTA;			// 1：中断使能，在加/减速驱动中，当开始定速时发中断信号 0：禁止中断
	UINT DEND;			// 1：中断使能，在驱动结束时发中断信号 0：禁止中断
	UINT CIINT;			// 1：中断使能，当允许写入下一个节点命令时产生中断 0：禁止中断
	UINT BPINT;			// 1：中断使能，当位插补堆栈计数器的值由2变为1时产生中断 0：禁止中断

} USB1020_PARA_Interrupt,*PUSB1020_PARA_Interrupt;
#endif

// 设置同步参数(主轴)
#ifndef _USB1020_PARA_SynchronActionOwnAxis
typedef struct _USB1020_PARA_SynchronActionOwnAxis    
{
	UINT PBCP;			// 1：当逻辑/实位计数器的值大于等于COMP+寄存器时，启动同步动作 0：无效
	UINT PSCP;			// 1：当逻辑/实位计数器的值小于COMP+寄存器时，启动同步动作 0：无效
	UINT PSCM;			// 1：当逻辑/实位计数器的值小于COMP-寄存器时，启动同步动作 0：无效
	UINT PBCM;			// 1：当逻辑/实位计数器的值大于等于COMP-寄存器时，启动同步动作 0：无效
	UINT DSTA;			// 1：当驱动开始时，启动同步动作 0：无效
	UINT DEND;			// 1：当驱动结束时，启动同步动作 0：无效
	UINT IN3LH;			// 1：当IN3出现上升沿时，启动同步动作 0：无效
	UINT IN3HL;			// 1：当IN3出现下降沿时，启动同步动作 0：无效
	UINT LPRD;			// 1：当读逻辑位置计数器时，启动同步动作 0：无效
	UINT CMD;			// 1：当写入同步操作命令时，启动同步轴的同步动作 0：无效
	UINT AXIS1;			// 1：指定与自己轴同步的轴  0：没有指定
	UINT AXIS2;			// 1：指定与自己轴同步的轴  0：没有指定
	UINT AXIS3;			// 1：指定与自己轴同步的轴  0：没有指定
						// 当前轴	AXIS3		AXIS2		AXIS1  
						// X轴		 U轴		 Z轴		 Y轴
						// Y轴		 U轴		 Z轴		 X轴
						// Z轴		 U轴		 Y轴		 X轴
						// U轴		 Z轴		 Y轴		 X轴
} USB1020_PARA_SynchronActionOwnAxis,*PUSB1020_PARA_SynchronActionOwnAxis;
#endif

// 设置同步参数(其它轴)
#ifndef _USB1020_PARA_SynchronActionOtherAxis
typedef struct _USB1020_PARA_SynchronActionOtherAxis    
{
	UINT FDRVP;			// 1：启动正方向定长驱动 0：无效
	UINT FDRVM;			// 1：启动反方向定长驱动 0：无效
	UINT CDRVP;			// 1：启动正方向连续驱动 0：无效
	UINT CDRVM;			// 1：启动反方向连续驱动 0：无效
	UINT SSTOP;			// 1：减速停止 0：无效
	UINT ISTOP;			// 1：立即停止 0：无效
	UINT LPSAV;			// 1：把当前逻辑寄存器LP值保存到同步缓冲寄存器BR 0：无效
	UINT EPSAV;			// 1：把当前实位寄存器EP值保存到同步缓冲寄存器BR 0：无效
	UINT LPSET;			// 1：把WR6和WR7的值设定到逻辑寄存器LP中 0：无效
	UINT EPSET;			// 1：把WR6和WR7的值设定到逻辑寄存器EP中 0：无效 
	UINT OPSET;			// 1：把WR6和WR7的值设定到逻辑寄存器LP中 0：无效
	UINT VLSET;			// 1：把WR6的值设定为驱动速度V 0：无效
	UINT OUTN;			// 1：用nDCC引脚输出同步脉冲  0：nDCC输出同步脉冲无效？？？
	UINT INTN;			// 1：产生中断  0：不产生中断
} USB1020_PARA_SynchronActionOtherAxis,*PUSB1020_PARA_SynchronActionOtherAxis;
#endif

// 设置其他参数
#ifndef _USB1020_PARA_ExpMode
typedef struct _USB1020_PARA_ExpMode
{
	UINT EPCLR;			// 1：当IN2触发有效时清除实位计数器 0：无效
	UINT FE0;			// 1：外部输入信号EMGN、nLMTP、nLMTM、nIN0、nIN1滤波器有效 0：无效
	UINT FE1;			// 1：外部输入信号nIN2滤波器有效 0：无效
	UINT FE2;			// 1：外部输入信号nALARM、nINPOS滤波器有效 0：无效
	UINT FE3;			// 1：外部输入信号nEXPP、nEXPM、EXPLS滤波器有效 0：无效
	UINT FE4;			// 1：外部输入信号nIN3滤波器有效 0：无效
	UINT FL0;			// 滤波器的时间常数 
						//	FL2 FL1 FL0	 滤波器时间常数	 信号延迟
	UINT FL1;			//		0：			1.75μS			2μS
	UINT FL2;			//		1：			224μS			256μS
						//		2：			448μS			512μS
						//		3：			896μS			1.024mμS
						//		4：			1.792mS			2.048mS
						//		5：			3.584mS			4.096mS
						//		6：			7.168mS			8.012mS
						//		7：			14.336mS		16.384mS
} USB1020_PARA_ExpMode,*PUSB1020_PARA_ExpMode;
#endif


// 偏离计数器清除设置
#ifndef _USB1020_PARA_DCC
typedef struct _USB1020_PARA_DCC
{
	UINT DCCE;			// 1：使能偏离计数器清除输出 0：无效
	UINT DCCL;			// 1：偏离计数器清除输出的逻辑电平为低电平  0：偏离计数器清除输出的逻辑电平为高电平
	UINT DCCW0;			// 用来指定偏离计数器清除输出的脉冲宽度
	UINT DCCW1;			//  DCCW2 DCCW1 DCCW0 清除的脉冲宽度(μS)
	UINT DCCW2;			// 	  0		0	  0		  10         	  1	 0  0		1000
						// 	  0		0	  1		  20			  1	 0  1		2000
						// 	  0		1	  0		  100			  1	 1  0		10000
						// 	  0		1	  1		  200			  1	 1  1		20000
} USB1020_PARA_DCC,*PUSB1020_PARA_DCC;
#endif

// 自动原点搜寻设置
#ifndef _USB1020_PARA_AutoHomeSearch
typedef struct _USB1020_PARA_AutoHomeSearch
{
	UINT ST1E;			// 1：第一步使能 0：无效
	UINT ST1D;			// 第一步的搜寻运转方向 0：正方向  1：负方向
	UINT ST2E;			// 1：第二步使能 0：无效
	UINT ST2D;			// 第二步的搜寻运转方向 0：正方向  1：负方向
	UINT ST3E;			// 1：第三步使能 0：无效
	UINT ST3D;			// 第三步的搜寻运转方向 0：正方向  1：负方向
	UINT ST4E;			// 1：第四步使能 0：无效
	UINT ST4D;			// 第四步的搜寻运转方向 0：正方向  1：负方向
	UINT PCLR;			// 1：第四步结束时清除逻辑计数器和实位计数器 0：无效
	UINT SAND;			// 1：原点信号和Z相信号有效时停止第三步操作 0：无效 
	UINT LIMIT;			// 1：利用硬件限位信号(nLMTP或nLMPM)进行原点搜寻 0：无效
	UINT HMINT;			// 1：当自动原点搜索结束时产生中断 0：无效
} USB1020_PARA_AutoHomeSearch,*PUSB1020_PARA_AutoHomeSearch;
#endif

// IO输出
#ifndef _USB1020_PARA_DO
typedef struct _USB1020_PARA_DO      
{
	UINT OUT0;			// 输出0
	UINT OUT1;			// 输出1
	UINT OUT2;			// 输出2
	UINT OUT3;			// 输出3
	UINT OUT4;			// 输出4
	UINT OUT5;			// 输出5
	UINT OUT6;			// 输出6
	UINT OUT7;			// 输出7
} USB1020_PARA_DO,*PUSB1020_PARA_DO;
#endif

// 状态寄存器RR0
#ifndef _USB1020_PARA_RR0
typedef struct _USB1020_PARA_RR0      
{
	UINT XDRV;			// X轴的驱动状态  1：正在输出脉冲 0：停止驱动
	UINT YDRV;			// Y轴的驱动状态  1：正在输出脉冲 0：停止驱动
	UINT ZDRV;			// Z轴的驱动状态  1：正在输出脉冲 0：停止驱动
	UINT UDRV;			// U轴的驱动状态  1：正在输出脉冲 0：停止驱动
	UINT XERROR;		// X轴的出错状态  X轴的RR2寄存器的任何一位为1，此位就为1
	UINT YERROR;		// Y轴的出错状态  Y轴的RR2寄存器的任何一位为1，此位就为1
	UINT ZERROR;		// Z轴的出错状态  Z轴的RR2寄存器的任何一位为1，此位就为1
	UINT UERROR;		// U轴的出错状态  U轴的RR2寄存器的任何一位为1，此位就为1
	UINT IDRV;			// 插补驱动状态   1：正处于插补模式  0：未处于插补模式
	UINT CNEXT;			// 表示可以写入连续插补的下一个数据  1：可以写入 0：不可以写入
	                    // 当设置连续插补中断使能后，CNEXT为1表示产生了中断，在中断程序写入下一个插补命令后，该位清零并且中断信号回到高电平
	UINT ZONE0;			// ZONE2、ZONE1、ZONE0表示在圆弧插补驱动中所在的象限
	UINT ZONE1;			// 000 ：第0象限   001：第1象限  010：第2象限  011：第3象限
	UINT ZONE2;			// 100 ：第4象限   101：第5象限	 110：第6象限  111：第7象限
	UINT BPSC0;			// BPSC1、BPSC0表示在位插补驱动中堆栈计数器(SC)的数值
	UINT BPSC1;			// 00： 0   01：1   10： 2   11：3
						// 设置位插补中断使能后，当SC的值由2变为1时，产生中断，
	                    // 当向位插补堆栈写入新的数据或调用USB1020_ClearInterruptStatus，中断解除。
} USB1020_PARA_RR0,*PUSB1020_PARA_RR0;
#endif

// 状态寄存器RR1，每一个轴都有RR1寄存器，读哪个要指定轴号
#ifndef _USB1020_PARA_RR1
typedef struct _USB1020_PARA_RR1    
{
	UINT CMPP;			// 表示逻辑/实位计数器和COMP+寄存器的大小关系 1：逻辑/实位计数器≥COMP+ 0：逻辑/实位计数器＜COMP+
	UINT CMPM;			// 表示逻辑/实位计数器和COMP-寄存器的大小关系 1：逻辑/实位计数器＜COMP- 0：逻辑/实位计数器≥COMP-
	UINT ASND;			// 在加/减速驱动中加速时，为1
	UINT CNST;			// 在加/减速驱动中定速时，为1
	UINT DSND;			// 在加/减速驱动中减速时，为1
	UINT AASND;			// 在S曲线加/减速驱动中，加速度/减速度增加时，为1 
	UINT ACNST;			// 在S曲线加/减速驱动中，加速度/减速度不变时，为1 
	UINT ADSND;			// 在S曲线加/减速驱动中，加速度/减速度减少时，为1 
	UINT IN0;			// 外部停止信号IN0有效使驱动停止时，为1
	UINT IN1;			// 外部停止信号IN1有效使驱动停止时，为1
	UINT IN2;			// 外部停止信号IN2有效使驱动停止时，为1
	UINT IN3;			// 外部停止信号IN3有效使驱动停止时，为1
	UINT LMTP;			// 外部正方向限制信号(nLMTP)有效使驱动停止时，为1
	UINT LMTM;			// 外部反方向限制信号(nLMTM)有效使驱动停止时，为1
	UINT ALARM;			// 外部伺服马达报警信号(nALARM)有效使驱动停止时，为1
	UINT EMG;			// 外部紧急停止信号(EMGN)使驱动停止时，为1
} USB1020_PARA_RR1,*PUSB1020_PARA_RR1;
#endif

// 状态寄存器RR2，每一个轴都有RR2寄存器，读哪个要指定轴号
#ifndef _USB1020_PARA_RR2
typedef struct _USB1020_PARA_RR2     
{
	UINT SLMTP;			// 设置正方向软件限位后，在正方向驱动中，逻辑/实位计数器大于COMP+寄存器值时，为1
	UINT SLMTM;			// 设置反方向软件限位后，在反方向驱动中，逻辑/实位计数器小于COMP-寄存器值时，为1
	UINT HLMTP;			// 外部正方向限制信号(nLMTP)处于有效电平时，为1
	UINT HLMTM;			// 外部反方向限制信号(nLMTM)处于有效电平时，为1
	UINT ALARM;			// 外部伺服马达报警信号(nALARM)设置为有效并处于有效状态时，为1
	UINT EMG;			// 外部紧急停止信号处于低电平时，为1
	UINT HOME;			// 当Z相编码信号在自动搜寻原点出错时为1
	UINT HMST0;			// HMST0-4(HMST4-0)表示自动原点搜寻中执行的步数
	UINT HMST1;			//	 0：等待自动原点搜寻命令
	UINT HMST2;			//	 3：等待IN0信号在指定方向上有效	
	UINT HMST3;			//	 8、12、15：等待IN1信号在指定方向上有效
	UINT HMST4;			//	 20：IN2信号在指定方向上有效
						//	 25：第四步
} USB1020_PARA_RR2,*PUSB1020_PARA_RR2;
#endif

// 状态寄存器RR3
#ifndef _USB1020_PARA_RR3
typedef struct _USB1020_PARA_RR3      
{
	UINT XIN0;			// 外部停止信号XIN0的电平状态 1：高电平 0：低电平
	UINT XIN1;			// 外部停止信号XIN1的电平状态 1：高电平 0：低电平
	UINT XIN2;			// 外部停止信号XIN2的电平状态 1：高电平 0：低电平
	UINT XIN3;			// 外部停止信号XIN3的电平状态 1：高电平 0：低电平
	UINT XEXPP;			// 外部正方向点动输入信号XEXPP的电平状态 1：高电平 0：低电平
	UINT XEXPM;			// 外部反方向点动输入信号XEXPM的电平状态 1：高电平 0：低电平
	UINT XINPOS;		// 外部伺服电机到位信号XINPOS的电平状态  1：高电平 0：低电平
	UINT XALARM;		// 外部伺服马达报警信号XALARM的电平状态  1：高电平 0：低电平
	UINT YIN0;			// 外部输入信号YIN0的电平状态  1：高电平 0：低电平
	UINT YIN1;			// 外部输入信号YIN1的电平状态  1：高电平 0：低电平
	UINT YIN2;			// 外部输入信号YIN2的电平状态  1：高电平 0：低电平
	UINT YIN3;			// 外部输入信号YIN3的电平状态  1：高电平 0：低电平
	UINT YEXPP;			// 外部正方向点动输入信号YEXPP的电平状态 1：高电平 0：低电平
	UINT YEXPM;			// 外部反方向点动输入信号YEXPM的电平状态 1：高电平 0：低电平
	UINT YINPOS;		// 外部伺服电机到位信号YINPOS的电平状态  1：高电平 0：低电平
	UINT YALARM;		// 外部伺服马达报警信号YALARM的电平状态  1：高电平 0：低电平
} USB1020_PARA_RR3,*PUSB1020_PARA_RR3;
#endif

// 状态寄存器RR4
#ifndef _USB1020_PARA_RR4
typedef struct _USB1020_PARA_RR4     
{
	UINT ZIN0;			// 外部停止信号YIN0的电平状态 1：高电平 0：低电平
	UINT ZIN1;			// 外部停止信号YIN1的电平状态 1：高电平 0：低电平
	UINT ZIN2;			// 外部停止信号YIN2的电平状态 1：高电平 0：低电平
	UINT ZIN3;			// 外部停止信号YIN3的电平状态 1：高电平 0：低电平
	UINT ZEXPP;			// 外部正方向点动输入信号ZEXPP的电平状态 1：高电平 0：低电平
	UINT ZEXPM;			// 外部反方向点动输入信号ZEXPM的电平状态 1：高电平 0：低电平
	UINT ZINPOS;		// 外部伺服电机到位信号ZINPOS的电平状态  1：高电平 0：低电平
	UINT ZALARM;		// 外部伺服马达报警信号ZALARM的电平状态  1：高电平 0：低电平
	UINT UIN0;			// 外部停止信号UIN0的电平状态 1：高电平 0：低电平
	UINT UIN1;			// 外部停止信号UIN1的电平状态 1：高电平 0：低电平
	UINT UIN2;			// 外部停止信号UIN2的电平状态 1：高电平 0：低电平
	UINT UIN3;			// 外部停止信号UIN3的电平状态 1：高电平 0：低电平
	UINT UEXPP;			// 外部正方向点动输入信号UEXPP的电平状态 1：高电平 0：低电平
	UINT UEXPM;			// 外部反方向点动输入信号UEXPM的电平状态 1：高电平 0：低电平
	UINT UINPOS;		// 外部伺服电机到位信号UINPOS的电平状态  1：高电平 0：低电平
	UINT UALARM;		// 外部伺服马达报警信号UALARM的电平状态  1：高电平 0：低电平
} USB1020_PARA_RR4,*PUSB1020_PARA_RR4;
#endif

// 状态寄存器RR5  当有中断产生时，相应的中断标志为1，中断输出信号为低电平
// 当主CPU读了RR5寄存器的中断标志后，RR5的标志就为0，中断信号恢复到高电平
#ifndef _USB1020_PARA_RR5
typedef struct _USB1020_PARA_RR5     
{
	UINT PULSE;			// 产生一个增量脉冲时为1
	UINT PBCM;			// 逻辑/实际位置计数器的值大于等于COMP-寄存器的值时为1
	UINT PSCM;			// 逻辑/实际位置计数器的值小于COMP-寄存器的值时为1
	UINT PSCP;			// 逻辑/实际位置计数器的值小于COMP+寄存器的值时为1
	UINT PBCP;			// 逻辑/实际位置计数器的值大于等于COMP+寄存器的值为1
	UINT CDEC;			// 在加/减速时，脉冲开始减速时为1
	UINT CSTA;			// 在加/减速时，开始定速时为1
	UINT DEND;			// 驱动结束时为1
	UINT HMEND;			// 自动原点搜索结束时为1
	UINT SYNC;			// 同步产生的中断
} USB1020_PARA_RR5,*PUSB1020_PARA_RR5;
#endif

#ifndef DEFINING
#define DEVAPI __declspec(dllimport)
#else
#define DEVAPI __declspec(dllexport)
#endif

#ifdef __cplusplus
extern "C" {
#endif

//######################## 设备对象管理函数 #################################
// 适用于本设备的最基本操作	
HANDLE DEVAPI FAR PASCAL USB1020_CreateDevice(			// 创建句柄
							int DeviceID);				// 设备ID号

HANDLE DEVAPI FAR PASCAL USB1020_CreateDeviceEx(		// 用物理ID创建句柄
							int DevicePhysID);			// 设备物理ID号

int DEVAPI FAR PASCAL USB1020_GetDeviceCount(			// 获得设备总数
							HANDLE hDevice);			// 设备句柄

int DEVAPI FAR PASCAL USB1020_GetDeviceCurrentID(		// 取得当前设备的物理ID号和逻辑ID号
							HANDLE hDevice,				// 设备句柄
							PLONG lpDeviceLgcID,		// 逻辑ID号
							PLONG lpDevicePhysID);		// 物理ID号

BOOL DEVAPI FAR PASCAL USB1020_ReleaseDevice(			// 释放设备
							HANDLE hDevice);			// 设备句柄

BOOL DEVAPI FAR PASCAL USB1020_Reset(				 // 复位整个USB设备
							HANDLE hDevice);		 // 设备句柄
//*******************************************************************
// 设置电机的逻辑计数器、实际位置计数器、加速计数器偏移

BOOL DEVAPI FAR PASCAL USB1020_PulseOutMode(         // 设置脉冲输出模式
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)  
							LONG Mode,				 // 模式
							LONG PLSLogLever,		 // 设定驱动脉冲的方向（默认正方向）
							LONG DIRLogLever);		 // 设定方向信号输出的逻辑电平（0：低电平为正向，1：高电平为正向）

BOOL DEVAPI FAR PASCAL USB1020_PulseInputMode(       // 设置脉冲输入模式
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)  
							LONG Mode);				 // 模式

BOOL DEVAPI FAR PASCAL USB1020_SetR(				 // 设置倍率(1-500)	
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)  
							LONG Data);				 // 倍率值(1-500)

BOOL DEVAPI FAR PASCAL USB1020_SetA(				 // 设置加速度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)     
							LONG Data);				 // 加速度(125-1000000)

BOOL DEVAPI FAR PASCAL USB1020_SetDec(				 // 设置减速度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 减速度值(125-1000000)

BOOL DEVAPI FAR PASCAL USB1020_SetAccIncRate(		 // 加速度变化率  
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)   
							LONG Data);				 // 数据(954-62500000)

BOOL DEVAPI FAR PASCAL USB1020_SetDecIncRate(		 // 减速度变化率  
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 数据

BOOL DEVAPI FAR PASCAL USB1020_SetSV(				 // 设置初始速度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)   
							LONG Data);				 // 速度值

BOOL DEVAPI FAR PASCAL USB1020_SetV(				 // 设置驱动速度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)     
							LONG Data);				 // 驱动速度值

BOOL DEVAPI FAR PASCAL USB1020_SetHV(				 // 设置原点搜寻速度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)	
							LONG Data);				 // 原点搜寻速度值(1-8000)

BOOL DEVAPI FAR PASCAL USB1020_SetP(				 // 设置定长脉冲数
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);			     // 定长脉冲数(0-268435455)

BOOL DEVAPI FAR PASCAL USB1020_SetIP(				 // 设置插补终点脉冲数(-8388608-+8388607)
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 插补终点脉冲数(-8388608-+8388607)

BOOL DEVAPI FAR PASCAL USB1020_SetC(                 // 设置圆心坐标(脉冲数)  
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 圆心坐标脉冲数范围(-2147483648-+2147483647)

BOOL DEVAPI FAR PASCAL USB1020_SetLP(				 // 设置逻辑位置计数器
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 逻辑位置计数器值(-2147483648-+2147483647)

BOOL DEVAPI FAR PASCAL USB1020_SetEP(				 // 设置实位计数器 
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 实位计数器值(-2147483648-+2147483647)

BOOL DEVAPI FAR PASCAL USB1020_SetAccofst(			 // 设置加速计数器偏移
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 偏移范围(0-65535)

BOOL DEVAPI FAR PASCAL USB1020_SelectLPEP(			 // 选择逻辑计数器或实位计数器
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG LogicFact);		 // 选择逻辑位置计数器或实位计数器 USB1020_LOGIC：逻辑位置计数器 USB1020_FACT：实位计数器	

BOOL DEVAPI FAR PASCAL USB1020_SetCOMPP(			 // 设置COMP+寄存器
							HANDLE hDevice,			 // 设备号
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)  
							USHORT LogicFact,		 // 选择逻辑位置计数器或实位计数器 USB1020_LOGIC：逻辑位置计数器 USB1020_FACT：实位计数器	
							LONG Data);

BOOL DEVAPI FAR PASCAL USB1020_SetCOMPM(			 // 设置COMP-寄存器
							HANDLE hDevice,			 // 设备号
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							USHORT LogicFact,		 // 选择逻辑位置计数器或实位计数器 USB1020_LOGIC：逻辑位置计数器 USB1020_FACT：实位计数器	
							LONG Data);
//*******************************************************************
// 设置同步位
BOOL DEVAPI FAR PASCAL USB1020_SetSynchronAction(	 // 设置同步位
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							PUSB1020_PARA_SynchronActionOwnAxis pPara1,// 自己轴的参数设置
						    PUSB1020_PARA_SynchronActionOtherAxis pPara2);// 其它轴的参数设置

BOOL DEVAPI FAR PASCAL USB1020_SynchronActionDisable(// 设置同步位无效
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)
							PUSB1020_PARA_SynchronActionOwnAxis pPara1,// 自己轴的参数设置
							PUSB1020_PARA_SynchronActionOtherAxis pPara2);// 其它轴的参数设置

BOOL DEVAPI FAR PASCAL USB1020_WriteSynchronActionCom(// 写同步操作命令
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

//*******************************************************************
//  设置DCC和其他模式
BOOL DEVAPI FAR PASCAL USB1020_SetDCC(				 // 设置输出信号nDCC的输出电平和电平宽度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							PUSB1020_PARA_DCC pPara);// DCC信号参数结构体指针

BOOL DEVAPI FAR PASCAL USB1020_StartDCC(			   // 启动偏离计数器清除输出命令
							HANDLE hDevice,			   // 设备句柄
							LONG AxisNum);			   // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

BOOL DEVAPI FAR PASCAL USB1020_ExtMode(				   // 设置其他模式
							HANDLE hDevice,			   // 设备句柄
							LONG AxisNum,			   // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							PUSB1020_PARA_ExpMode pPara);// 其他参数结构体指针
//*******************************************************************
// 设置自动原点搜寻
BOOL DEVAPI FAR PASCAL USB1020_SetInEnable(			// 设置自动原点搜寻第一、第二、第三步外部触发信号IN0-2的有效电平
							HANDLE hDevice,			// 设备号
							LONG AxisNum,			// 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)	
							LONG InNum,				// 停止号
							LONG LogLever);			// 有效电平

BOOL DEVAPI FAR PASCAL USB1020_SetAutoHomeSearch(   // 设置自动原点搜寻参数
							HANDLE hDevice,			// 设备句柄
							LONG AxisNum,			// 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)
							PUSB1020_PARA_AutoHomeSearch pPara);// 自动搜寻原点参数结构体指针

BOOL DEVAPI FAR PASCAL USB1020_StartAutoHomeSearch( // 启动自动原点搜寻
							HANDLE hDevice,			// 设备句柄		
							LONG AxisNum);			// 轴号(1:X轴; 2:Y轴)	

//*******************************************************************
// 设置编码器输入信号类型
BOOL DEVAPI FAR PASCAL USB1020_SetEncoderSignalType(// 设置编码器输入信号类型
							HANDLE hDevice,			// 设备句柄
							LONG AxisNum,			// 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)	
							LONG Type,				// 输入信号类型 0：2相脉冲输入 1：上/下脉冲输入
							LONG DivRatio);			// 脉冲的倍频数
//*******************************************************************
// 直线S曲线初始化、启动函数
BOOL DEVAPI FAR PASCAL USB1020_InitLVDV(				// 初始化连续,定长脉冲驱动
							HANDLE hDevice,				// 设备句柄
							PUSB1020_PARA_DataList pDL, // 公共参数结构体指针
							PUSB1020_PARA_LCData pLC);	// 直线S曲线参数结构体指针

BOOL DEVAPI FAR PASCAL USB1020_StartLVDV(				// 启动连续,定长脉冲驱动
							HANDLE hDevice,				// 设备句柄
							LONG AxisNum);				// 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

BOOL DEVAPI FAR PASCAL	USB1020_Start4D(HANDLE hDevice);// 4轴同时启动						           
//*******************************************************************
// 任意2轴直线插补初始化、启动函数
BOOL DEVAPI FAR PASCAL USB1020_InitLineInterpolation_2D(// 初始化任意2轴直线插补运动 
							HANDLE hDevice,				// 设备句柄
							PUSB1020_PARA_DataList pDL, // 公共参数结构体指针
							PUSB1020_PARA_InterpolationAxis pIA,// 插补轴结构体指针
							PUSB1020_PARA_LineData pLD);// 直线插补结构体指针

BOOL DEVAPI FAR PASCAL USB1020_StartLineInterpolation_2D(// 启动任意2轴直线插补运动 
							HANDLE hDevice);			 // 设备句柄
							
//*******************************************************************
// 任意3轴直线插补初始化、启动函数
BOOL DEVAPI FAR PASCAL USB1020_InitLineInterpolation_3D(// 初始化任意3轴直线插补运动	
							HANDLE hDevice,				// 设备句柄
							PUSB1020_PARA_DataList pDL, // 公共参数结构体指针
							PUSB1020_PARA_InterpolationAxis pIA,// 插补轴结构体指针
							PUSB1020_PARA_LineData pLD);// 直线插补结构体指针

BOOL DEVAPI FAR PASCAL USB1020_StartLineInterpolation_3D(// 启动任意3轴直线插补运动 				
							HANDLE hDevice);			 // 设备句柄
	
//*******************************************************************
// 任意2轴正反方向圆弧插补初始化、启动函数
BOOL DEVAPI FAR PASCAL USB1020_InitCWInterpolation_2D(	// 初始化任意2轴正反方向圆弧插补运动 
							HANDLE hDevice,				// 设备句柄
							PUSB1020_PARA_DataList pDL, // 公共参数结构体指针
							PUSB1020_PARA_InterpolationAxis pIA,// 插补轴结构体指针
							PUSB1020_PARA_CircleData pCD);// 圆弧插补结构体指针
                         
BOOL DEVAPI FAR PASCAL USB1020_StartCWInterpolation_2D( // 启动任意2轴正、反方向圆弧插补运动 
							HANDLE hDevice,				// 设备句柄
	                        LONG Direction);			// 方向 正转：USB1020_PDIRECTION 反转：USB1020_MDIRECTION  

BOOL DEVAPI FAR PASCAL USB1020_SetCWRadius(				// 设置圆弧半径
							HANDLE hDevice,				// 设备句柄
							LONG mainCerter,			// 主轴圆心坐标
							LONG secondCerter);         // 第二轴轴圆心坐标        
//*************************************************************************
// 位插补相关函数
BOOL DEVAPI FAR PASCAL USB1020_InitBitInterpolation_2D(	// 初始化任意2轴位插补参数
							HANDLE hDevice,				// 设备句柄
							PUSB1020_PARA_InterpolationAxis pIA,// 插补轴结构体指针
							PUSB1020_PARA_DataList pDL);// 公共参数结构体指针

BOOL DEVAPI FAR PASCAL USB1020_InitBitInterpolation_3D(// 初始化任意2轴位插补参数
							HANDLE hDevice,			   // 设备句柄
							PUSB1020_PARA_InterpolationAxis pIA,// 插补轴结构体指针
						    PUSB1020_PARA_DataList pDL);// 公共参数结构体指针

BOOL DEVAPI FAR PASCAL USB1020_AutoBitInterpolation_2D( // 启动任意2轴位插补子线程
							HANDLE hDevice,				// 设备句柄
							PUSHORT pBuffer,				// 位插补数据指针	
							UINT nCount);				// 数据组数

BOOL DEVAPI FAR PASCAL USB1020_AutoBitInterpolation_3D( // 启动任意3轴位插补子线程
							HANDLE hDevice,				// 设备句柄
							PSHORT pBuffer,				// 位插补数据指针	
							UINT nCount);				// 数据组数

BOOL DEVAPI FAR PASCAL USB1020_ReleaseBitInterpolation(	// 释放BP寄存器
							HANDLE hDevice);			// 设备句柄

BOOL DEVAPI FAR PASCAL USB1020_SetBP_2D(                // 设置任意2轴位插补数据
							HANDLE hDevice,				// 设备句柄 
							LONG BP1PData,				// 1轴正方向驱动数据
							LONG BP1MData,				// 1轴反方向驱动数据
							LONG BP2PData,				// 2轴正方向驱动数据
							LONG BP2MData);				// 2轴反方向驱动数据

BOOL DEVAPI FAR PASCAL USB1020_SetBP_3D(				// 设置任意3轴位插补数据	
							HANDLE hDevice,				// 设备句柄
							USHORT BP1PData,			// 1轴正方向驱动数据
							USHORT BP1MData,			// 1轴反方向驱动数据
							USHORT BP2PData,			// 2轴正方向驱动数据
							USHORT BP2MData,			// 2轴反方向驱动数据
							USHORT BP3PData,			// 3轴正方向驱动数据
							USHORT BP3MData);			// 3轴反方向驱动数据

LONG DEVAPI FAR PASCAL USB1020_BPRegisterStack(			// BP位数据堆栈返回值
							HANDLE hDevice);			// 设备句柄

BOOL DEVAPI FAR PASCAL USB1020_StartBitInterpolation_2D(// 启动任意2轴位插补
							HANDLE hDevice);			// 设备句柄

BOOL DEVAPI FAR PASCAL USB1020_StartBitInterpolation_3D(// 启动任意3轴位插补
							HANDLE hDevice);			// 设备句柄

BOOL DEVAPI FAR PASCAL  USB1020_BPWait(					// 等待位插补的下一个数据设定
							HANDLE hDevice,				// 设备句柄
							PBOOL pbRun);			

BOOL DEVAPI FAR PASCAL USB1020_ClearBPData(				// 清除BP寄存器数据
							HANDLE hDevice);			// 设备句柄
//*******************************************************************
// 连续插补相关函数
BOOL DEVAPI FAR PASCAL  USB1020_NextWait(				// 等待连续插补下一个节点命令设定
							HANDLE hDevice);			// 设备句柄

//*******************************************************************
// 单步插补函数
BOOL DEVAPI FAR PASCAL USB1020_SingleStepInterpolationCom(// 设置命令控制单步插补运动
							HANDLE hDevice);			// 设备句柄	

BOOL DEVAPI FAR PASCAL USB1020_StartSingleStepInterpolation(// 发单步命令
							HANDLE hDevice);

BOOL DEVAPI FAR PASCAL USB1020_SingleStepInterpolationExt(// 设置外部控制单步插补运动
							HANDLE hDevice);			// 设备句柄

BOOL DEVAPI FAR PASCAL USB1020_ClearSingleStepInterpolation(// 清除单步插补设置
							HANDLE hDevice);			// 设备句柄
//*******************************************************************
// 中断位设置、插补中断状态清除
BOOL DEVAPI FAR PASCAL USB1020_SetInterruptBit(			// 设置中断位
							HANDLE hDevice,				// 设备句柄
							LONG AxisNum,				// 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							PUSB1020_PARA_Interrupt pPara);// 中断位结构体指针

BOOL DEVAPI FAR PASCAL USB1020_ClearInterruptStatus(	// 清除插补中断状态 
							HANDLE hDevice);			// 设备句柄

//*******************************************************************
// 外部信号启动电机定长驱动、连续驱动

BOOL DEVAPI FAR PASCAL USB1020_SetOutEnableDV(		 // 设置外部使能定量驱动(下降沿有效)
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
		                    
BOOL DEVAPI FAR PASCAL USB1020_SetOutEnableLV(		 // 设置外部使能连续驱动(保持低电平有效)
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

//*******************************************************************
// 设置软件限位有效和无效
BOOL DEVAPI FAR PASCAL USB1020_SetPDirSoftwareLimit( // 设置正方向软件限位
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG LogicFact,			 // 逻辑/实位计数器选择 USB1020_LOGIC：逻辑位置计数器 USB1020_FACT：实位计数器	
							LONG Data);				 // 软件限位数据

BOOL DEVAPI FAR PASCAL USB1020_SetMDirSoftwareLimit( // 设置反方向软件限位
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG LogicFact,			 // 逻辑/实位计数器选择 USB1020_LOGIC：逻辑位置计数器 USB1020_FACT：实位计数器	
							LONG Data);				 

BOOL DEVAPI FAR PASCAL USB1020_ClearSoftwareLimit(	 // 清除软件限位
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)

//******************************************************************* 
// 设置外部输入信号的有效和无效		
BOOL DEVAPI FAR PASCAL USB1020_SetPDirLMTEnable(	 // 设置外部越限信号的有效及停止方式	
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG StopMode,           // USB1020_DECSTOP：减速停止，USB1020_SUDDENSTOP：立即停止
							LONG LogLever);			 // 有效电平（默认低电平有效）

BOOL DEVAPI FAR PASCAL USB1020_SetMDirLMTEnable(	 // 设置外部越限信号的有效及停止方式	
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG StopMode,           // USB1020_DECSTOP：减速停止，USB1020_SUDDENSTOP：立即停止
							LONG LogLever);			 // 有效电平（默认低电平有效）

BOOL DEVAPI FAR PASCAL USB1020_SetStopEnable(		 // 设置外部停止信号有效
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG StopNum,			 // 停止号
							LONG LogLever);			 // 有效电平（默认低电平有效）

BOOL DEVAPI FAR PASCAL USB1020_SetStopDisable(		 // 设置外部停止信号无效
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)
							LONG StopNum);			 // 停止号
											
BOOL DEVAPI FAR PASCAL USB1020_SetALARMEnable(       // 设置伺服报警信号有效 
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)  
							LONG LogLever);			 // 有效电平（默认低电平有效）

BOOL DEVAPI FAR PASCAL USB1020_SetALARMDisable(      // 设置伺服报警信号无效  
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)  

BOOL DEVAPI FAR PASCAL USB1020_SetINPOSEnable(		 // 设置伺服马达定位完毕输入信号有效 
							HANDLE hDevice,			 // 设备句柄	
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG LogLever);			 // 有效电平（默认低电平有效）

BOOL DEVAPI FAR PASCAL USB1020_SetINPOSDisable(		 // 设置伺服马达定位完毕输入信号无效
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

//*******************************************************************
// 减速函数设置

BOOL DEVAPI FAR PASCAL USB1020_DecValid(			 // 减速有效
							HANDLE hDevice);		 // 设备句柄

BOOL DEVAPI FAR PASCAL USB1020_DecInvalid(			 // 减速无效
							HANDLE hDevice);		 // 设备句柄

BOOL DEVAPI FAR PASCAL USB1020_DecStop(				 // 减速停止
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)  

BOOL DEVAPI FAR PASCAL USB1020_InstStop(			 // 立即停止
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

BOOL DEVAPI FAR PASCAL USB1020_AutoDec(				 // 自动减速
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

BOOL DEVAPI FAR PASCAL USB1020_HanDec(				 // 手动减速点设定
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Data);				 // 手动减速点数据，范围(0 - 4294967295)

//*************************************************************************
// 读电机状态：逻辑计数器、实际位置计数器、当前速度、加/减速度
LONG DEVAPI FAR PASCAL USB1020_ReadLP(				 // 读逻辑计数器
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

LONG DEVAPI FAR PASCAL USB1020_ReadEP(				 // 读实位计数器
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

LONG DEVAPI FAR PASCAL USB1020_ReadBR(				 // 读同步缓冲寄存器
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)

LONG DEVAPI FAR PASCAL USB1020_ReadCV(				 // 读当前速度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 

LONG DEVAPI FAR PASCAL USB1020_ReadCA(				 // 读当前加速度
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum);			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴)

//*******************************************************************
// 设置输出切换和通用输出
BOOL DEVAPI FAR PASCAL USB1020_OutSwitch(			 // 设置输出切换
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG StatusGeneralOut);	 // 状态输出和通用输出选择 USB1020_STATUS:状态输出 USB1020_GENERAL:通用输出

BOOL DEVAPI FAR PASCAL USB1020_SetDeviceDO(
							 HANDLE hDevice,	 	 // 设备号
							 LONG AxisNum,			 // 轴号
							 PUSB1020_PARA_DO pPara);
//*******************************************************************
// 读状态寄存器的位状态
LONG DEVAPI FAR PASCAL USB1020_ReadRR(				 // 读RR寄存器
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							LONG Num);				 // 寄存器号

BOOL DEVAPI FAR PASCAL USB1020_GetRR0Status(		 // 获得主状态寄存器RR0的位状态
							HANDLE hDevice,			 // 设备句柄
							PUSB1020_PARA_RR0 pPara);// RR0寄存器状态

BOOL DEVAPI FAR PASCAL USB1020_GetRR1Status(		 // 获得状态寄存器RR1的位状态
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							PUSB1020_PARA_RR1 pPara);// RR1寄存器状态			

BOOL DEVAPI FAR PASCAL USB1020_GetRR2Status(		 // 获得状态寄存器RR2的位状态
							HANDLE hDevice,			 // 设备句柄
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							PUSB1020_PARA_RR2 pPara);// RR2寄存器状态			

BOOL DEVAPI FAR PASCAL USB1020_GetRR3Status(		 // 获得状态寄存器RR3的位状态
							HANDLE hDevice,			 // 设备句柄
							PUSB1020_PARA_RR3 pPara);// RR3寄存器状态			

BOOL DEVAPI FAR PASCAL USB1020_GetRR4Status(		 // 获得状态寄存器RR4的位状态
							HANDLE hDevice,			 // 设备句柄
							PUSB1020_PARA_RR4 pPara);// RR4寄存器状态

BOOL DEVAPI FAR PASCAL USB1020_GetRR5Status(
							HANDLE hDevice,			 // 设备号
							LONG AxisNum,			 // 轴号(USB1020_XAXIS:X轴,USB1020_YAXIS:Y轴, USB1020_ZAXIS:Z轴,USB1020_UAXIS:U轴) 
							PUSB1020_PARA_RR5 pPara);// RR5寄存器状态
//*******************************************************************
#ifdef __cplusplus
}
#endif
// 自动包含驱动函数导入库
// 自动包含驱动函数导入库
#ifndef DEFINING
#ifndef _WIN64
#pragma comment(lib, "USB1020_32.lib")
#pragma message("======== Welcome to use our art company's products!")
#pragma message("======== Automatically linking with USB1020_32.dll...")
#pragma message("======== Successfully linked with USB1020_32.dll")
#else
#pragma comment(lib, "USB1020_64.lib")
#pragma message("======== Welcome to use our art company's products!")
#pragma message("======== Automatically linking with USB1020_64.dll...")
#pragma message("======== Successfully linked with USB1020_64.dll")
#endif

#endif

#endif; // _USB1020_DEVICE_