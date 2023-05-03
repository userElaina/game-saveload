import os
import shutil


def save_tar(gamedata: str, archive: str) -> None:
    print('.save_tar "%s" -> "%s"' % (gamedata, archive))
    assert archive.endswith('.tar')
    archive = archive[:-4]
    shutil.make_archive(archive, 'tar', gamedata)


def load_tar(gamedata: str, archive: str) -> None:
    print('.load_tar "%s" <- "%s"' % (gamedata, archive))
    assert archive.endswith('.tar')
    save_tar(gamedata, archive[:-4] + '.cache.tar')
    shutil.rmtree(gamedata)
    shutil.unpack_archive(archive, gamedata, 'tar')


def autonext(s: str, ex: str) -> str:
    if not s:
        return '%s.00.tar' % ex

    i = len(s) - 5
    while i >= 0:
        try:
            int(s[i])
            break
        except ValueError:
            i -= 1

    if i < 0:
        return '%s.00.tar' % s[:-4]

    r = i
    while i >= 0:
        try:
            int(s[i])
            i -= 1
        except ValueError:
            break

    l = r-i
    # print('select',s[i+1:r+1])
    return s[:i+1] + str(int(s[i+1:r+1]) + 1).zfill(l) + s[r+1:]
