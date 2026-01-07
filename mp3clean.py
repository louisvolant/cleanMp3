#!/usr/local/bin/python3
__author__ = 'Louis Volant'
__version__ = 1.1

import logging
import os
import re
import unicodedata
import eyed3


# README
# execute with
# python3 -m venv myenv
# source myenv/bin/activate
# pip install -r requirements.txt
# python3 youtube2mp3.py 'https://www.youtube.com/watch?v=YOUTUBE_ID'

def cleanFilePath(inputFilePath, cleaned_filepath):
    # Ensure extension is lowercase
    file_path = inputFilePath.replace('.Mp3', '.mp3')
    cleanedFilePath = cleaned_filepath + ".mp3"

    if file_path != cleanedFilePath:
        logging.info('FILENAME TO rename: {0} / To: {1}'
                     .format(file_path, cleanedFilePath))
        try:
            os.rename(file_path, cleanedFilePath)
        except OSError as e:
            logging.error('Error renaming file: {0}'.format(e))
    else:
        logging.info('FILENAME NOT DIFFERENT: {0} / To: {1}'
                     .format(file_path, cleanedFilePath))
    return cleanedFilePath


def custom_title(s):
    """
    Capitalizes the first letter of each word in a string, while preserving acronyms,
    handling words within parentheses correctly, and avoiding unwanted spaces around apostrophes.
    """
    if not s:
        return ""

    # Normalize unicode to NFC (joins base characters with their diacritics like 'ë')
    s = unicodedata.normalize('NFC', s)

    # Updated regex:
    # [\w'’]+ matches alphanumeric characters AND straight/curly apostrophes as one block.
    # \S matches any other non-whitespace character.
    words = re.findall(r"[\w'’]+|\S", s)
    result = []

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
            # .title() works fine on words containing apostrophes (e.g., "C’est" -> "C’Est")
            result.append(word.title())
        else:
            result.append(word.lower())

    # Rejoin the words, handling the spacing correctly.
    final_string = ""
    for i, part in enumerate(result):
        if i == 0:
            final_string += part
        # No space before these punctuation marks
        elif part in [",", ".", ")", "!", "?", "]", "'s"]:
            final_string += part
        # No space after opening brackets
        elif result[i - 1] in ["(", "["]:
            final_string += part
        else:
            final_string += " " + part

    # Final cleanup
    final_string = final_string.strip()
    # Fix the issue with spaces before a comma
    final_string = re.sub(r'\s+([,.!?])', r'\1', final_string)

    return final_string


def handleMp3File(inputFilePath):
    # Remove extension for processing
    _cleanedFileName = re.sub(r'\.mp3$', '', inputFilePath, flags=re.IGNORECASE)

    # Standardize different types of dashes
    _cleanedFileName = _cleanedFileName.replace(' – ', ' - ')  # en dash
    _cleanedFileName = _cleanedFileName.replace('—', ' - ')  # em dash
    _cleanedFileName = _cleanedFileName.replace('–', '-')  # simple en dash

    # Split Artist and Title
    _fileNameParts = _cleanedFileName.split(' - ')
    _fileNameParts = [p.strip() for p in _fileNameParts]

    _artist = custom_title(_fileNameParts[0])

    if len(_fileNameParts) > 1:
        _fileNameParts.pop(0)
        _title = custom_title(' - '.join(_fileNameParts))
    else:
        _title = "Unknown Title"

    _new_filename_base = ' - '.join([_artist, _title])
    cleaned_file_path = cleanFilePath(inputFilePath, _new_filename_base)

    # Update ID3 Tags
    try:
        mp3file = eyed3.load(cleaned_file_path)
        if mp3file is not None:
            _originalTitle = ""
            _originalArtist = ""

            if mp3file.tag:
                _originalTitle = mp3file.tag.title if mp3file.tag.title else ""
                _originalArtist = mp3file.tag.artist if mp3file.tag.artist else ""
            else:
                mp3file.initTag()

            logging.info('TAGS: OriginalTitle: {0} / Title: {1} / OriginalArtist: {2} / Artist: {3}'
                         .format(_originalTitle, _title, _originalArtist, _artist))

            mp3file.tag.artist = _artist
            mp3file.tag.title = _title
            mp3file.tag.save()
        else:
            logging.warning('eyed3 couldn\'t load: {0}'.format(cleaned_file_path))
    except Exception as e:
        logging.error('Error processing ID3 tags for {0}: {1}'.format(cleaned_file_path, e))


def main():
    dir_path = '.'
    for file_path in os.listdir(dir_path):
        # Check for .mp3 extension case-insensitively
        if file_path.lower().endswith('.mp3'):
            logging.info('Processing: {0}'.format(file_path))
            handleMp3File(file_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    main()