import requests
from os import environ as env
from dotenv import load_dotenv, find_dotenv #для .env
# Используемые ресурсы:
# https://github.com/reddit-archive/reddit/wiki/OAuth2
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c


load_dotenv(find_dotenv())
print(f" {env['CLIENT_ID'] = }")

# login method (password), username, and password
data = {'grant_type': 'password',
        'username': env['username'],
        'password': env['password']}


auth = requests.auth.HTTPBasicAuth(env['CLIENT_ID'], env['SECRET_TOKEN'])


# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'Reddit_Explore/0.0.1'}


# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
def make_requests():
    result = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    print("requests.get was done")
    print(f'{result.status_code =}')
    print(f"{result.headers['content-type']=}")
    print(f'{result.text=}')
    print(f'{result.encoding=}')
    print(f'{type(result)=}')

    result.raise_for_status()
    print(result.json())
    return result

result = make_requests()
res = requests.get("https://oauth.reddit.com/r/python/new",headers=headers)


# loop through each post retrieved from GET request
for post in res.json()['data']['children']:
    # append relevant data to dataframe
    df = {
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }
