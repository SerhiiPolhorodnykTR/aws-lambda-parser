import json
import boto3

list = []


def next_page(marker):
    client = boto3.client('lambda')
    return client.list_functions(Marker=marker)


def parse_page(page):
    num = len(page['Functions'])
    for n in range(num):
        if page['Functions'][n]['Runtime'] == "python2.7":
            line = str(n) + ' ' + page['Functions'][n]['FunctionName'] + ' Runtime: ' + page['Functions'][n][
                'Runtime'] + ' Description: ' + page['Functions'][n]['Description'] + " LastModified: " + \
                   page['Functions'][n]['LastModified'] + " Used Role: " + page['Functions'][n]['Role']
            list.append(line)
            # print(str)


def lambda_handler(event, context):
    client = boto3.client('lambda')
    result = client.list_functions()
    num = len(result['Functions'])
    marker = result["NextMarker"]
    parse_page(result)

    while marker:
        page = next_page(marker)
        try:
            marker = page["NextMarker"]
        except:
            marker = ''
        parse_page(page)

    return (list)