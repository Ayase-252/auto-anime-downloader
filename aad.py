import sys
import json

import bangumi
import database
import dmhy
import downloader
import configure

if __name__ == '__main__':

    if len(sys.argv) != 1:
        args = sys.argv[1:]
        action_queue = []

        #   Parse arguments
        while args != []:
            #   Read bangumis from file
            if args[0] == 'add':
                file_path = args[1]
                bangumis = bangumi.read_bangumi_from_file(file_path)
                action_queue.append((database.add_bangumis, (bangumis,), {}))
                args = args[2:]
                continue
            elif args[0] == 'update':
                file_path = args[1]
                f = open(file_path, 'r', encoding='utf-8')
                parsed = json.loads(f.read(), encoding='utf-8')
                f.close()
                for anime in parsed:
                    database.update_anime_info(
                        anime['name'],
                        bangumi.parsed_json_to_dict(anime['new_info']))
                args = args[2:]
                continue
            #   Wrong arguments
            else:
                raise RuntimeError('Unexcepted arguments: {0}'.format(args))

        for action in action_queue:
            action[0](*action[1], **action[2])
    # Main procedure
    else:
        print('Fetching new episodes infomation')
        unload = database.fetch_available_episodes()
        if len(unload) == 0:
            print('No available anime at present.')
        else:
            print('Download start\n')
        for unload_episode in unload:
            print('Ep.{0} of {1} is processing'.format(unload_episode['ep'],
                                                       unload_episode['name']))
            try:
                unload_episode_url = dmhy.get_download_url(**unload_episode)
                downloader.download(url=unload_episode_url,
                                    save_path=configure.TORRENT_SAVE_PATH,
                                    **unload_episode)
                database.set_downloaded_episode(unload_episode['name'],
                                                unload_episode['ep'])
            except FileNotFoundError:
                print("Error: Torrent doesn't exist in the website.")
