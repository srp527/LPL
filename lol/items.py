# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class PlayerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    MemberId = Field()
    NickName = Field()
    RealName = Field()
    Place = Field()
    GameName = Field()
    GamePlace = Field()
    UserIcon = Field()


class TeamItem(Item):
    TeamName = Field()
    TeamEnName = Field()
    TeamDesc = Field()
    TeamLogo = Field()
    TeamId = Field()


class BaseInfoItem(Item):
    EnName = Field()
    GameDate = Field()
    GameHero = Field()
    GameName = Field()
    GamePlace = Field()
    MemberDesc = Field()
    MemberId = Field()
    NickName = Field()
    RealName = Field()
    TeamId = Field()
    TeamName = Field()
    UserIcon = Field()


class FavoriteHerosItem(Item):
    HeroId = Field()
    UseNum = Field()
    WinNum = Field()
    sUpdated = Field()


class PlayerAwardsItem(Item):
    AwardDesc = Field()
    RankName = Field()
    sGameName = Field()

