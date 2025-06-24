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


import re

import re


def custom_title(s):
    """
    Capitalizes the first letter of each word in a string, while preserving acronyms and
    handling words within parentheses correctly.

    Args:
        s (str): The string to be formatted.

    Returns:
        str: The string with corrected capitalization.
    """
    # Regex to find words, including those with special characters like ' and numbers.
    words = re.findall(r"[\w']+|\S", s)
    result = []

    # Flag to check if we are inside a parenthesis
    in_paren = False

    for word in words:
        if word == "(":
            in_paren = True
            result.append(word)
            continue
        elif word == ")":
            in_paren = False
            result.append(word)
            continue

        # Check if the word is an acronym (all caps) and not a single letter
        if word.isupper() and len(word) > 1:
            result.append(word)
        elif in_paren or (not result or result[-1] not in ["(", "["]):
            result.append(word.title())
        else:
            result.append(word.lower())

    # Rejoin the words, handling the spacing correctly.
    final_string = ""
    for i, part in enumerate(result):
        # Handle cases where no space is needed before the word
        if i == 0:
            final_string += part
        elif part in [",", ".", ")", "!", "?", "]", "'s"]:
            final_string += part
        # Handle cases where a space is needed
        elif result[i - 1] in ["(", "["]:
            final_string += part
        else:
            final_string += " " + part

    # Clean up any extra spaces at the beginning
    final_string = final_string.strip()

    # Fix the issue with spaces after a comma
    final_string = re.sub(r'(\w+)\s,', r'\1,', final_string)

    return final_string

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
