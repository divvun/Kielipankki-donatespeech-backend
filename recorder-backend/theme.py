import json
import logging
import boto3
import os
from botocore.exceptions import ClientError
from json import JSONDecodeError
from yle_utils import *
from common import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

theme_langs = ["fi", "en", "sv"]

def load_theme(event, context):
    try:
        theme_id = event.get('pathParameters').get('id')
        if theme_id in theme_langs:
            logger.info("calling load_all_themes from load_theme")
            return load_all_themes(event, context, lambda x: 'title' in x.keys() and theme_id in x['title'].keys())
        else:
            theme_dict = load_s3_file_content('theme/' + theme_id + '.json')
        logger.info("returning regular response from load_theme " + theme_id)
        return {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            "body": json.dumps(theme_dict)
        }
    except Exception as e:
        logger.error(e)
        raise FileProcessingError("Error reading theme")


# keep the standard indices below 10000, anything else will be assigned a bigger index
# note that these are not the "configuration" IDs, but rather the original "theme" IDs.
theme_sort_index = {
    '56311f9b-8fed-42e9-84d9-9cb1f53f1073': 1000, # Eläinystävät
    'ed04026a-8860-4760-bcb7-66915f29111a': 2000, # Urheilu
    'e5e2e982-d016-49bf-a36a-1e4f73cbbc6b': 3000, # K-18
    '7c3a4ab5-bbcc-450f-b2d0-285499c6048d': 4000, # Luonto, sää ja mää
    'f5da01f4-7044-4f30-99e6-9aa6be201028': 5000, # Lähellä
    'b93513ac-3385-4b92-a238-8406f644916b': 6000, # Kirottu korona
    'ec596c45-6304-4a67-8368-aafbbf1764ed': 6400, # Mediataidot 4-6 lk.
    '55d0dd12-7233-4be6-92a3-a7dc687871b1': 6800, # Mediataidot 8-9 lk.
    '2252a752-e06f-4c73-83cc-ff6d4f07cffd': 7000, # Mediataidot lukio
    '020fbda7-987b-48bb-aaa3-74b4b611e713': 1100, # Svenskan i Finland
    'f81ae5b8-8693-4e13-a142-2687cccb79dc': 1110, # Djur och Natur
    '5ebe74b0-7c80-4a12-863a-7140b486549e': 1120, # Mediekunskap 4-6
    '5ecd09a7-6ff9-48e9-a4cf-b5d1b3083413': 1130, # Mitt studieliv
    'bcb868b8-1780-4534-b2c0-6d2f1d37fc4a': 1140, # Mediekunskap 7-9
    'b4d1c95d-2cdb-4b3d-910d-2178f3457fbb': 1150, # Idrottsögonblick
    '801731c5-e1d9-4733-8112-2a3ed0fd60d9': 1160, # Mediekunskap, andra stadiet
    '0228a3fa-38c2-44f5-96ba-1de07a1dcda9': 1170, # Relationer & Sex
}

def sort_themes(theme_list):
    theme_dict = {}
    next_free_sort_index = 10000
    for theme in theme_list:
        theme_id = theme['id']
        if theme_id in theme_sort_index.keys():  # we have a sort index for this theme
            # put it in the dictionary with the sort index as key
            sort_index = theme_sort_index[theme_id]
            theme_dict[sort_index] = theme
        else: # no sort index found, assign one
            theme_dict[next_free_sort_index] = theme
            next_free_sort_index += 1000
    theme_list = []
    sort_indices = sorted(theme_dict.keys())
    for index in sort_indices:
        theme_list.append(theme_dict[index])
    return theme_list

def load_all_themes(event, context, theme_filter = None):
    try:
        list_of_theme_files = s3_client.list_objects_v2(
            Bucket=content_bucket, 
            Prefix=f'theme/',
            MaxKeys=1000
        )

        def map_theme_list(content):
            key = content.get('Key')
            filename = key.replace('theme/','')
            
            # Filter the parent "directory"
            if filename == '':
                 return None

            return {
                "id": filename.replace('.json', '').strip(),
                "content": load_s3_file_content(key)
            }

        if theme_filter == None:
            # By default, only Finnish
            theme_filter = lambda x: isinstance(x, dict) and 'title' in x.keys() and "fi" in x['title'].keys()
        def mapped_filter(mapped_theme):
            return theme_filter(mapped_theme["content"])

        themes = list(filter(lambda x: x is not None, map(map_theme_list, list_of_theme_files.get('Contents'))))
        mapped_contents = list(filter(mapped_filter, themes))
        # mapped_contents = list(filter(lambda x: x is not None, map(map_theme_list, list_of_theme_files.get('Contents'))))
        sorted_themes = sort_themes(mapped_contents)
        
        return {
                "statusCode": 200,
                "headers": {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True
                },
                "body": json.dumps(sorted_themes)
            }
    except Exception as e:
        logger.error(e)
        raise FileProcessingError("Error reading configuration")

