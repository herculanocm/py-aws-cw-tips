import sys

sys.path.insert(0, f"../de_aws_cw_tips/")
from de_aws_cw_tips import cw_utils
import pytest
from boto3 import client as aws_client


@pytest.fixture(scope="session")
def cw_client():
    aws_access_key_id = ""
    aws_secret_access_key = ""
    aws_session_token = ""

    cw_client = aws_client(
        "logs",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name="sa-east-1",
    )
    yield cw_client


def test_put_log_event_analytics_v1(cw_client):
    dict_obj_log = {
        "partition_value": {
            "company": "captalys",
            "service": "glue",
            "task": "job1",
            "subtask": "job1",
            "version": "v1",
            "date_logical": "2023-05-19",
        },
        "category": "TESTE",
        "level": "INFO",
        'json_value': {'tableName': 'credit', 'qtdRowsDataset': 5688455},
        "message": "TESTE10",
    }

    logGroupName='/aws/poligono/lake/analytics/v1/json/glue/jobs'
    logStreamName='datalake-csv-vivo/20230418102735999999/20230418102735999998'

    assert cw_utils.put_log_event_analytics_v1(cw_client, logGroupName, logStreamName, dict_obj_log) == None


