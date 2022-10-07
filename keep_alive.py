from flask import Flask
from threading import Thread

app = Flask('')

import sys
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

@app.route('/')
def main():
    return "Your bot is connected to Twitter"


def run():
    app.run(host="0.0.0.0", port=5000)


def keep_alive():
    server = Thread(target=run)
    server.start()
