from videoonline import Create_App

app = Create_App('videoonline.config.DevConfig')

if __name__ == '__main__':
    app.debug = True
    app.run(port=3000, threaded=True)
