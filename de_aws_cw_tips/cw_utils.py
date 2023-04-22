from boto3 import client
import time
import logging
import json
from de_aws_cw_tips.custom_formatter_logger import CustomFormatter
from sys import exit, stdout


def get_logger(logger: logging.Logger = None) -> logging.Logger:
    if logger is None:
        handler = logging.StreamHandler(stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(CustomFormatter())

        logger = logging.getLogger(__name__)

        if logger.hasHandlers():
            logger.removeHandler(handler)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger


def log_group_exists(cw_client: client, log_group_name: str) -> bool:
    # Check if the log group exists
    response = cw_client.describe_log_groups(logGroupNamePrefix=log_group_name)

    for log_group in response["logGroups"]:
        if log_group["logGroupName"] == log_group_name:
            # Log group exists
            return True

    # Log group doesn't exist
    return False


def create_log_group_if_not_exists(cw_client: client, log_group_name: str) -> None:
    # Check if the log group already exists
    if log_group_exists(cw_client, log_group_name):
        return

    # Create the log group
    cw_client.create_log_group(logGroupName=log_group_name)

    return None


def log_stream_exists(
    cw_client: client, log_group_name: str, log_stream_name: str
) -> bool:
    # Check if the log stream exists
    response = cw_client.describe_log_streams(
        logGroupName=log_group_name, logStreamNamePrefix=log_stream_name
    )

    for log_stream in response["logStreams"]:
        if log_stream["logStreamName"] == log_stream_name:
            # Log stream exists
            return True

    # Log stream doesn't exist
    return False


def create_log_stream_if_not_exists(
    cw_client: client, log_group_name: str, log_stream_name: str
) -> None:
    # Check if the log stream already exists
    if log_stream_exists(cw_client, log_group_name, log_stream_name):
        return

    # Create the log stream
    cw_client.create_log_stream(
        logGroupName=log_group_name, logStreamName=log_stream_name
    )

    return None


def put_log_event(
    cw_client: client,
    log_group_name: str,
    log_stream_name: str,
    log_message: str,
    int_timestamp: int = None,
    check_log_group_exists_and_create: bool = False,
    check_log_stream_exists_and_create: bool = False,
) -> None:
    if check_log_group_exists_and_create == True:
        create_log_group_if_not_exists(cw_client, log_group_name)

    if check_log_stream_exists_and_create == True:
        create_log_stream_if_not_exists(cw_client, log_group_name, log_stream_name)

    if int_timestamp is None:
        int_timestamp = int(round(time.time() * 1000))

    # Put the log event in the log stream
    cw_client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{"timestamp": int_timestamp, "message": log_message}],
        sequenceToken="string",
    )

    return None


def put_log_event_analytics_v1(
    cw_client: client,
    log_group_name: str,
    log_stream_name: str,
    dict_obj_log: dict,
    int_timestamp: int = None,
    check_log_group_exists_and_create: bool = False,
    check_log_stream_exists_and_create: bool = False,
    logger=None,
) -> None:
    logger = logging.getLogger()
    if "partition_value" not in dict_obj_log or (
        "company" not in dict_obj_log["partition_value"]
        or "service" not in dict_obj_log["partition_value"]
        or "task" not in dict_obj_log["partition_value"]
        or "subtask" not in dict_obj_log["partition_value"]
        or "version" not in dict_obj_log["partition_value"]
        or "date_logical" not in dict_obj_log["partition_value"]
    ):
        logger.error(
            """
            Error partition_value in dict_obj_log is mandatory and 
            (company, service, task, subtask, version, date_logical) is mandatory in dict_obj_log['partition_value']
            """
        )
        exit(3)

    if (
        "category" not in dict_obj_log
        or "level" not in dict_obj_log
        or "message" not in dict_obj_log
    ):
        logger.error(
            """
            Error (category, level, message) is mandatory in in dict_obj_log
            """
        )
        exit(3)

    json_message = json.dumps(dict_obj_log)
    logger.debug(json_message)

    put_log_event(
        cw_client,
        log_group_name,
        log_stream_name,
        json_message,
        int_timestamp,
        check_log_group_exists_and_create,
        check_log_stream_exists_and_create,
    )

    return None
