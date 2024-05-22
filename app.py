from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager
from auth import auth as auth_blueprint
from image_processing import image as image_blueprint
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = 'uploads/'  # Ensure this folder exists

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(image_blueprint, url_prefix='/')

    # Add route for the "About" section
    @app.route('/about')
    def about():
        return render_template('about.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
