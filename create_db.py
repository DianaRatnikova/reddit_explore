from webapp import db, create_app

# db.create_all(app=create_app())
app=create_app()
with app.app_context():
    db.create_all()