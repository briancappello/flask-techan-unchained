import os
import redis

from appdirs import AppDirs
from datetime import timedelta
from flask_unchained import url_for
from flask_unchained import AppBundleConfig
from flask_unchained.utils import get_boolean_env
from werkzeug.local import LocalProxy


class Config(AppBundleConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    DEBUG = get_boolean_env('FLASK_DEBUG', False)
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'not-secret-key')  # FIXME

    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))

    app_dirs = AppDirs('flask-techan-unchained')

    APP_CACHE_FOLDER = app_dirs.user_cache_dir
    os.makedirs(APP_CACHE_FOLDER, exist_ok=True)

    APP_DATA_FOLDER = app_dirs.user_data_dir
    os.makedirs(APP_DATA_FOLDER, exist_ok=True)

    ##########################################################################
    # celery                                                                 #
    ##########################################################################
    CELERY_BROKER_URL = 'redis://{host}:{port}/0'.format(
        host=os.getenv('FLASK_REDIS_HOST', '127.0.0.1'),
        port=os.getenv('FLASK_REDIS_PORT', 6379),
    )
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL

    ##########################################################################
    # mail                                                                   #
    ##########################################################################
    MAIL_ADMINS = ['admin@example.com']  # FIXME
    MAIL_DEFAULT_SENDER = (
        os.environ.get('FLASK_MAIL_DEFAULT_SENDER_NAME', 'Flask Techan Unchained'),
        os.environ.get('FLASK_MAIL_DEFAULT_SENDER_EMAIL',
                       f"noreply@{os.environ.get('FLASK_DOMAIN', 'localhost')}")
    )

    ##########################################################################
    # session/cookies                                                        #
    ##########################################################################
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(
        host=os.getenv('FLASK_REDIS_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_REDIS_PORT', 6379)),
    )
    SESSION_PROTECTION = 'strong'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    # SECURITY_TOKEN_MAX_AGE is fixed from time of token generation;
    # it does not update on refresh like a session timeout would. for that,
    # we set (the ironically named) PERMANENT_SESSION_LIFETIME
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    ##########################################################################
    # security                                                               #
    ##########################################################################
    FLASH_MESSAGES = False
    SECURITY_PASSWORD_SALT = 'security-password-salt'
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True

    SECURITY_FORGOT_PASSWORD_ENDPOINT = 'frontend.forgot_password'
    SECURITY_API_RESET_PASSWORD_HTTP_GET_REDIRECT = 'frontend.reset_password'
    SECURITY_INVALID_RESET_TOKEN_REDIRECT = LocalProxy(
        lambda: url_for('frontend.forgot_password', _external=True) + '?invalid')
    SECURITY_EXPIRED_RESET_TOKEN_REDIRECT = LocalProxy(
        lambda: url_for('frontend.forgot_password', _external=True) + '?expired')
    SECURITY_POST_CONFIRM_REDIRECT_ENDPOINT = LocalProxy(
        lambda: url_for('frontend.index', _external=True) + '?welcome')
    SECURITY_CONFIRM_ERROR_REDIRECT_ENDPOINT = LocalProxy(
        lambda: url_for('frontend.resend_confirmation_email', _external=True))

    ##########################################################################
    # database                                                               #
    ##########################################################################
    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{pw}@{host}:{port}/{db}'.format(
        engine=os.getenv('FLASK_DATABASE_ENGINE', 'postgresql+psycopg2'),
        user=os.getenv('FLASK_DATABASE_USER', 'techan_unchained'),
        pw=os.getenv('FLASK_DATABASE_PASSWORD', 'techan_unchained'),
        host=os.getenv('FLASK_DATABASE_HOST', '127.0.0.1'),
        port=os.getenv('FLASK_DATABASE_PORT', 5432),
        db=os.getenv('FLASK_DATABASE_NAME', 'techan_unchained'))

    MARKETSTORE_RPC_HOST = os.getenv('MARKETSTORE_RPC_HOST', 'localhost')
    MARKETSTORE_RPC_PORT = os.getenv('MARKETSTORE_RPC_PORT', '5993')
    MARKETSTORE_RPC_PATH = os.getenv('MARKETSTORE_RPC_PATH', '/rpc')


class DevConfig(Config):
    DEBUG = get_boolean_env('FLASK_DEBUG', True)
    # EXPLAIN_TEMPLATE_LOADING = True
    # SQLALCHEMY_ECHO = True

    EXTERNAL_SERVER_NAME = 'http://localhost:8888'

    SESSION_COOKIE_SECURE = False

    ##########################################################################
    # mail                                                                   #
    ##########################################################################
    MAIL_PORT = 1025  # MailHog
    MAIL_DEFAULT_SENDER = ('Flask Techan Unchained', 'noreply@localhost')

    ##########################################################################
    # security                                                               #
    ##########################################################################
    SECURITY_CONFIRM_EMAIL_WITHIN = '1 minutes'  # for testing


class ProdConfig(Config):
    pass


class StagingConfig(ProdConfig):
    pass


class TestConfig(Config):
    TESTING = True

    SERVER_NAME = 'localhost:5000'

    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{pw}@{host}:{port}/{db}'.format(
        engine=os.getenv('FLASK_DATABASE_ENGINE', 'postgresql+psycopg2'),
        user=os.getenv('FLASK_DATABASE_USER', 'flask_test'),
        pw=os.getenv('FLASK_DATABASE_PASSWORD', 'flask_test'),
        host=os.getenv('FLASK_DATABASE_HOST', '127.0.0.1'),
        port=os.getenv('FLASK_DATABASE_PORT', 5432),
        db=os.getenv('FLASK_DATABASE_NAME', 'flask_test'))
