import json
import boto3

list = []
client = boto3.client('lambda')


def next_page(marker):
    client = boto3.client('lambda')
    return client.list_functions(Marker=marker)


def parse_page(page):
    num = len(page['Functions'])
    for n in range(num):
        if page['Functions'][n]['Runtime'] == "python2.7":
            arn = page['Functions'][n]['FunctionArn']
            tags = client.list_tags(Resource=arn)
            try:
                tag = tags['Tags']['tr:resource-owner']
            except:
                tag = ''
            line = page['Functions'][n]['FunctionName'] + ' Description: ' + page['Functions'][n][
                'Description'] + " LastModified: " + page['Functions'][n]['LastModified'] + " Owner: " + tag
            list.append(line)
            # print(str)


def lambda_handler(event, context):
    result = client.list_functions()
    num = len(result['Functions'])
    try:
        marker = result["NextMarker"]
    except:
        marker = ''
    parse_page(result)

    while marker:
        page = next_page(marker)
        try:
            marker = page["NextMarker"]
        except:
            marker = ''
        parse_page(page)

    return (list)
