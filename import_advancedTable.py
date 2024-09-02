import json
import boto3

# Specify your DynamoDB table names and the region
source_table_name = "UsersTable"
target_table_name = "AdvancedUsersTable"
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
target_table = dynamodb.Table(target_table_name)

def import_users_data():
    # Read the data from the JSON file
    data_to_import = read_data_from_json()
    
    # Import data to AdvancedUsersTable
    write_data_to_advanced_table(data_to_import)

def read_data_from_json():
    # Load data from the JSON file created earlier
    with open(f"data_export_{source_table_name}.json", "r") as file:
        contents = file.read()
        users_data = json.loads(contents)
        
    return users_data

def write_data_to_advanced_table(users_data):
    failed_records = []
    success_count = 0

    for user in users_data:
        try:
            # Create items to match the AdvancedUsersTable structure
            response = target_table.put_item(
                Item={
                    'PK': f"USER#{user['userId']}",
                    'SK': f"USER#{user['userId']}",
                    'userEmail': user['email'],
                    'userName': user['name'],
                    'GSI1PK': "USER",
                    'GSI1SK': int(user['userId']) 
                },
                ConditionExpression='attribute_not_exists(PK)'  # Ensure no duplicates
            )
            print(f"Successfully inserted user {user['userId']} into {target_table_name}. Response: {response['ResponseMetadata']['HTTPStatusCode']}")
            success_count += 1

        except Exception as e:
            print(f"Error inserting user {user['userId']}: {e}")
            failed_records.append(user)

    if failed_records:
        print(f"Failed records: {failed_records}")
    
    print(f"Successfully inserted {success_count} records into {target_table_name}.")
    print("Import process completed!")

# Run the import function
import_users_data()
