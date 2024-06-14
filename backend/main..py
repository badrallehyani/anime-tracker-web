from threading import Thread
from app import flask_app, tracker


def run_flask():
    HOST = '10.0.0.2'
    PORT = '8080'
    flask_app.run(host = HOST, port = PORT, debug = False)

def run_tracker():
    tracker.run_loop()

flask_thread = Thread(target = run_flask)
tracker_thread = Thread(target = run_tracker)

flask_thread.start()
tracker_thread.start()

flask_thread.join()
tracker_thread.join()
