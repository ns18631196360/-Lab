# -*- coding: utf-8 -*-

from elasticsearch_dsl import DocType, Completion, Keyword, Text, Integer, Long

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections

# 新建连接
connections.create_connection(hosts=["47.94.248.236"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleArtist(DocType):
    # 歌手的文档类型
    # suggest 字段
    suggest = Completion(analyzer=ik_analyzer)

    # 歌手的id
    artist_id = Integer()
    # 歌手名
    artist_name = Text(analyzer="ik_max_word")
    # 歌手详情页面的 url
    aritst_url = Keyword()
    # 歌手的所有专辑页的 url
    album_list_url = Keyword()
    # 歌手的所有专辑数量
    album_list_num = Integer()
    # 歌手的所有歌曲数量
    artist_song_num = Integer()
    # 所属平台
    artist_platform = Keyword()


    class Index:
        name = 'musicartist'
        doc_type = "artist"

    class Meta:
        index = "musicartist"
        doc_type = "artist"




class ArticleAlbum(DocType):
    # 歌手的文档类型
    # suggest 字段
    suggest = Completion(analyzer=ik_analyzer)

    # 专辑id
    album_id = Integer()
    # 专辑的url
    album_url = Keyword()
    # 专辑的名称
    album_name = Text(analyzer="ik_max_word")
    # 专辑的图片url
    album_pic = Keyword()
    # 专辑的歌手列表
    album_artist_list = Keyword()
    # 专辑发布日期
    album_date = Long()
    # 所属平台
    album_platform = Keyword()


    class Index:
        name = 'musicalbum'
        doc_type = "album"

    class Meta:
        index = "musicalbum"
        doc_type = "album"



class ArticleSong(DocType):
    # 歌手的文档类型
    # suggest 字段
    suggest = Completion(analyzer=ik_analyzer)

    # 歌曲id
    song_id = Integer()
    # 歌曲页面的 url
    song_url = Keyword()
    # 歌曲的歌词
    lyric = Text(analyzer="ik_max_word")
    # 歌曲名
    song_name = Text(analyzer="ik_max_word")
    # 唱歌曲的歌手列表
    song_artist_list = Keyword()
    # 所属的专辑名称
    song_album = Keyword()
    # 所属平台
    song_platform = Keyword()

    class Index:
        name = "musicsong"
        doc_type = "song"

    class Meta:
        index = "musicsong"
        doc_type = "song"



if __name__ == "__main__":
    ArticleArtist.init()
    ArticleAlbum.init()
    ArticleSong.init()
