#!/usr/local/bin/python3
__author__ = 'Louis Volant'
__version__= 1.0

import logging, os
import eyed3


# README
# execute with
# python3 -m venv myenv
# source myenv/bin/activate
# pip install -r requirements.txt
# python3 youtube2mp3.py 'https://www.youtube.com/watch?v=YOUTUBE_ID' 


def cleanFilePath(inputFilePath, cleaned_filepath):

    file_path = inputFilePath.replace('.Mp3', '.mp3')
    cleanedFilePath = cleaned_filepath + ".mp3"

    if(file_path != cleanedFilePath):
        logging.info('FILENAME TO rename:{0}/To:{1}'
                 .format(file_path,cleanedFilePath))
        os.rename(file_path, cleanedFilePath)
    else:
        logging.info('FILENAME NOT DIFFERENT:{0}/To:{1}'
                 .format(file_path,cleanedFilePath))
    return cleanedFilePath


def custom_title(s):
    words = s.split()
    capitalized_words = []

    for word in words:
        if len(word) > 0:
            #logging.info('Word to process: {0}'.format(word))
            first_letter = word[0].upper()
            rest_of_word = word[1:].lower()
            capitalized_word = first_letter + rest_of_word
            capitalized_words.append(capitalized_word)
            #logging.info('Word processed: {0}'.format(capitalized_word))

    return ' '.join(capitalized_words)

def handleMp3File(inputFilePath):
    _cleanedFileName = inputFilePath.replace(".mp3", "")
    _fileNameParts = _cleanedFileName.split(' - ');
    for i in _fileNameParts:
        i = i.strip()

    _artist = custom_title(_fileNameParts[0])
    _fileNameParts.pop(0)
    _title = custom_title(' - '.join(_fileNameParts))
    _cleaned_filepath = ' - '.join([_artist, _title])

    cleaned_file_path = cleanFilePath(inputFilePath, _cleaned_filepath)

    mp3file = eyed3.load(cleaned_file_path)

    if mp3file is not None:
        _originalTitle = ''
        _originalArtist = ''
        if hasattr(mp3file, 'tag'):
            if hasattr(mp3file.tag, 'title'):
                _originalTitle = mp3file.tag.title
            if hasattr(mp3file.tag, 'artist'):
                _originalArtist = mp3file.tag.artist

        logging.info('TAGS:OriginalTitle:{0}/Title:{1}/OriginalArtist:{2}/Artist:{3}'
                    .format(_originalTitle,_title,_originalArtist,_artist))

        mp3file.initTag()
        mp3file.tag.save()

        mp3file.tag.artist = _artist
        mp3file.tag.title = _title

        mp3file.tag.save()
    else:
        logging.info('eyed3 couldn\'t load:{0}'.format(_cleanedFileName))



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
