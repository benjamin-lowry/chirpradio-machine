#!/usr/bin/env python

import codecs
import sys
from chirp.common.printing import cprint
from chirp.common.input import cinput
from chirp.library import artists
from chirp.library import dropbox



def main_generator(rewrite):
    drop = dropbox.Dropbox()
    new_artists = set()
    for au_file in drop.tracks():
        try:
            tpe1 = au_file.mutagen_id3["TPE1"].text[0]
        except:
            cprint('** file: %r' % au_file.path)
            raise

        if not rewrite:
            new_artists.add(tpe1)
        else:
            standardized_name = artists.standardize(tpe1)
            if not standardized_name:
                new_artists.add(tpe1)
            elif standardized_name != tpe1:
                bp_inpt = cinput(f"Correct {tpe1} to {standardized_name}?", ["Yes (default)","No"],allow_custom=False)
                if(bp_inpt != "No"): #Breakpoint passed
                    new_artists.add(tpe1)



    to_print = list(new_artists)
    if rewrite:
        to_print.extend(artists.all())
    to_print.sort(key=artists.sort_key)

    output = None
    if rewrite:
        output = codecs.open(artists._WHITELIST_FILE, "w", "utf-8")
    for tpe1 in to_print:
        if output:
            output.write(tpe1)
            output.write("\n")
        else:
            cprint(tpe1)
        yield

    if rewrite:
        cprint('Artist whitelist updated', type='success')
    else:
        cprint('Found %d new artists' % len(to_print), type='success')


def main():
    for _ in main_generator(rewrite="--rewrite" in sys.argv):
        pass


if __name__ == "__main__":
    main()
