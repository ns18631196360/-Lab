#coding=UTF-8
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from MiGu.items import SongItem
from selenium import webdriver
from  selenium.webdriver.chrome.options import Options
from MiGu.items import ArtistItem
from MiGu.items import AlbumItem
import re
import datetime

class spider(CrawlSpider):
    # 定义爬虫程序的名称，用于程序的启动使用
    name = 'MiGu'
    # 定义爬虫程序运行的作用域
    allow_domains = ['music.migu.cn']
    # #定义起始爬取页面
    start_urls = ['http://music.migu.cn/v3/music/album']
    #start_urls = ['http://music.migu.cn/v3/music/song/69915800051']
    #定义超链接的提取规则
    page_link = LinkExtractor(allow=('http://music.migu.cn/v3/music*'))
    #定义爬虫爬取数据的规则
    rules = (Rule(link_extractor=page_link,callback='parse_content', follow=True),)
    domain = 'http://music.migu.cn'
    # 建立driver
    # chrome_options = Options()
    # #chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    # # 指定谷歌浏览器路径
    # driver = webdriver.Chrome(chrome_options=chrome_options,
    #                                executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver')

    # def parse_1(self, response):
    #     #解析文章列表页
    #     urls = response.xpath('//div[@class="artist-item"]/a/@href').extract()
    #     for url in urls:
    #         url = self.domain + "".join(url)
    #         print url
    #         request = scrapy.http.Request(url=url, callback='parse_content', dont_filter=True)
    #         request.meta['PhantomJS'] = True
    #         yield request

    #定义爬虫获取到的相应数据处理类
    def parse_content(self, response):
        print ('进入spider')
        domain = 'http://music.migu.cn'
        song_list = response.xpath('//div[@class="songInfo"]/div[@class="container songinfoCon"]/div[@class="info_contain"]')
        #print (song_list)
        for song in song_list:
            item = SongItem()
            item['song_name'] = "".join(song.xpath('.//h2[@class="info_title"]/text()').extract())
            print (item['song_name'])
            #original_url = song.xpath('./div[@class="song-name clearfix"]/span[@class="song-name-text"]/a/@href/text()').extract()
            #获取当前歌曲页url
            split_url = "".join(response.request.url)
            item['song_url'] = split_url
            print(item['song_url'])
            song_artist_list = song.xpath('./div[@class="info_singer"]/a')
            artist_list = {}
            for song_artist in song_artist_list:
                song_artist_text= "".join(song_artist.xpath('./text()').extract())
                ar_list_url = domain + "".join(song_artist.xpath('./@href').extract())
                artist_list[song_artist_text] = ar_list_url
            item['song_artist_list'] = artist_list
            print(item['song_artist_list'])
            song_album_list = song.xpath('./div[@class="info_about"]/p[@class="about_blog"]/span[@class="blog_name"]/a')
            album_list = ''
            for song_album in song_album_list:
                album_list += "".join(song_album.xpath('./text()').extract())
            item['song_album'] = album_list
            print(item['song_album'])
            lyric_list = response.xpath('//div[@class="container songLyr clearfix"]//div[@class="lyric"]/div[@class="info-contain lyr-contain"]/p[@class="lyric-text"]')
            all_lyric = ""
            for lyric in lyric_list:
                all_lyric += "".join(lyric.xpath('./text()').extract())
            item['lyric'] = all_lyric
            print(all_lyric)
            item['song_platform'] = '咪咕音乐'
            print ('爬到一条')
            yield item

        Album_list = response.xpath('//div[@class="container"]/div[@class="mal-album-list"]/ul/li')
        for album in Album_list:
            item = AlbumItem()
            item['album_name'] = "".join(album.xpath('./a/text()').extract())
            album_url = domain + "".join(album.xpath('./div[@class="thumbnail"]/a/@href').extract())
            item['album_url'] = album_url
            item['album_pic'] = "".join(album.xpath('./div[@class="thumbnail"]/a/img/@src').extract())
            #制作歌手列表字典
            album_artist_list = album.xpath('./div[@class="album-singers"]/a')
            al_artist_list = {}
            for al_artist in album_artist_list:
                al_artist_text = "".join(al_artist.xpath('./text()').extract())
                al_artist_url = domain + "".join(al_artist.xpath('./@href').extract())
                al_artist_list[al_artist_text] = al_artist_url
            item['album_artist_list'] = al_artist_list
            album_date = "".join(album.xpath('./div[@class="album-release-date"]/span/text()').extract())
            #album_date_result = re.search('(\d+)-(\d+)-(\d+)', album_date)
            #转时间为时间戳
            try:
                pub_time = datetime.datetime.strptime(album_date,"%Y-%m-%d")
                print(pub_time)
                item['album_date'] = int((pub_time-datetime.datetime(1970,1,1,8)).total_seconds())*1000
            except:
                item['album_date'] = -1
            #item['album_date'] = album_date_result.group(1)+album_date_result.group(2)+album_date_result.group(3)
            item['album_platform'] = '咪咕音乐'
            yield item

        Artist_list = response.xpath('//div[@id="J_ArtistDetailPage"]/div[@class="artist-info"]/div[@class="container"]')
        for singer_list in Artist_list:
            item = ArtistItem()
            item['artist_name'] = "".join(singer_list.xpath('./div[@class="artist-name"]/a/text()').extract())
            item['artist_url'] = domain + "".join(singer_list.xpath('./div[@class="artist-name"]/a/@href').extract())
            album_url = domain + "".join(response.xpath('//div[@id="J_ArtistDetailPage"]/div[@class="artist-section container"]/div[@class="artist-section-title"]/a/@href').extract()[1])
            item['album_list_url'] = album_url
            num = "".join(response.xpath(
                '//div[@id="J_ArtistDetailPage"]/div[@class="artist-section container"]/div[@class="artist-section-title"]/a/text()').extract())
            album_num = re.search('全部(\d*)张', num).group(1)
            print(album_num)
            item['album_list_num'] = album_num
            song_num = re.search('全部(\d*)首', num).group(1)
            print(song_num)
            item['artist_song_num'] = song_num
            item['artist_platform'] = '咪咕音乐'
            yield item

