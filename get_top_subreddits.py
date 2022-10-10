from webapp import create_app
from webapp.data_reddit import main_request

app = create_app()
with app.app_context():
    main_request()