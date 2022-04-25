from flask import Flask
from coffeeCalc import app

if __name__ == '__main__':
    app.run(app.config['ip_address'],
            port = int(app.config['port']))