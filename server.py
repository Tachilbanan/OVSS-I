from videoonline import create_app

app = create_app('videoonline.config.DevConfig')

if __name__ == '__main__':
    app.debug = True
    app.run(port=3000, threaded=True)
