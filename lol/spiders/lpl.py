# -*- coding: utf-8 -*-
import json
import os
import requests

from scrapy import Spider,Request

from lol.items import PlayerItem,TeamItem,BaseInfoItem,FavoriteHerosItem,PlayerAwardsItem

class LplSpider(Spider):
    name = "lpl"
    allowed_domains = ["lpl.qq.com"]
    start_urls = ['http://lpl.qq.com/']

    team_url = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_TEAM{team_id}_INFO.js' #LOL战队详情api
    member_url = 'http://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_MEMBER{member_id}_INFO.js' #战队成员详情api

    # G_gameTeam: [
    #     {'TeamId': 57, 'TeamName': 'BLG'},
    #     {'TeamId': 1, 'TeamName': 'EDG'},
    #     {'TeamId': 7, 'TeamName': 'FPX'},
    #     {'TeamId': 2, 'TeamName': 'IG'},
    #     {'TeamId': 29, 'TeamName': 'JDG'},
    #     {'TeamId': 4, 'TeamName': 'LGD'},
    #     {'TeamId': 6, 'TeamName': 'OMG'},
    #     {'TeamId': 8, 'TeamName': 'RNG'},
    #     {'TeamId': 422, 'TeamName': 'RW'},
    #     {'TeamId': 41, 'TeamName': 'SNG'},
    #     {'TeamId': 9, 'TeamName': 'Snake'},
    #     {'TeamId': 42, 'TeamName': 'TOP'},
    #     {'TeamId': 11, 'TeamName': 'VG'},
    #     {'TeamId': 12, 'TeamName': 'WE'}
    # ],
    # LPL战队ID号
    Team_IDs = {
        'BLG': 57, 'EDG': 1, 'FPX': 7, 'IG': 2, 'JDG': 29, 'LGD': 4,
        'OMG': 6, 'RNG': 8, 'RW': 422, 'SNG': 41, 'Snake': 9, 'TOP': 42,
        'VG': 11, 'WE': 12
    }


    def start_requests(self):
        for team_name,team_id in self.Team_IDs.items():
            print('---->',team_id)
            yield Request(self.team_url.format(team_id=team_id),callback=self.parse_team)


    def parse_team(self,response):
        data = json.loads(response.text)
        player_item = PlayerItem()
        team_item = TeamItem()
        teams_list = []
        players_list = []

        if 'msg' in data.keys():
            team_info = data['msg']['baseInfo']
            team_item['TeamName'] = team_info.get('TeamName')
            team_item['TeamEnName'] = team_info.get('TeamEnName')
            team_item['TeamDesc'] = team_info.get('TeamDesc')
            team_item['TeamLogo'] = team_info.get('TeamLogo')
            team_item['TeamId'] = team_info.get('TeamId')
            teams_list.append(team_item)
            yield team_item

            for player_info in data['msg']['activePlayers']:
                player_item['MemberId'] = player_info.get('MemberId')
                player_item['NickName'] = player_info.get('NickName')
                player_item['RealName'] = player_info.get('RealName')
                player_item['Place'] = player_info.get('Place')
                player_item['GameName'] = player_info.get('GameName')
                player_item['GamePlace'] = player_info.get('GamePlace')
                player_item['UserIcon'] = player_info.get('UserIcon')
                players_list.append(player_item)
                yield player_item
                member_id = player_info.get('MemberId')
                yield Request(self.member_url.format(member_id=member_id),callback=self.parse_member)

                self.save_img(teams_list, players_list) #保存队员头像

    def parse_member(self,response):
        data = json.loads(response.text)
        base_item = BaseInfoItem()
        fav_item = FavoriteHerosItem()
        award_item = PlayerAwardsItem()

        if 'msg' in data.keys():
            base_info = data['msg']['baseInfo']
            base_item['EnName'] = base_info.get('EnName')
            base_item['GameDate'] = base_info.get('GameDate')
            base_item['GameHero'] = base_info.get('GameHero')
            base_item['GameName'] = base_info.get('GameName')
            base_item['GamePlace'] = base_info.get('GamePlace')
            base_item['MemberDesc'] = base_info.get('MemberDesc')
            base_item['MemberId'] = base_info.get('MemberId')
            base_item['NickName'] = base_info.get('NickName')
            base_item['RealName'] = base_info.get('RealName')
            base_item['TeamId'] = base_info.get('TeamId')
            base_item['TeamName'] = base_info.get('TeamName')
            base_item['UserIcon'] = base_info.get('UserIcon')
            yield base_item

            for fav_hero in data['msg']['favoriteHeros']:
                fav_item['HeroId'] = fav_hero.get('HeroId')
                fav_item['UseNum'] = fav_hero.get('UseNum')
                fav_item['WinNum'] = fav_hero.get('WinNum')
                fav_item['sUpdated'] = fav_hero.get('sUpdated')
                yield fav_item

            try:
                for award_info in data['msg']['playerAwards']:
                    award_item['AwardDesc'] = award_info.get('AwardDesc')
                    award_item['RankName'] = award_info.get('RankName')
                    award_item['sGameName'] = award_info.get('sGameName')
                    yield award_item
            except TypeError:
                return None


    def save_img(self,teams_list,players_list):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_dir = os.path.join(base_dir,'images/')
        for team in teams_list:
            img_name = str(team['TeamName'])+'.jpg'
            img = requests.get(team['TeamLogo'])
            with open(img_dir+img_name,'wb') as f:
                f.write(img.content)
        for player in players_list:
            img_name1 = str(player['GameName'])+'-'+str(player['RealName'])+'.jpg'
            img1 = requests.get(player['UserIcon'])
            with open(img_dir+img_name1,'wb') as f:
                f.write(img1.content)


# if __name__ == '__main__':
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     img_dir = os.path.join(base_dir, 'images/')
#     print(base_dir,img_dir)
#
#     img_name = 'lpl.jpg'
#     img = requests.get('http://img.crawler.qq.com/lolwebvideo/201712250188/34f20f2ea6ecf86d1a97cada1c3cf4ce/0')
#     with open(img_dir+img_name,'wb') as f:
#         f.write(img.content)
# {"status":"0","msg":{
#     "baseInfo":
#         {"TeamId":"57",
#          "TeamName":"BLG",
#          "TeamEnName":"BilibiliGaming",
#          "TeamDesc":""
#          "TeamLogo":"http:\/\/img.crawler.qq.com\/lolwebvideo\/201712250188\/34f20f2ea6ecf86d1a97cada1c3cf4ce\/0",
#          "CreateDate":"0000-00-00",
#          "sUrl":"",
#          "Place":"0",
#          "Leader":"",
#          "Weibo":"",
#          "Tags":"",
#          "TeamStatus":"1",
#          "RsetNameStatus":"1",
#          "RsetTeamId":"IM-EDE",
#          "TeamLogoDeep":"http:\/\/shp.qpic.cn\/lolwebvideo\/201501\/e20e1c233f1227037261c2d8761b6041\/0",
#          "TeamLogo450":"http:\/\/img.crawler.qq.com\/lolwebvideo\/201712250188\/918eb21b4581f0459e33e42d98003102\/0"},
#     "activePlayers":[
#         {"MemberId":"7",
#          "RealName":"\u77f3\u4f1f\u8c6a",
#          "NickName":"AmazingJ",
#          "UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180606135528\/3e19bfb098783405281c493b68996a6c\/0",
#          "sUrl":"",
#          "Place":"1",
#          "GameName":"BLGAmazingJ",
#          "GamePlace":"1,"
#          },
#         {"MemberId":"8",
#          "RealName":"\u8c22\u91d1\u5c71",
#          "NickName":"Jinjiao",
#          "UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180531124129\/f7e00aba2d2f4e4082270e9b53decf24\/0",
#          "sUrl":"",
#          "Place":"1",
#          "GameName":"BLGJinjiao",
#          "GamePlace":"3,"
#          },
#         {"MemberId":"265","RealName":"\u59dc\u53a6\u4e91","NickName":"Athena","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180531123858\/477ff7e532d2211a8da236f26cab2d83\/0","sUrl":"","Place":"2","GameName":"BLGAthena","GamePlace":"2,"},
#         {"MemberId":"291","RealName":"\u5c39\u97e9\u5409","NickName":"Road","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180531124512\/f88e04d72c712e279dc56091568cbe4e\/0","sUrl":"","Place":"2","GameName":"BLGRoad","GamePlace":"4,"},
#         {"MemberId":"1496","RealName":"\u674e\u660a\u708e","NickName":"Mole","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180531124357\/207a8569613fd96ffc00a43cde90bdf2\/0","sUrl":"","Place":"0","GameName":"BLGMole","GamePlace":"2,"},
#         {"MemberId":"1536","RealName":"\u9648\u5bb6\u8c6a","NickName":"M1anhua","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180606135346\/0a48f98de2491f7768dd460bf87250d1\/0","sUrl":"","Place":"0","GameName":"BLGM1anhua","GamePlace":"5,"},
#         {"MemberId":"1823","RealName":"\u674e\u5728\u70e8","NickName":"Chieftain","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180531123937\/fc9eee440fc31b92e2d89f1a26782374\/0","sUrl":"","Place":"0","GameName":"BLGChieftain","GamePlace":"5,"}],
# "historyPlayers":[
#     {"MemberId":"554","sDate":"2016-05-19","eDate":"2016-12-28","RealName":"\u8d75\u5fd7\u94ed","NickName":"mitty","UserIcon":"http:\/\/shp.qpic.cn\/lolwebvideo\/201501\/c6045c0ad6798911e4c7a5181207ae0a\/0","sUrl":"","Place":"1","GameName":"IMmitty","GamePlace":"5,"},
#     {"MemberId":"452","sDate":"2016-01-01","eDate":"2016-12-01","RealName":"\u738b\u4f51\u519b","NickName":"Baybay","UserIcon":"http:\/\/shp.qpic.cn\/lolwebvideo\/201501\/ec8f4262cd5d7b00bbd135e89323f395\/0","sUrl":"","Place":"1","GameName":"AHQBayBay","GamePlace":"5,"},
#     {"MemberId":"289","sDate":"2016-01-01","eDate":"2016-12-01","RealName":"\u8303\u4fca\u4f1f","NickName":"avoidless","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180726090725\/21e7f22934024212a057892323c7ea04\/0","sUrl":"","Place":"1","GameName":"VTGavoidless","GamePlace":"5,"},
#     {"MemberId":"290","sDate":"2016-01-01","eDate":"2016-12-01","RealName":"\u59dc\u58e4\u8d24","NickName":"baeme","UserIcon":"http:\/\/shp.qpic.cn\/lolwebvideo\/201501\/60acd83b5f00cd46292e4acbac806cd5\/0","sUrl":"","Place":"2","GameName":"IMBaeme","GamePlace":"2,"},
#     {"MemberId":"1179","sDate":"2016-12-01","eDate":"2017-12-01","RealName":"\u6210\u6f14\u4fca","NickName":"Flawless","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180609120934\/8ddb309d831f70ac36640f798d943637\/0","sUrl":"","Place":"2","GameName":"RWFlawless","GamePlace":"5,"},
#     {"MemberId":"1473","sDate":"2018-01-09","eDate":"2018-06-09","RealName":"\u8d75\u5965\u8fea","NickName":"Aodi","UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180609212432\/3054ac2007d8c7c20580a0d0b4535cd8\/0","sUrl":"","Place":"0","GameName":"VGAodi","GamePlace":"1,"}
#     ],
#     "teamAwards":null}}


# {"status":"0",
#  "msg":{
#      "baseInfo":{
#          "MemberId":"14",
#          "RealName":"\u7b80\u81ea\u8c6a",
#          "EnName":"Uzi",
#          "NickName":"Uzi",
#          "MemberDesc":"Uzi\u662f\u4e16\u754c\u4e0a\u6700\u53d7\u6b22\u8fce\u7684\u9009\u624b\u4e4b\u4e00\u3002Uzi\u5728\u4e2d\u56fd\u4eba\u79f0\u201c\u72c2\u5c0f\u72d7\u201d\uff0c\u8fd9\u4f4d\u8001\u5c06\u4fdd\u6301\u7740\u4e00\u8d2f\u7684\u6700\u9ad8\u7ade\u6280\u6c34\u51c6\u3002\u4ed6\u57282014\u5e74\u4f5c\u4e3a\u804c\u4e1a\u9009\u624b\u52a0\u5165Royal\u3002\u540c\u5e74TGA\u51ac\u5b63\u603b\u51b3\u8d5b\u4f20\u5947\u7684\u4e94\u6740\uff0c\u8ba9\u4ed6\u8fdb\u5165\u4e86\u4eba\u4eec\u7684\u89c6\u7ebf\u3002",
#          "UserIcon":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180607133737\/a41134b8d0612d31e5b95835f3ef86a7\/0",
#          "sUrl":"",
#          "Place":"1",
#          "GameDate":"2015-01-01",
#          "GameName":"RNGUzi",
#          "GamePlace":"3,",
#          "GameHero":"412,111,67,15,429,67,51,236,236,15,67,",
#          "TeamId":"8",
#          "TeamName":"RNG",
#          "UserStatus":"1",
#          "iVoteStatus":"0",
#          "UserPhoto550":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20180607133826\/efa16287a630e78851c31d68534fc3d3\/0",
#          "UserPhoto155":"http:\/\/img.crawler.qq.com\/lolwebvideo\/20170608112546\/3bff0d966be3c87045da936978281168\/0"},
#      "favoriteHeros":[{"HeroId":"81",
#                        "UseNum":"40",
#                        "WinNum":"25",
#                        "sUpdated":"2018-08-04 17:30:03"},
#                       {"HeroId":"22",
#                        "UseNum":"29",
#                        "WinNum":"19",
#                        "sUpdated":"2018-06-30 22:20:08"},
#                       {"HeroId":"15","UseNum":"24","WinNum":"14","sUpdated":"2017-07-23 20:20:05"},
#                       {"HeroId":"110","UseNum":"22","WinNum":"15","sUpdated":"2018-04-22 00:00:08"},
#                       {"HeroId":"51","UseNum":"20","WinNum":"13","sUpdated":"2018-03-30 11:30:08"},
#                       {"HeroId":"96","UseNum":"19","WinNum":"9","sUpdated":"2018-04-28 19:00:08"},
#                       {"HeroId":"236","UseNum":"17","WinNum":"12","sUpdated":"2018-07-06 19:50:06"},
#                       {"HeroId":"202","UseNum":"12","WinNum":"7","sUpdated":"2017-02-17 19:40:06"}],
#      "historyTeams":[
#          {"TeamId":"8","TeamName":"RNG","sDate":"2016-05-19","eDate":"0000-00-00",
#           "TeamLogo":"http:\/\/img.crawler.qq.com\/lolwebvideo\/201712250188\/dbd34ea3f5daa0e70431f3bf77a2cfc3\/0",
#           "sUrl":"","TeamEnName":"RoyalNeverGiveUp"},
#          {"TeamId":"7","TeamName":"Newbee","sDate":"2015-12-27","eDate":"2016-05-19",
#           "TeamLogo":"http:\/\/img.crawler.qq.com\/lolwebvideo\/201712250188\/27cb76381cb71b7f2888f91193b2ab65\/0",
#           "sUrl":"","TeamEnName":"FunPlusPhoenix"}
#       ],
#      "playerAwards":null}}


