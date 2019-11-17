from app import APP

from app.models.server import Server


@APP.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    APP.run()

