from webapp import create_app
from webapp.data_reddit import make_requests2

app = create_app()
with app.app_context():
    LIMIT = int(input("Введите количество топ-новостей: "))
    make_requests2(LIMIT)