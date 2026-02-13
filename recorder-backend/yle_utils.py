import os
import json
import base64
import logging
import urllib.request
from Crypto.Cipher import AES
from common import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CLIENT_ID = os.environ.get('YLE_CLIENT_ID')
CLIENT_KEY = os.environ.get('YLE_CLIENT_KEY')
YLE_DECRYPT = os.environ.get('YLE_DECRYPT')

PROGRAM_INFO_URL = "https://programs.api.yle.fi/v3/schema/v1/items/{program_id}?app_id={client_id}&app_key={client_key}"
MEDIA_URL = "https://media.api.yle.fi/v4/{media_id}/playouts.json?protocol=HLS&app_id={client_id}&app_key={client_key}"

def map_yle_content(yle_program_id):
    
    if yle_program_id is None:
        return

    try:
        media_url = get_media_url(yle_program_id)
        logger.info("Successfully decrypted YLE URL, url is " + str(media_url))
    except Exception as e:
        logger.error("Error decrypting yle URL: {}".format(e))
        raise FileProcessingError(e)

    try:
        req = urllib.request.Request(media_url)
        req.add_header('User-Agent', 'lahjoita-puhetta')
        with urllib.request.urlopen(req, timeout=10) as media_res:
            logger.info("Media response status is " + str(media_res.status))
            return json.loads(media_res.read()).get('data')[0].get('url')
    except Exception as e:
        logger.error("error from urllib, " + str(e))
        raise e

def decrypt_yle_url(crypted_url):
    base64_decoded_url = base64.b64decode(crypted_url)
    iv = base64_decoded_url[:16]
    msg = base64_decoded_url[16:]
    cipher = AES.new(YLE_DECRYPT, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(msg) 
    return decrypted.decode("utf-8").strip()

    
def get_media_url(yle_program_id):
    processed_program_info_url = PROGRAM_INFO_URL.format(
        program_id= yle_program_id,
        client_id=CLIENT_ID,
        client_key=CLIENT_KEY)

    with urllib.request.urlopen(processed_program_info_url,timeout=10) as res:
        program_res = json.loads(res.read())
        pub_events = program_res.get('data').get('publicationEvent')
        pub_event = next ((event for event in pub_events if event.get('temporalStatus') == 'currently'))

        media_id = pub_event.get('media').get('id')
        return MEDIA_URL.format(
            program_id= yle_program_id,
            media_id= media_id,
            client_id=CLIENT_ID,
            client_key=CLIENT_KEY
        )
