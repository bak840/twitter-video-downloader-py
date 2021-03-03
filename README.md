# Twitter Video Downloader

This is a simple script to download twitter videos by using Python and the Twitter API.

Before getting started, you need python installed on your computer. If that is not the case you can download it at the
following [link](https://www.python.org/downloads/). I have used Python 3.9 but it can probably work with Python 3.6.

## Get Bearer Token for Twitter API

You need a bearer token to make requests to the Twitter API. Here is how you can get one.

1. Login to your Twitter account on [developer.twitter.com](developer.twitter.com).
1. Navigate to the [Twitter App dashboard](https://developer.twitter.com/en/portal/projects-and-apps)
1. If you have an existing app, go to the next step. If not, to create an app, you will be first asked to create a
   project. You can give the app the name you want. When asked the access level required for your app, select Read Only,
   it will be enough for the script to work.
1. Open the app and navigate to the "keys and tokens" page.
1. You'll find the "bearer token" on this page.

## Prepare the script

1. Clone the repo and open the project folder in the terminal.
1. Run this script to install the dependencies of the project:

`pip install -r requirements.txt`

## Configure the environment variables

This script reads the Twitter bearer token from .env file.

1. Create a file named ".env" in the project folder.
1. Refer to the file named .env.sample for the structure.
1. Copy and paste the bearer token for the app you have created earlier on the BEARER_TOKEN line (without the <>).
1. If you want for the videos to be downloaded in a folder different from the default downloads folder, copy the path to
   the DOWNLOAD_PATH line.

## Run the script

In a terminal window opened to the project folder you just need to run:

`python3 main.py <tweet url of the video>`