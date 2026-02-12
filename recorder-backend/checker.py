import custom_fleep
import json
from urllib.parse import unquote_plus
from common import s3_client, logger, rreplace

audio_prefix = "uploads/audio_and_metadata/"
metadata_prefix = "uploads/audio_and_metadata/metadata/"


def check_audio_file(event, context):
    """Checks the validity of audio files uploaded to the S3 bucket and deletes invalid files along with their associated metadata.

    Args:
        event: The event data passed to the Lambda function, containing S3 object information.
        context: The context in which the Lambda function is executed.

    Returns:
        None. The function performs its operations directly on the S3 bucket.
    """
    event_str = json.dumps(event)
    logger.info(f"Event received ${event_str}")

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        logger.info(f"Analyzing {key}")

        try:
            res = s3_client.get_object(Bucket=bucket, Key=key)
        except Exception:
            logger.error(f"Couldn't read file from s3 with key {key}")
            continue

        content_length = res.get("ContentLength")

        if key.endswith(".json"):
            if content_length > 100000:
                logger.warning(f"Too large json file {key}")
                s3_client.delete_object(Bucket=bucket, Key=key)
            continue

        if content_length < 10000 or content_length > 500000000:
            logger.warning(f"Invalid size file {key} with size {content_length}")
            delete_audio_and_metadata(key, bucket)
            continue

        body = res.get("Body")
        if body is None:
            continue

        try:
            (valid, info) = is_valid_audio_file(body.read(128))
            if valid:
                logger.info(f"Valid audio {info.mime} file: {key}")
            else:
                logger.warning(f"NOT_VALID: file {key} is not a valid audio file")
                delete_audio_and_metadata(key, bucket)

        except Exception as e:
            logger.error(f"Error determining file type {e}")
        finally:
            body.close()


def is_valid_audio_file(body_start: bytes) -> tuple[bool, custom_fleep.Info]:
    info = custom_fleep.get(body_start)
    return (info.type_matches("audio"), info)


def delete_audio_and_metadata(key: str, bucket: str) -> None:
    """Deletes the audio file and its associated metadata file from the S3 bucket.

    Args:
        key: The key of the audio file in the S3 bucket to be deleted.
        bucket: The name of the S3 bucket.
    Returns:
        None.
    """
    try:
        s3_client.delete_object(Bucket=bucket, Key=key)

        (_, suffix) = key.rsplit(".", 1)

        meta_key = rreplace(
            key.replace(audio_prefix, metadata_prefix), suffix, "json", 1
        )

        s3_client.delete_object(Bucket=bucket, Key=meta_key)

    except Exception as e:
        logger.error(f"Error deleting files {e}")
