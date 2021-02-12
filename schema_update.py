import json
import csv
import os

# Load the crosswalk.csv and make it a ditionary
# key-value pairs in the dictionary refers to the old-new schemas
crosswalk = {}
with open('crosswalk.csv') as f:
    reader = csv.reader(f)
    fields = next(reader)
    for record in reader:
        old = record[0]
        new = record[1]
        crosswalk[old] = new


# Function to update the metadata schema
def schema_update(filepath):
    # Open the JSON file with schema GBL 1.0
    with open(filepath) as fr:
        # Load its content and make a new dictionary
        data = json.load(fr)

        # Loop over crosswalk to change dictionary keys
        for old_schema, new_schema in crosswalk.items():
            if old_schema in data:
                data[new_schema] = data.pop(old_schema)

    # Overwrite JSON with the modified schema
    with open(filepath, 'w') as fw:
        j = json.dumps(data, indent=2)
        fw.write(j)

# Collect all JSON files in a list
# Iterate the list to update metadata schema
files = [x for x in os.listdir('test_jsons') if x.endswith('.json')]
for file in files:
    print(f'Executing {file} ...')
    filepath = 'solr_documents/' + file
    schema_update(filepath)