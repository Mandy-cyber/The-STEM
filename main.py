from distutils.log import debug
from website import create_app

app = create_app()

if __name__ == '__main__':
    # TODO turn this to False before submit
    app.run(debug=True)