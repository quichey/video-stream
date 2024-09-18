import json
import boto3

def lambda_handler(event, context):
    print("event \n")
    print(event)
    print("context \n")
    print(context)

    # Create a DynamoDB resource
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    
    # Access a table
    table = dynamodb.Table('comments')
    
    # Perform operations on the table
    print("dir(table)")
    print(dir(table))
    response = table.get_item(Key={'id': '0'})
    item = response.get('Item')
    print("\nitem")
    print(item)
    if "next_page_key" in event.keys():
        exclusive_start_key = {
            "id": event["next_page_key"] 
        }
        response_scan = table.scan(
            Limit=event["limit"],
            ExclusiveStartKey=exclusive_start_key
        )
    else:
        response_scan = table.scan(
            Limit=event["limit"]
        )
    item_scan = response_scan.get('Items')
    print("\nitem_scan")
    print(item_scan)
    #LastEvaluatedKey 
    #ExclusiveStartKey 
    
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')

    response_iterator = paginator.paginate(
        TableName='comments',
        Select='ALL_ATTRIBUTES',
        PaginationConfig={
            'MaxItems': 30,
            'PageSize': 30,
            'StartingToken': 'string'
        }
    )
    print(vars(response_iterator))

    """
    for page in response_iterator:
        #print(page)
        print('test')

    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(f"Hello from Lambda! {item}\n pages: {response_iterator.get("Items")}")
    }
    """
    body = {
        "items": item_scan,
        "last_evaluated_key": response_scan.get('LastEvaluatedKey')
    }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
