import string
from flask import Flask
import requests
from os import environ as env
from dotenv import load_dotenv, find_dotenv #для .env
from webapp.model import db, Top_Subreddit
# import json
import webapp.config
import os

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


def authentication():
#=========Without env=============
    data = {'grant_type': 'password',
            'username': webapp.config.user_name,
            'password': webapp.config.password}

    print(f"{webapp.config.user_name = }")
    print(f"{webapp.config.password = }")

# указываем параметры аутентификации
    auth = requests.auth.HTTPBasicAuth(webapp.config.CLIENT_ID, webapp.config.SECRET_TOKEN)
    result_post = requests.post('https://www.reddit.com/api/v1/access_token',
                                auth=auth, data=data, headers=webapp.config.HEADERS_INFO)
    # convert response to JSON and pull access_token value
    TOKEN = result_post.json()['access_token']
    # add authorization to our headers dictionary
    headers = {**webapp.config.HEADERS_INFO, **{'Authorization': f"bearer {TOKEN}"}}

    print(f"{webapp.config.HEADERS_INFO = }")
    print(f"{TOKEN = }")
    print(f"{headers = }")

    return headers


def print_result_post(result_post):
    print(f"{result_post = }")
    print("=========================")
    print(f"{result_post.status_code = }")
    print(f"{result_post.json() = }")
    print(f"{result_post.history = }")
    print(f"{result_post.cookies = }")
    print(f"{result_post.headers = }")
    print(f'{result_post.is_redirect=}')


def mkdir_for_results(FOLDER_NAME):
    if not os.path.isdir(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)
    os.chdir(FOLDER_NAME)

def write_comments_to_file(filename: str, comments: list, nesting: int):
    mkdir_for_results(webapp.config.FOLDER_NAME)

    with open(filename, 'a', encoding='utf-8') as file_comment_top_post:
        file_comment_top_post.write(nesting*"--- " + f"{comments['author']}: {comments['body']}\n")
    file_comment_top_post.close()
    os.chdir("..")


def show_all_comments(comments, nesting_of_comment, num_of_file):
    filename = "comment_for_top_post_"+str(num_of_file+1)+'.txt'
    if "author" in comments and "body" in comments:
        write_comments_to_file(filename, comments, nesting_of_comment)   
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
def make_comments_request(comments_url, num_of_file, headers):
    result_comments = requests.get(f'{comments_url}', headers=headers)
    # нулевой элемент списка содержит инфу о посте, первый - все комменты
    comment_json = result_comments.json()[1]['data']['children']
    print(f'Number of comments for post {num_of_file+1}: {len(comment_json)}')

    for comment_for_top_post in comment_json:
        show_all_comments(comment_for_top_post['data'], 0, num_of_file)


def write_subreddit_to_file(filename: str, top_post_info: list):
    mkdir_for_results(webapp.config.FOLDER_NAME)

    with open(filename, 'w', encoding='utf-8') as file_top_post:
        file_top_post.write(f"{top_post_info['subreddit']=}\n")
        file_top_post.write(f"{top_post_info['author']=}\n")
        file_top_post.write(f"{top_post_info['title']=}\n")
    os.chdir("..")

# loop through each post retrieved from GET request
def show_subreddit_data(result_subreddit, comments_url_list):
    filename_top_post = "top_post_"
    for (num_of_top_post, top_post) in enumerate(result_subreddit.json()["data"]["children"]):
        top_post_info = {
                        'subreddit': top_post["data"]["subreddit"],
                        'author': top_post["data"]["author"],
                        'title': top_post["data"]["title"],
                        'url': comments_url_list[num_of_top_post]
                        }

        filename = filename_top_post+str(num_of_top_post+1)+'.txt'
        write_subreddit_to_file(filename, top_post_info)
        save_top_subreddit_to_db(top_post_info['subreddit'],
                                 top_post_info['url'],
                                 top_post_info['author'],
                                 top_post_info['title'])


def construct_comments_url(result_subreddit: any) -> list:
    comments_url_list = []
    for post in result_subreddit.json()["data"]["children"]:
        comments_url = webapp.config.CONST_URL + post['data']['permalink']
        comments_url = comments_url[:-1]+'.json'  # сформирована ссылка на комменты
        comments_url_list.append(comments_url)
    return comments_url_list


# вытащить топовые посты
def make_top_subreddit_requests(LIMIT, headers):
# формирую словарь result_subreddit.json()
    result_subreddit = requests.get(f'https://oauth.reddit.com/top.json?limit={LIMIT}', headers=headers)

    print("\n------------request for top subreddits was done-----------")
    print(f'{result_subreddit.status_code =}')

    print("-----Comments_URL---------")
    comments_url_list = construct_comments_url(result_subreddit)
    print('\n'.join(comments_url_list))

    print(f"\n----TOP {LIMIT} news-------------------")
    show_subreddit_data(result_subreddit, comments_url_list)

    for (num_of_file, comment_url) in enumerate(comments_url_list):
        make_comments_request(comment_url, num_of_file, headers)
    return result_subreddit


def save_top_subreddit_to_db(subreddit: int, url: string, author: string, text: string):
    top_subreddit_exists = Top_Subreddit.query.filter(Top_Subreddit.url == url).count()
    print(f"{top_subreddit_exists=}")
# проверка, что новость уже существует:
    if not top_subreddit_exists: 
        new_top_subreddit = Top_Subreddit(subreddit=subreddit, url=url, author=author, text=text)
        db.session.add(new_top_subreddit)
        db.session.commit()


def main_request():
    LIMIT = int(input("Введите количество топ-новостей: "))
    headers = authentication()
    make_top_subreddit_requests(LIMIT, headers)

if __name__ == "__main__":
#    app.config.from_pyfile('config.py') # откуда брать параметры конфигурации
    main_request()
