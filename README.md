import_advancedTable.py script contains code to import items from dynamo db table into json file named data_export_UsersTable.json

export_users_table.py script contains code to export table items from json file to another table of dynamo db database

The whole purpose of this project is to manage schema changes without having any downtime, the goal is to copy old data from existing table to new one with latest schema changes