#!/usr/local/bin/python3
__author__ = 'Louis Volant'
__version__= 1.0

import logging, json, os
import eyed3

def cleanFilePath(inputFilePath):
    file_path = inputFilePath
    cleanedFilePath = file_path.title().replace('.Mp3', '.mp3')
    if(file_path != cleanedFilePath):
        logging.info('Will rename:{0}/To:{1}'
                 .format(file_path,cleanedFilePath))
        os.rename(file_path, cleanedFilePath)
    else:
        logging.info('NOT DIFFERENT:{0}/To:{1}'
                 .format(file_path,cleanedFilePath))
    return cleanedFilePath

# README
# execute with
# $ mp3clean % pip install os
# $ mp3clean % python3 mp3clean.py

def handleMp3File(inputFilePath):
    file_path = cleanFilePath(inputFilePath)
    mp3file = eyed3.load(file_path)

    _originalTitle = mp3file.tag.title
    _originalArtist = mp3file.tag.artist

    _cleanedFileName = file_path.replace(".mp3", "").title()
    _fileNameParts = _cleanedFileName.split(' - ');
    for i in _fileNameParts:
        i = i.strip().title()

    _artist = _fileNameParts[0]
    _fileNameParts.pop(0)
    _title = ' - '.join(_fileNameParts)


    logging.info('OriginalTitle:{0}/Title:{1}/OriginalArtist:{2}/Artist:{3}'
                 .format(_originalTitle,_title,_originalArtist,_artist))

    mp3file.initTag()
    mp3file.tag.save();

    mp3file.tag.artist = _artist
    mp3file.tag.title = _title

    mp3file.tag.save()


def main():
    dir_path = '.'
    for file_path in os.listdir(dir_path):
        logging.info('Processing: {0}'.format(file_path))
        if(file_path.title().endswith('.Mp3')):
            handleMp3File(file_path)




if __name__ == '__main__':
    ## Initialize logging before hitting main, in case we need extra debuggability
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    main()
