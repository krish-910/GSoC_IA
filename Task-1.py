# Importing internet archive python library
import internetarchive as ia

# Defining the collection name
collection_name = 'nle-historicaltextbooks'

# Defining the media type which we need to scan
media_type = 'texts'

# Searching for all items in the collection with Media Type - Text
items = ia.search_items('collection:' + collection_name + ' mediatype:' + media_type)

# Loop through all the Full Text items and printing their URLs
cnt = 0
for item in items:
    cnt += 1
    print(str(cnt) + " " + item['identifier'])
    
    item_url = f"https://archive.org/details/{item_id}"
    print("URL:", item_url)

    item_id = item['identifier']
    item_metadata = ia.get_item(item_id)
    print("Metadata:", item_metadata.metadata)
    print()