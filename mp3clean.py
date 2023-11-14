#!/usr/local/bin/python3
__author__ = 'Louis Volant'
__version__= 1.0

import logging, json, os
import eyed3

# README
# execute with
# $ mp3clean % pip install os
# $ mp3clean % python3 mp3clean.py

def handleMp3File(inputFilePath):
    file_path = inputFilePath
    mp3file = eyed3.load(file_path)

    _originalTitle = mp3file.tag.title
    _originalArtist = mp3file.tag.artist

    _title = file_path.replace(".mp3", "").title()
    _artist = _title.split(' - ')[0].title()

    logging.info('OriginalTitle: {0} / Title: {1} / OriginalArtist : {2} / Artist: {3}'.format(_originalTitle,_title,_originalArtist,_artist))

    mp3file.initTag()
    mp3file.tag.save();

    mp3file.tag.artist = _artist
    mp3file.tag.title = _title

    mp3file.tag.save()


def main():
    dir_path = '.'
    for file_path in os.listdir(dir_path):
        logging.info('Processing: {0}'.format(file_path))
        if(file_path.endswith('.mp3')):
            handleMp3File(file_path)




if __name__ == '__main__':
    ## Initialize logging before hitting main, in case we need extra debuggability
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    main()
