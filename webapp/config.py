import imp
import os

from flask_sqlalchemy import SQLAlchemy

'''
Нужно задать путь к нашей sqlite-базе. 
Flask-SQLAlchemy ожидает найти этот параметр 
в конфигурации по ключу SQLALCHEMY_DATABASE_URI
'''

basedir = os.path.abspath(os.path.dirname(__file__))
# print(f"{__file__=}")
# print(f"{os.path.dirname(__file__) = }")
# print(f"{basedir = }")
# print(f"{os.path.join(basedir, '..', 'webapp.db')=}")


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'top_subreddit.db')