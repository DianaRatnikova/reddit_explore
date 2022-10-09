from flask import Flask
import requests
from os import environ as env
from dotenv import load_dotenv, find_dotenv #для .env
from webapp.model import db, Top_Subreddit
import json

from webapp.model import db

# Используемые ресурсы:
# https://github.com/reddit-archive/reddit/wiki/OAuth2
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
from pprint import pprint
from pprint import pformat


'''
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
'''

#=========Without env=============

data = {'grant_type': 'password',
        'username': user_name,
        'password': password}

print(f"{user_name = }")
print(f"{password = }")
# указываем параметры аутентификации
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

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


def show_all_comments(comments, nesting_of_comment, num_of_file):
    filename_comment_for_top_post = "comment_for_top_post_"+str(num_of_file+1)+'.txt'
    if "author" in comments and "body" in comments:
        with open( filename_comment_for_top_post, 'a', encoding='utf-8') as file_comment_top_post:
            file_comment_top_post.write(nesting_of_comment*"--- " + f"{comments['author']}: {comments['body']}\n")
        file_comment_top_post.close()
        author = comments['author']

    if 'replies' in comments:
        if comments['replies'] == '':
            #print(nesting_of_comment*"--- " + f"{comments['replies'] = } (No Replies)")
            nesting_of_comment -= 1
        else:
            for comments_dict in comments['replies']['data']['children']:
                if comments_dict['kind'] != "more":
                    nesting_of_comment += 1
                    show_all_comments(comments_dict['data'], nesting_of_comment, num_of_file)
                else:
                    pass
                #   print(nesting_of_comment*"--- "+f"(There are also {comments_dict['data']['count']} more replies for {author})")
                nesting_of_comment -= 1



# разбор странички с комментариями
def make_comments_request(comments_url, num_of_file):
    result_comments = requests.get(f'{comments_url}', headers=headers)

 #   print(f'{result_comments.status_code =}')
 #   print(f"{result_comments.headers['content-type']=}")
 #   print(f"{len(result_comments.json())=}\n")

# нулевой элемент списка содержит инфу о посте
# первый - все комменты
    comment_json=result_comments.json()[1]['data']['children']
    print(f'{len(comment_json) = }')

 #   print(':::::::::')
 #   show_all_comments(comment_json[0]['data'], 0)
    
    for comment_for_top_post in comment_json:
        print(':::::::::')
        show_all_comments(comment_for_top_post['data'], 0, num_of_file)


# loop through each post retrieved from GET request
def show_what_is_in_subreddit(result_subreddit, comments_url_dict):
    filename_top_post = "top_post_"
    for (num_of_top_post,top_post) in enumerate(result_subreddit.json()["data"]["children"]):
        top_post_info = {
       'subreddit': top_post["data"]["subreddit"],
       'author': top_post["data"]["author"],
       'title': top_post["data"]["title"],
       'url': comments_url_dict[num_of_top_post]
   }
        with open( filename_top_post+str(num_of_top_post+1)+'.txt', 'w', encoding='utf-8') as file_top_post:
            file_top_post.write(f"{top_post_info['subreddit']=}\n")
            file_top_post.write(f"{top_post_info['author']=}\n")
            file_top_post.write(f"{top_post_info['title']=}\n")
        save_top_subreddit(top_post_info['subreddit'], top_post_info['url'], top_post_info['author'], top_post_info['title'])
     #   save_top_subreddit("subreddit", "url", "author", "text")

def construct_comments_url(result_subreddit):
    comments_url_dict=[]
    CONST_URL='https://www.reddit.com'
    CONST_URL='https://oauth.reddit.com'
    for post in result_subreddit.json()["data"]["children"]:
        comments_url = CONST_URL + post['data']['permalink']
        comments_url = comments_url[:-1]+'.json'
        print(f"{comments_url = }")
        comments_url_dict.append(comments_url)
    return comments_url_dict


# вытащить 3 самых популярных поста
def make_requests2(LIMIT):
    CONST_URL='https://www.reddit.com'
  # https://www.reddit.com/top.json?limit=3

  # формирую словарь result_subreddit.json()
    result_subreddit = requests.get(f'https://oauth.reddit.com/top.json?limit={LIMIT}', headers=headers)

    print("\n------------request for users/popular was done-----------")
    print(f'{result_subreddit.status_code =}')
    print("-----Comments_URL---------")
    comments_url_dict = construct_comments_url(result_subreddit)
    print(f"{comments_url_dict = }")

    print(f"\n----TOP {LIMIT} news-------------------")
    show_what_is_in_subreddit(result_subreddit, comments_url_dict)

    for (num_of_file, comment_url) in enumerate(comments_url_dict):
        make_comments_request(comment_url, num_of_file)
    return result_subreddit


def save_top_subreddit(subreddit, url, author, text):
    top_subreddit_exists = Top_Subreddit.query.filter(Top_Subreddit.url == url).count()
    print(f"{top_subreddit_exists=}")
    #проверка, что новость уже существует:
    if not top_subreddit_exists: 
        new_top_subreddit = Top_Subreddit(subreddit=subreddit, url=url, author=author, text=text)
        db.session.add(new_top_subreddit)
        db.session.commit()

if __name__ == "__main__":
#    app.config.from_pyfile('config.py') # откуда брать параметры конфигурации
    LIMIT = int(input("Введите количество топ-новостей: "))
    result2 = make_requests2(LIMIT)

