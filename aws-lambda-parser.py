import json
import boto3

client = boto3.client('lambda')

lambda_list = []
runtime = "python2.7"
owner_tag_name = 'tr:resource-owner'
func = 'Functions'
desc = "Description"
last = "LastModified"


def next_page(marker):
    return client.list_functions(Marker=marker)


def parse_page(page):
    num = len(page['Functions'])
    for n in range(num):
        if page[func][n]['Runtime'] == runtime:
            arn = page[func][n]['FunctionArn']
            owner_tag = test_owner_tag(client.list_tags(Resource=arn))
            line = page[func][n]['FunctionName'] + ' ' + desc + ': ' + page[func][n][desc] + ' ' + last + ': ' + \
                   page[func][n][last] + " Owner: " + owner_tag
            lambda_list.append(line)


def test_marker(result):
    try:
        return result["NextMarker"]
    except Exception:
        return ''


def test_owner_tag(result):
    try:
        return result['Tags'][owner_tag_name]
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
