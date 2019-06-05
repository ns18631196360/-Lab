# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import  ItemLoader
from  scrapy.loader.processors import TakeFirst, MapCompose, Join


class ArtistItem(scrapy.Item):
    '''获取所有歌手url
    '''
    #_id = scrapy.Field()
    #歌手的id
    #artist_id = scrapy.Field()
    #歌手名
    artist_name = scrapy.Field()
    #歌手详情页面的 url
    artist_url = scrapy.Field()
    #歌手的所有专辑页的 url
    album_list_url = scrapy.Field()
    #歌手的所有专辑数量
    album_list_num = scrapy.Field()
    #歌手的所有歌曲数量
    artist_song_num = scrapy.Field()
    #所属平台
    artist_platform = scrapy.Field()

    # def get_insert_sql(self):
    #     insert_sql = """
    #         insert into artist(name,url,album_num,platform)
    #         VALUES (%s, %s, %s, %s)
    #     """
    #
    #     params = (self["artist_name"], self["artist_url"],self["album_list_num"],
    #               self["artist_platform"])
    #
    #     return insert_sql, params

class AlbumItem(scrapy.Item):
    '''专辑的所有歌列表
    '''
    #_id = scrapy.Field()
    #专辑id
    #album_id = scrapy.Field()
    #专辑的url
    album_url = scrapy.Field()
    # 专辑的名称
    album_name = scrapy.Field()
    #专辑的图片url
    album_pic = scrapy.Field()
    #专辑的歌手列表
    album_artist_list = scrapy.Field()
    #专辑发布日期
    album_date = scrapy.Field()
    #所属平台
    album_platform = scrapy.Field()
    # def get_insert_sql(self):
    #     insert_sql = """
    #         insert into album(name,url,pic_url,artist,date,platform)
    #         VALUES (%s, %s, %s, %s, %s, %s)
    #     """
    #
    #     params = (self["album_name"], self["album_url"],self["album_pic"], self["album_artist_list"],
    #               self["album_date"], self["album_platform"])
    #
    #     return insert_sql, params

class SongItem(scrapy.Item):
    '''每首歌信息
    '''
    #_id = scrapy.Field()
    #歌曲id
    song_id = scrapy.Field()
    # 歌曲名
    song_name = scrapy.Field()
    #歌曲页面的 url
    song_url = scrapy.Field()
    #歌曲的歌词
    lyric = scrapy.Field()
    #唱歌曲的歌手列表
    song_artist_list = scrapy.Field()
    #所属的专辑名称
    song_album = scrapy.Field()
    #所属平台
    song_platform = scrapy.Field()

    # def get_insert_sql(self):
    #     insert_sql = """
    #         insert into song(title,url,singer,album,platform)
    #         VALUES (%s, %s, %s, %s, %s)
    #     """
    #     print('歌曲插入')
    #     params = (self["song_name"], self["song_url"],self["song_artist_list"],
    #               self["song_album"],self["song_platform"])
    #
    #     return insert_sql, params