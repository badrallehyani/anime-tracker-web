import os, json

from tracker import Tracker
from aria2_helpers.torrent_download_manager import create_download_manager

conf_file_name = os.path.join( os.path.dirname(__file__), 'conf.json' )
data_file_name = os.path.join( os.path.dirname(__file__), 'data.json' )
recent_file_name = os.path.join( os.path.dirname(__file__), 'recent.json' )


conf = json.load(open(conf_file_name, 'r'))
sleep_between_animes = int(conf.get('sleep_between_animes'))
sleep_between_updates = int(conf.get('sleep_between_updates'))
react_server_url = conf.get('react_server_url')

downloader = create_download_manager(conf.get('aria2_xmlrpc_server_url'))
def send_to_downloader(torrent_urls, path):
    downloader.create_new_multiple_downloads(torrent_urls, path, paused = False)


tracker = Tracker(
        data_file_name,
        recent_file_name,
        send_to_downloader,
        sleep_between_animes = sleep_between_animes,
        sleep_between_updates = sleep_between_updates
    )



from flask import Flask, request
from flask_cors import CORS, cross_origin

from flask_routes import create_main_routes_bp
flask_app = Flask(__name__)

main_routes_bp = create_main_routes_bp(tracker)
flask_app.register_blueprint(main_routes_bp)

CORS(flask_app, origins =[
    react_server_url
])


if __name__ == '__main__':
    flask_app.run()
