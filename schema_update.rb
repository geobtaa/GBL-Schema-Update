require 'json'
require 'csv'

# Manual changes before run
dir_crosswalk = 'btaa_crosswalk.csv'
dir_old_schema = 'btaa_solr_documents_1.0'
dir_new_schema = 'btaa_solr_documents_updated_ruby'

# Load the crosswalk.csv and make it a dictionary
# key-value pairs in the dictionary refers to the old-new schemas
CROSSWALK = {}

csv = CSV.parse(File.read(dir_crosswalk))

csv.each do |row|
  old = row[2]
  new = row[3]
  CROSSWALK[old] = new
end

puts CROSSWALK.inspect

# Function to update the metadata schema
def schema_update(filepath, dir_new_schema)
  file = File.read(filepath)

  puts File.basename(filepath)

  data = JSON.parse(file)
  data_crosswalked = {}

  # Old record
  puts "OLD\n"
  puts data.inspect

  CROSSWALK.each do |key,val|
    if data[key]
      data_crosswalked[val] = data[key]
    end
  end

  # check for multi-val field
  # if so, convert its value to an array
  data_crosswalked = string2array(data_crosswalked)

  # Set Aardvark
  data_crosswalked['gbl_mdVersion_s'] = "Aardvark"

  # Remove deprecated fields
  data_crosswalked = data_crosswalked.reject{|k,v| k == '-'}

  puts "NEW\n"
  puts data_crosswalked.to_json

  # Write updated JSON to a new folder
  filepath_updated = File.join(dir_new_schema, File.basename(filepath))

  File.write(filepath_updated, JSON.pretty_generate(data_crosswalked))
end

# Function to convert fields that ends with '_sm' to an array
def string2array(dict)
  dict.keys.each do |key|
    suffix = key.split('_')[-1]
    if suffix == 'sm' or suffix == 'im'
      val = dict[key]
      unless val.kind_of?(Array)
        dict[key] = [val]
      end
    end
  end

  dict
end


# Collect all JSON files in a list
# Iterate the list to update metadata schema
files = Dir.glob("#{dir_old_schema}/*.json")
files.each do |file|
  puts "Executing #{file} ..."
  schema_update(file, dir_new_schema)
end
