from flask_sqlalchemy import SQLAlchemy
'''
Модель описывает объект, который мы хотим сохранять в БД 
и получать из БД. SQLAlchemy будет делать 
всю работу по переводу с привычного нам python-синтаксиса 
на язык SQL.
'''

db = SQLAlchemy()

class Top_Subreddit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subreddit = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False) # = ссылка на страничку с комментами
    author = db.Column(db.String, nullable=False)
  #  published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True) #['title']

# что выведет Питон при print(News)
    def __repr__(self): # "магический метод Питона"
        return '<News {} {}>'.format(self.subreddit, self.url)