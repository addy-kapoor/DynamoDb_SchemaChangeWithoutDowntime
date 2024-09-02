import json
import boto3

# Specify the table name and AWS region
export_table_name = "UsersTable"
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(export_table_name)

def export_table_data():
    print(f"Exporting data from {export_table_name}")
    response = table.scan()
    data = response['Items']

    # Paginate through DynamoDB table response
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    # Create or open a text file to save exported data
    with open(f"data_export_{export_table_name}.json", "w+") as f:
        json_data = json.dumps(data, indent=4)  # Pretty print with indentation
        f.write(json_data)

    print("Export complete!")

# Call the function to export the data
export_table_data()
