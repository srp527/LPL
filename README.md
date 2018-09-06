
# LOL lpl战队信息爬取
python 3.6
scrapy 1.3.3


#### 简单说下爬取的过程
#### 战队页面: http://lpl.qq.com/es/team.shtml

#### 一开始直接爬取发现爬不到数据, 查了一下发现 战队信息在'clublist.js'文件中
![python](https://github.com/srp527/LPL/blob/master/lol/images/lol0.png)

#### 战队详细信息在一个'LOL_MATCH2_TEAM_TEAM57_INFO.js'文件中, 57这个数字是战队编号
![python](https://github.com/srp527/LPL/blob/master/lol/images/lol1.png)


#### 选手信息在一个'LOL_MATCH2_TEAM_MEMBER14_INFO.js'的文件中, 14是选手的编号
![python](https://github.com/srp527/LPL/blob/master/lol/images/lol2.png)

#### 所以有这两个url 就可以爬取到需要的信息了
#### LOL战队详情api
team_url = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_TEAM{team_id}_INFO.js'
#### 战队成员详情api
member_url = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_MEMBER{member_id}_INFO.js'



#### 爬到的数据展示
![python](https://github.com/srp527/LPL/blob/master/lol/images/lol.png)