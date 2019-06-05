# -*- coding: utf-8 -*-
from scrapy.conf import settings
from MiGu.items import ArtistItem, AlbumItem, SongItem

from elasticsearch_dsl.connections import connections

from MiGu.models.es_types import ArticleArtist, ArticleAlbum, ArticleSong

es = connections.create_connection(hosts=["47.94.248.236"])


# from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

def gen_suggests(index: object, info_list: object) -> object:
    # 根据字符串生成搜索建议数组
    used_words = set()
    # 获取过去生成的 suggest 字段集合
    suggests = []
    # 定义数组存放生成的 suggest 字段

    for text, weight in info_list:
        if text:
            # 调用es的analyze接口分析字符串、通过分词器生成 suggest 字段集合
            #words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            words = es.indices.analyze(index=index,body={'text':text,'analyzer':"ik_max_word",'filter':["lowercase"] })
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


def save_artist_to_es(item):
    article = ArticleArtist()

    #article.artist_id = item['artist_id']
    article.artist_name = item["artist_name"]
    article.aritst_url = item["artist_url"]
    article.album_list_url = item["album_list_url"]
    article.album_list_num = item["album_list_num"]
    article.artist_song_num = item["artist_song_num"]
    article.artist_platform = item["artist_platform"]

    article.suggest = gen_suggests("musicartist", [(article.artist_name, 10)])

    try:
        article.save()
    except Exception as e:
        print(e)
        return "fail"

    return "sucess"


def save_album_to_es(item):
    article = ArticleAlbum()

    # article.album_id = item['album_id']
    article.album_url = item["album_url"]
    article.album_pic = item["album_pic"]
    article.album_name = item["album_name"]
    article.album_artist_list = str(item["album_artist_list"])
    article.album_date = item["album_date"]
    article.album_platform = item["album_platform"]

    article.suggest = gen_suggests("musicalbum", [(article.album_name, 10)])

    try:
        article.save()
    except Exception as e:
        print(e)
        return "fail"

    return "sucess"


def save_song_to_es(item):
    article = ArticleSong()

    # article.song_id = item['song_id']
    article.song_url = item["song_url"]
    article.lyric = item["lyric"]
    article.song_name = item["song_name"]
    article.song_artist_list = str(item["song_artist_list"])
    article.song_album = item["song_album"]
    article.song_platform = item["song_platform"]

    article.suggest = gen_suggests("musicsong", [(article.song_name, 10)])

    try:
        article.save()
    except Exception as e:
        print(e)
        return "fail"

    return "sucess"


class ElasticsearchPipeline(object):
    # 将数据写入到es中

    def process_item(self, item, spider):

        # 将item转换为es的数据
        if isinstance(item, ArtistItem):
            result = save_artist_to_es(item)
            print('ArtistItem - > ' + result)

        elif isinstance(item, AlbumItem):
            result = save_album_to_es(item)
            print('AlbumItem - > ' + result)

        elif isinstance(item, SongItem):
            result = save_song_to_es(item)
            print('AlbumItem - > ' + result)

        return item


#将数据写入 mangodb
# class WangyiyunPipeline(object):
#
#     def __init__(self):
#         client = pymongo.MongoClient(
#             settings['MONGODB_HOST'],
#             settings['MONGODB_PORT']
#         )
#         db_name = settings['MONGODB_DBNAME']
#         self.db = client[db_name]
#         self.artist = self.db[settings['MONGODB_COL_ARTIST']]
#         # 不能同时生成多个，只能通过isinstance的方法判断
#         # self.album = db[settings['MONGODB_COL_ALBUM']]
#         # self.album_list = db[settings['MONGODB_COL_ALBUMLIST']]
#         # self.song = db[settings['MONGODB_COL_SONG']]
#
#     def process_item(self, item, spider):
#         '''不同的item类型，放入不同的集合中，
#
#         分为四块：Items - col - dict - desc ：
#             WYYArtistItem - > self.aritst - > artist_infos -> 所有的歌手列表
#             WYYAlbumItem - > self.ablum - > album_infos - > 每个歌手的所有专辑列表
#             WYYAlbumListItem - > self.album_list - > album_list_infos - > 每张专辑内的所有歌曲列表
#             WYYSongItem - > self.song -> song_infos -> 每首歌曲的信息
#         '''
#
#         # if item['artist_id'] == 860734:
#         #     print("????")
#
#         if isinstance(item, WYYArtistItem):
#             artist_infos = dict(item)
#             self.artist = self.db[settings['MONGODB_COL_ARTIST']]
#             self.artist.insert_one(artist_infos)
#             print('WYYArtistItem - > success')
#
#         elif isinstance(item, WYYAlbumItem):
#             album_infos = dict(item)
#             self.artist = self.db[settings['MONGODB_COL_ALBUM']]
#             self.artist.insert_one(album_infos)
#             print('WYYAlbumItem - > success')
#
#         # elif isinstance(item,WYYAlbumListItem):
#         #     album_list_infos = dict(item)
#         #     self.artist = self.db[settings['MONGODB_COL_ALBUMLIST']]
#         #     self.artist.insert_one(album_list_infos)
#         #     print('WYYAlbumListItem - > success')
#
#         elif isinstance(item, WYYSongItem):
#             song_infos = dict(item)
#             self.artist = self.db[settings['MONGODB_COL_SONG']]
#             self.artist.insert_one(song_infos)
#             print('WYYSongItem - > success')
#
#         return item
