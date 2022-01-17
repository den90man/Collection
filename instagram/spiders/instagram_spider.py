import json
import re
import scrapy
from scrapy.http import HtmlResponse
from instagram.items import InstagramItem


class InstagramSpiderSpider(scrapy.Spider):
    name = 'instagram_spider'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = '	https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'den1090men'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1642381797:ATRQAFMIjaZTka90i33zaafd2fFVQDnha/ArJk2Q002gCNYupS/HMZQT9ndLqIbI+VGzFYcltuPtEtXsHbxKcT23AtiolXNBSEO7tTyrTSGARhXN91tO/lsu0ov+ni+Bs3rf4gKNrFPWEMOxB46AudM='
    users = ['likainart', 'gordienko_artur']
    followers_link = 'https://i.instagram.com/api/v1/friendships/'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
                                 headers={'X-CSRFToken': csrf}
                                 )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            for user in self.users:
                yield response.follow(f'/{user}', callback=self.user_parsing, cb_kwargs={'username': user})

    def user_parsing(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text)
        subscribers_url = f'{self.followers_link}{user_id}/followers/?count=12&search_surface=follow_list_page'
        following_url = f'{self.followers_link}{user_id}/following/?count=12'
        urls = [subscribers_url, following_url]
        for link_url in urls:
            yield response.follow(link_url, callback=self.user_parse_details,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                  cb_kwargs={'username': username, 'user_id': user_id, 'link_url': link_url})

    def user_parse_details(self, response: HtmlResponse, username, user_id, link_url):
        j_data = response.json()
        next_max_id = j_data.get('next_max_id')
        if next_max_id:
            subscribers_url = f'{self.followers_link}{user_id}/followers/?count=12&max_id={next_max_id}&search_surface=follow_list_page'
            following_url = f'{self.followers_link}{user_id}/following/?count=12&max_id={next_max_id}'
            urls = [subscribers_url, following_url]
            for link_url in urls:
                yield response.follow(link_url, callback=self.user_parse_details,
                                      headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                      cb_kwargs={'username': username, 'user_id': user_id, 'link_url': link_url})
        users = j_data.get('users')
        for user in users:
            if re.match(r'.+/followers/.+', response.url):
                item = InstagramItem(user_id=user_id, username=username, subscriber_user_id=user['pk'],
                                     subscriber_username=user['username'], subscriber_photo_url=user['profile_pic_url'])
                yield item

            elif re.match(r'.+/following/.+', response.url):
                item = InstagramItem(user_id=user_id, username=username, following_user_id=user['pk'],
                                     following_username=user['username'], following_photo_url=user['profile_pic_url'])
                yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text):
        matched = re.search('\"profilePage_\\d+\"', text).group()
        return matched.split('_')[-1].replace(r'"', '')
