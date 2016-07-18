import sys

import bangumi
import database
import dmhy
import downloader

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
            #   Wrong arguments
            else:
                raise RuntimeError('Unexcepted arguments: {0}'.format(args))

        for action in action_queue:
            action[0](*action[1], **action[2])
    # Main procedure
    else:
        print('Fetching new episodes infomation')
        unload = database.unloaded_episodes()
        print('Download start\n')
        for unload_episode in unload:
            print('Ep.{0} of {1} is processing'.format(unload_episode.ep,
                                                       unload_episode.name))
            unload_episode.url = dmhy.get_download_url(unload_episode)
            downloader.download(unload_episode)
            database.set_downloaded_episode(unload_episode.name,
                                            unload_episode.ep)
