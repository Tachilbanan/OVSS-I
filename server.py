from videoonline import Create_App

app = Create_App()

if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)
