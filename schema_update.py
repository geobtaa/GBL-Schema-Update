import json
import csv
import os

# Manual changes before run
dir_crosswalk = 'crosswalk.csv'
dir_old_schema = 'solr_documents_1.0/'
dir_new_schema = 'solr_documents_updated/'

# Load the crosswalk.csv and make it a ditionary
# key-value pairs in the dictionary refers to the old-new schemas
crosswalk = {}
with open(dir_crosswalk) as f:
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

    # check for multi-val field
    # if so, convert its value to an array
    data = string2array(data)

    # Write updated JSON to a new folder
    filepath_updated = dir_new_schema + file
    with open(filepath_updated, 'w') as fw:
        j = json.dumps(data, indent=2)
        fw.write(j)

# Function to convert fields that ends with '_sm' to an array
def string2array(dict):
    for key in dict.keys():
        suffix = key.split('_')[-1]
        if suffix == 'sm' or suffix == 'im':
            val = dict[key]
            if type(val) != list:
                dict[key] = [val]
    return dict


# Collect all JSON files in a list
# Iterate the list to update metadata schema
files = [x for x in os.listdir(dir_old_schema) if x.endswith('.json')]
for file in files:
    print(f'Executing {file} ...')
    filepath = dir_old_schema + file
    schema_update(filepath)

