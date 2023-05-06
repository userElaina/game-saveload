import os
import json
import shlex
import shelllikecui as slc

from util import autonext, save_tar, load_tar

DATADIR = 'data'
CONFIG = 'config.json'
DFT = '__DFT__'

datadir = os.path.abspath(DATADIR)
config = json.loads(open(CONFIG, 'rb').read().decode('utf8'))
config['__DFT__'] = {'path': __file__}

os.makedirs(datadir, exist_ok=True)

for i in config:
    os.makedirs(os.path.join(datadir, i), exist_ok=True)


def addgame(arg: str):
    arg = shlex.split(arg.strip())
    if len(arg < 3):
        print('Type Error: `addgame` need 3 args.')
        return
    config[arg[1]] = {
        'path': arg[2]
    }
    os.makedirs('data/%s' % arg[2], exist_ok=True)


def removegame(arg: str):
    arg = shlex.split(arg.strip())
    if len(arg < 2):
        print('Type Error: `removegame` need 2 args.')
        return
    del config[arg[1]]


class Status:
    def __init__(self) -> None:
        self.status(DFT)

    def status(self, game: str) -> None:
        if game not in config:
            print('Game Not Found: "%s"', game)
        self.game = game
        self.auto_latest = True
        self.dir = os.path.join(datadir, game)
        self.re(os.path.basename((['',] + sorted(os.listdir(self.dir)))[-1]))

    def re(self, name: str) -> int:
        if not self._exists(name):
            print('File Not Found: "%s"' % name)
            print('Latest: "%s"' % self.latest)
            print('Next:   "%s"' % self.next)
            return 1
        self.latest = name
        print('Latest: "%s"' % self.latest)
        self._update_next()
        print('Next:   "%s"' % self.next)
        return 0

    def save(self, name: str = '', force: bool = False) -> int:
        if not os.path.exists(config[self.game]['path']):
            print("Where is your game data?")
            return 1
        if not name:
            name = self.next

        print('.save:  "%s"' % name)
        if self._exists(name):
            print('File Already Exist: "%s"' % name)
            if force:
                print('ReWrite!')
            else:
                return 1

        save_tar(config[self.game]['path'], self._join(name))
        return self.re(name)

    def load(self, name: str = '') -> int:
        if not name:
            name = self.latest
        if not name:
            print('You have no archive!')
            return 1

        print('.load:  "%s"' % name)
        if not self._exists(name):
            print('File Not Exist: "%s"' % name)
            return 1
        load_tar(config[self.game]['path'], self._join(name))
        return self.re(name)

    def _update_next(self) -> str:
        self.next = autonext(self.latest, self.game)
        while self._exists(self.next):
            self.next = '%s.00.tar' % self.next[:-4]

    def _join(self, s: str) -> str:
        return os.path.join(self.dir, s)

    def _exists(self, s: str) -> str:
        return os.path.exists(self._join(s))


b = Status()


def gotogame(arg: str):
    arg = shlex.split(arg.strip())
    if len(arg) < 2:
        print('Type Error: `gotogame` need 2 args.')
        return
    b.status(arg[1])


def re(arg: str):
    arg = shlex.split(arg.strip())
    if len(arg) == 1:
        b.status(b.game)
    else:
        b.re(arg[1])


def save(arg: str):
    arg = shlex.split(arg.strip())
    if len(arg) == 1:
        b.save()
    elif len(arg) == 2:
        if arg[1] in ('-f', '--force'):
            b.save(force=True)
        else:
            b.save(arg[1])
    else:
        if arg[1] in ('-f', '--force'):
            b.save(arg[2], True)
        else:
            b.save(arg[1], arg[2] in ('-f', '--force'))


def load(arg: str):
    arg = shlex.split(arg.strip())
    if len(arg) == 1:
        b.load()
    else:
        b.load(arg[1])


a = slc.make_cui0()
a.ps1 = 'GameSL> '
a.register(slc.make_command('addgame', addgame))
a.register(slc.make_command('removegame', removegame))
a.register(slc.make_command('gotogame', gotogame))
a.register(slc.make_command('re', re))
a.register(slc.make_command('save', save, ['sv', 's']))
a.register(slc.make_command('load', load, ['ld', 'l']))
a.always_input()
