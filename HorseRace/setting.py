#跑道长度
setting_track_length = 20
#随机位置事件，最小能到的跑道距离
setting_random_min_length = 0
#随机位置事件，最大能到的跑道距离
setting_random_max_length = 15
#每回合基础移动力最小值
base_move_min = 1
#每回合基础移动力最大值
base_move_max = 3
#最大支持玩家数
max_player = 8
#最少玩家数
min_player = 2
#超时允许重置最少时间，秒
setting_over_time = 120

#马儿事件概率 = event_rate / 1000
event_rate = 450
#环境事件概率 = event_rate2 / 1000
event_rate2 = 450

#马儿称号最大字数
nickname_max_len = 2
#马儿名字最大字数
name_max_len = 16

#新版本增加配置
#最大等级
level_max = 20
#每级所需经验
exp_up_level = 100
#比赛经验获取-冠军
exp_win = 80
#比赛经验获取-参与奖
exp_articipation = 30

#零级驻足/+1/+2/+3事件触发权数
rate_0_base = 20
rate_1_base = 50
rate_2_base = 30
rate_3_base = 10

#满级驻足/+1/+2/+3权数
rate_0_min = 5
rate_1_min = 20
rate_2_max = 50
rate_3_max = 30

#属性波动修正（实际权数=零级权数+|（当前等级权数*基础波动系数1-零级权数*基础波动系数2）|*（1+修正系数）* 曲率修正系数
#曲率修正系数 = 1 ./ (1+exp(-level / level_max * 4)) - 0.5;
#基础波动系数 = 1+base_rate%
#基础波动系数 = 1-base_rate%
#修正系数随机范围：-max_rate ~ +max_rate
#基础波动比 单位%
base_rate = 20
#修正波动比 单位%
max_rate = 30

#属性rank区间
#以最低-100%，最高100%计
#S区间为 [80,100]
#A区间为 [50,80)
#B区间为 [20,50)
#C区间为 [-20,20)
#D区间为 [-50,-20)
#E区间为 [-80,-50)
#F区间为 [-100,-80)
