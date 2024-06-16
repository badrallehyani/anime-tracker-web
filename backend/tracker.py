import os, json, time

import logging
log_file_name = os.path.join( os.path.dirname(__file__), 'log.log' )
logging.basicConfig(filename=log_file_name, format='%(asctime)s - %(message)s', level=logging.INFO)

from nyaasi import Nyaasi


class Tracker:
    def __init__(self,
                 data_file_name,
                 recent_file_name,
                 send_to_downloader,
                 sleep_between_animes = 15,
                 sleep_between_updates = 1800
        ):
        
        self.data_file_name = data_file_name
        self.recent_file_name = recent_file_name
        self.send_to_downloader = send_to_downloader
        self.sleep_between_animes = sleep_between_animes
        self.sleep_between_updates = sleep_between_updates

        self.last_update = -1


    def get_updates_info(self):
        return {
            'last_update': self.last_update,
            'next_update': self.next_update
        }

    def run_loop(self):
        while True:
            self.check_and_download()
            
            self.last_update = int(time.time())
            self.next_update = int(self.last_update + self.sleep_between_updates)
            
            time.sleep(self.sleep_between_updates)

    # RECENT.JSON

    def add_to_recent(self, files):
        recent = self.get_recent()
        files = [
            {
                'ID': file.get('ID'),
                'name': file.get('name'),
                'timestamp': int(time.time())
            }
            for file in files
        ]
        
        recent += files
        self.update_recent(recent)

        return recent

    def get_recent(self):
        return json.load(open(self.recent_file_name, 'r')).get('recent')
    
    def update_recent(self, files_list):
        data = {'recent': files_list}
        open(self.recent_file_name, 'w').write(json.dumps(data))
        return True

    def clear_recent(self):
        data = {'recent': []}
        open(self.recent_file_name, 'w').write(json.dumps(data))
        return {'status': 'ok'}

    # DATA.JSON

    def add_anime(self, name, keyword, submitter, path) -> dict:
        # returns the new data
        
        data = self.get_data()
        
        new_anime_list = data.get("anime_list")
        new_anime_list.append({
            "name": name,
            "keyword": keyword,
            "submitter": submitter,
            "done": [],
            "path": path
        })

        data.update({"anime_list": new_anime_list})
        self.update_data(data)

        return data

    def remove_anime(self, name):
        data = self.get_data()
        
        new_anime_list = [i for i in data.get('anime_list') if i.get('name') != name]
        
        data.update({"anime_list": new_anime_list})
        self.update_data(data)

        return data

    def get_data(self):
        return json.load(open(self.data_file_name, 'r'))
    
    def update_data(self, data):
        open(self.data_file_name, 'w').write(json.dumps(data))
        

    def check_and_download(self):
        # returns a list of newly added files
        data = self.get_data()
        anime_list = data.get("anime_list")
        data_has_changed = False
        newly_added = []
        
        for anime in anime_list:
            name = anime.get("name")
            keyword = anime.get("keyword")
            submitter = anime.get("submitter")
            done = anime.get("done")
            path = anime.get("path")

            search_result = Nyaasi.searchByUser(keyword, submitter)
            missing = [ i for i in search_result if i.get('URL') not in done ]
            missing_urls = [i.get('URL') for i in missing]
            missing_torrent_urls = [i.get('links').get('torrent_file') for i in missing]

            if missing:
                newly_added += missing
                data_has_changed = True
                
                self.send_to_downloader(missing_torrent_urls, path)
                self.add_to_recent(missing)
                
                anime.update({"done": done + missing_urls})

            time.sleep(self.sleep_between_animes)

        if data_has_changed:
            self.update_data(data)

        return newly_added
