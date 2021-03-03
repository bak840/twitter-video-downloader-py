import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import requests


def sort_bitrate(value):
    return value['bitrate']


class Downloader:
    def __init__(self):
        load_dotenv()
        bearer_token = os.getenv('BEARER_TOKEN')
        self.headers = {"Authorization": "Bearer {}".format(bearer_token)}

    def download_biggest_variant(self, tweet_url):
        videos = self.fetch_videos_infos(tweet_url)
        video = sorted(videos, key=sort_bitrate, reverse=True)[0]
        self.download_video(video, self.get_id(tweet_url))

    def download_smallest_variant(self, tweet_url):
        videos = self.fetch_videos_infos(tweet_url)
        video = sorted(videos, key=sort_bitrate)[0]
        self.download_video(video, self.get_id(tweet_url))

    def download_video(self, video_info, tweet_id):
        video_data = requests.get(video_info['url'], allow_redirects=True)
        filename = '{}_{}x{}.mp4'.format(tweet_id, video_info['width'], video_info['height'])
        download_path = self.get_download_path()
        filepath = os.path.join(download_path, filename)
        if not os.path.exists(filepath):
            print('Downloading video of tweet {}'.format(tweet_id))
            open(filepath, 'wb').write(video_data.content)
            print('Saved at {}'.format(filepath))
        else:
            print('Video already downloaded at {}'.format(filepath))

    def fetch_videos_infos(self, tweet_url):
        api_url = self.get_api_url(tweet_url)
        data = self.connect_to_endpoint(api_url)
        videos = self.get_videos_info(data)
        return videos

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
            'bitrate': raw_info['bitrate'],
            'width': int(sizes[0]),
            'height': int(sizes[1]),
            'url': video_url
        }

    def get_video_sizes(self, video_url):
        definition = video_url.split('/')[-2]
        return definition.split('x')

    def get_download_path(self):
        return os.getenv('DOWNLOAD_PATH') or os.path.join(Path.home(), 'Downloads')


if __name__ == '__main__':
    print('Welcome to the Twitter Video Downloader')
    url = sys.argv[1]
    downloader = Downloader()
    downloader.download_biggest_variant(url)
