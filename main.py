import os
import sys
from dotenv import load_dotenv
import requests


class Downloader:
    def __init__(self):
        load_dotenv()
        bearer_token = os.getenv('BEARER_TOKEN')
        self.headers = {"Authorization": "Bearer {}".format(bearer_token)}

    def download_first_variant(self, tweet_url):
        api_url = self.get_api_url(tweet_url)
        data = self.connect_to_endpoint(api_url)
        videos = self.get_videos_info(data)
        print('Downloading video of tweet {}'.format(self.get_id(tweet_url)))
        first_video = videos[0]
        video_data = requests.get(first_video['url'], allow_redirects=True)
        filename = '{}_{}x{}.mp4'.format(self.get_id(tweet_url), first_video['width'], first_video['height'])
        open(filename, 'wb').write(video_data.content)
        print('Saved at {}'.format(filename))

    def get_api_url(self, tweet_url):
        tweet_id = self.get_id(tweet_url)
        api_url = 'https://api.twitter.com/1.1/statuses/show/{}.json?tweet_mode=extended'.format(tweet_id)
        return api_url

    def get_id(self, tweet_url):
        tweet_id = tweet_url.split('/')[-1]
        to_remove = tweet_id.find('?')
        if to_remove != 1:
            tweet_id = tweet_id[0:to_remove]
        return tweet_id

    def connect_to_endpoint(self, api_url):
        response = requests.get(api_url, headers=self.headers)
        return response.json()

    def get_videos_info(self, data):
        raw_info = data['extended_entities']['media'][0]['video_info']['variants']
        raw_info = filter(self.is_variant_valid, raw_info)
        info = list(map(self.extract_video_info, raw_info))
        return info

    def is_variant_valid(self, variant):
        return variant['content_type'] == 'video/mp4'

    def extract_video_info(self, raw_info):
        video_url = raw_info['url']
        sizes = self.get_video_sizes(video_url)
        return {
            'width': sizes[0],
            'height': sizes[1],
            'url': video_url
        }

    def get_video_sizes(self, video_url):
        definition = video_url.split('/')[-2]
        return definition.split('x')


if __name__ == '__main__':
    print('Welcome to the Twitter Video Downloader')
    url = sys.argv[1]
    downloader = Downloader()
    downloader.download_first_variant(url)
