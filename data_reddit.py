import requests
from os import environ as env
from dotenv import load_dotenv, find_dotenv #для .env
import time

import json
# Используемые ресурсы:
# https://github.com/reddit-archive/reddit/wiki/OAuth2
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c




load_dotenv(find_dotenv()) #for ./env
print(f" {env['CLIENT_ID'] = }")

# login method (password), username, and password
data = {'grant_type': 'password',
        'username': env['username'],
        'password': env['password']}

print(f"{env['user_name']=}")
print(f"{env['password']=}")
# указываем параметры аутентификации
auth = requests.auth.HTTPBasicAuth(env['CLIENT_ID'], env['SECRET_TOKEN'])

#=========Without env=============
'''
data = {'grant_type': 'password',
        'username': user_name,
        'password': password}

print(f"{user_name = }")
print(f"{password = }")
# указываем параметры аутентификации
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)
'''
#=========================


# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'Reddit_Explore/0.0.1'}
print(f"{headers = }")

# send our request for an OAuth token

result_post = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

def print_result_post(result_post):
    print(f"{result_post = }")
    print("=========================")
    print(f"{result_post.status_code = }")
    print(f"{result_post.json() = }")
    print(f"{result_post.history = }")
    print(f"{result_post.cookies = }")
    print(f"{result_post.headers = }")
    print(f'{result_post.is_redirect=}')

# convert response to JSON and pull access_token value
TOKEN = result_post.json()['access_token']
print(f"{TOKEN = }")

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
print(f"{headers = }")

time.sleep(2.0)

# while the token is valid (~2 hours) we just add headers=headers to our requests
def make_requests1():
    result = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    print("requests.get was done")
    print(f'{result.status_code =}')
    print(f"{result.headers['content-type']=}")
    print(f"\n{result.headers =}\n\n")
    print(f'{result.text=}\n')
    try:
        print(f'\n{result.json()=}\n')
    except ValueError:
        print('ValueError: No JSON object could be decoded.')
    print(f'{result.encoding=}')
    print(f'{result.is_redirect=}')
    print(f'{result.elapsed=}')
    print(f'{result.url=}')
    print(f'{result.history=}')
    print(f'{type(result)=}')

    result.raise_for_status()
    print(f'{result.json()=}')
    return result

# result1 = make_requests1()
# res = requests.get("https://oauth.reddit.com/r/python/new",headers=headers)


# вытащить 3 самых популярных поста
def make_requests2():
    LIMIT = 3
    CONST_URL='https://www.reddit.com'
  # https://www.reddit.com/top.json?limit=3
    result_subreddit = requests.get(f'https://oauth.reddit.com/top.json?limit={LIMIT}', headers=headers)

    print("\n------------request for users/popular was done-----------")
    print(f'{result_subreddit.status_code =}')
    print(f"{result_subreddit.headers['content-type']=}")
    print(f"\n{result_subreddit.headers =}\n\n")
    print(f"\n{len(result_subreddit.json())=}\n")
    print(f"\n{result_subreddit.json().keys()=}\n")

    time.sleep(4.0)
    if "data" in result_subreddit.json().keys():
        if "children" in result_subreddit.json()["data"]:
            print("++++++") 
            for data_massive in result_subreddit.json()['data']['children']:
                if "data" in data_massive:
                    if "title" in data_massive["data"]:
                        print(f"{data_massive['data']['title'] = }")
                        print(f"{data_massive['data']['permalink'] = }")
                        print(f"{data_massive['data']['domain'] = }")
                        data_massive_url = CONST_URL + data_massive['data']['permalink']
                        data_massive_url = data_massive_url[:-1]+'.json'
                        print(f"{data_massive_url = }") #ссылка на пост с комментнариями
                        print("----------------------------")

    else:
        print('NO data!=========')            

    print(f'{result_subreddit.encoding=}')
    print(f'{result_subreddit.is_redirect=}')
    print(f'{result_subreddit.elapsed=}')
    print(f'{result_subreddit.url=}')
    print(f'{result_subreddit.history=}')
    print(f'{type(result_subreddit)=}')

    return result_subreddit

result2 = make_requests2()


# loop through each post retrieved from GET request
# for post in result2.json()["data"]["children"]:
#   # append relevant data to dataframe
#   df = {
#       'subreddit': post["data"]["subreddit"],
#       'title': post["data"]["title"],
#       'selftext': post["data"]["selftext"],
#       'upvote_ratio': post["data"]["upvote_ratio"],
#       'ups': post["data"]["ups"],
#       'downs': post["data"]["downs"],
#       'score': post["data"]["score"]
#   }
#   print(f"{df['subreddit']=}")
#   print(f"{df['title']=}")
#   print(f"{df['selftext']=}")
#   print(f"{df['upvote_ratio']=}")
#   print(f"{df['ups']=}")
#   print(f"{df['downs']=}")
#   print(f"{df['score']=}")
#   print("------------")


'''
def get_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()
'''