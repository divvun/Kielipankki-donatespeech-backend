import json
import uuid
import sys

# Load the JSON file
with open(sys.argv[1], "r") as file:
    data = json.load(file)
# Replace the itemId
for items in data["items"]:
    items["itemId"] = str(uuid.uuid4())
# Save the updated JSON back to a file
with open(sys.argv[1], "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
