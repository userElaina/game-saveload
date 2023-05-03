import os
import json


config = {
    'ds1': {
        'path': '~\\Documents\\NBGI'
    },
    'code': {
        'path': './啊.txt'
    }
}

for i in config:
    config[i]['path'] = os.path.abspath(os.path.expanduser(config[i]['path']))

s = json.dumps(config, indent=4, ensure_ascii= False)

open('config.json', 'wb').write(s.encode('utf8'))

