import logging
from flask import Flask

app = Flask(__name__)


def setup_application():
    app.secret_key = 'super secret key'
    with app.app_context():
        # Enables routes in 'application.py'
        from e2tg import webapp

    log = logging.getLogger(__name__)
    log.debug(logging.getLevelName(log.getEffectiveLevel()) + ' log level activated')


if __name__ == '__main__':
    # Used only when starting this script directly, i.e. for debugging
    setup_application()
    app.run(debug=True)
else:
    setup_application()