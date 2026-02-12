import json
import logging
from yle_utils import map_yle_content
from common import load_s3_file_content, FileProcessingError, s3_client, content_bucket

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pre_process_configuration_file(content: dict) -> None:
    """Pre-processes the configuration file content by mapping YLE content URLs to their decrypted media URLs.

    Args:
        content: The configuration file content as a dictionary to be pre-processed.

    Returns:
        None. The function modifies the input content dictionary in place.
    """
    for item in content.get("items", []):
        item_type = item.get("itemType")
        if item_type == "yle-video" or item_type == "yle-audio":
            url = item.get("url")
            item["url"] = map_yle_content(url)


def load_s3_conf_file(file: str) -> dict:
    """Loads a configuration file from the S3 bucket, pre-processes its content, and returns it as a dictionary.

    Args:
        file: The key of the configuration file in the S3 bucket to be loaded.

    Returns:
        The content of the configuration file as a dictionary after pre-processing.

    Raises:
        FileProcessingError: If there is an error during the loading or pre-processing of the configuration file.
    """
    conf_dict = load_s3_file_content(file)
    pre_process_configuration_file(conf_dict)
    return conf_dict


def load_configuration(event, context) -> dict:
    """Loads a specific configuration file from the S3 bucket based on the provided schedule ID and returns its content.

    Args:
        event: The event data passed to the Lambda function, containing the schedule ID in the path
        context: The context in which the Lambda function is executed.

    Returns:
        A dictionary containing the status code, headers, and body with the configuration content.

    Raises:
        FileProcessingError: If there is an error during the loading of the configuration file.
    """
    try:
        schedule_id = event.get("pathParameters").get("id")
        conf_name = "configuration/" + schedule_id + ".json"
        conf_dict = load_s3_conf_file(conf_name)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(conf_dict),
        }
    except Exception as e:
        logger.error(e)
        raise FileProcessingError(
            "Error reading configuration file: {}".format(conf_name)
        )


def load_all_configurations(event, context) -> dict:
    """Loads all configuration files from the S3 bucket and returns their content.

    Args:
        event: The event data passed to the Lambda function.
        context: The context in which the Lambda function is executed.

    Returns:
        A dictionary containing the status code, headers, and body with the list of all configuration contents.

    Raises:
        FileProcessingError: If there is an error during the loading of the configuration files.
    """
    try:
        list_of_conf_files = s3_client.list_objects_v2(
            Bucket=content_bucket, Prefix="configuration/", MaxKeys=1000
        )

        def map_conf_list(content):
            key = content.get("Key")
            filename = key.replace("configuration/", "")

            # Filter the parent "directory"
            if filename == "":
                return None

            return {
                "id": filename.replace(".json", "").strip(),
                "content": load_s3_conf_file(key),
            }

        mapped_contents = list(
            filter(
                lambda x: x is not None,
                map(map_conf_list, list_of_conf_files.get("Contents")),
            )
        )
        mapped_contents.sort(key=lambda x: x.get("id"))

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(mapped_contents),
        }
    except Exception as e:
        logger.error(e)
        raise FileProcessingError("Error reading configuration")
