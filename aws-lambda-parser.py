import json
import boto3

lambda_list = []
client = boto3.client('lambda')


def next_page(marker):
    return client.list_functions(Marker=marker)


def parse_page(page):
    num = len(page['Functions'])
    for n in range(num):
        if page['Functions'][n]['Runtime'] == "python2.7":
            arn = page['Functions'][n]['FunctionArn']
            owner_tag = test_owner_tag(client.list_tags(Resource=arn))
            line = page['Functions'][n]['FunctionName'] + ' Description: ' + page['Functions'][n][
                'Description'] + " LastModified: " + page['Functions'][n]['LastModified'] + " Owner: " + owner_tag
            lambda_list.append(line)


def test_marker(result):
    try:
        return result["NextMarker"]
    except Exception:
        return ''


def test_owner_tag(result):
    try:
        return result['Tags']['tr:resource-owner']
    except Exception:
        return ''


def lambda_handler(event, context):
    result = client.list_functions()
    marker = test_marker(result)
    parse_page(result)

    while marker:
        page = next_page(marker)
        marker = test_marker(result)
        parse_page(page)

    return lambda_list
