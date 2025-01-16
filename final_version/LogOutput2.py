import json
from datetime import datetime
from collections import defaultdict

file_path = "C:/Users/vince/Downloads/detections_log.json"
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
json_data = load_json_data(file_path)

def analyze_changes_for_attribute(data, target_identity, attribute, start_date=None, end_date=None):
    # Filter data for the target identity
    filtered_data = [
        entry for entry in data if target_identity.lower() in entry["identity"].lower()
    ]

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        filtered_data = [
            entry for entry in filtered_data
            if datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").date() >= start_date.date()
        ]
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        filtered_data = [
            entry for entry in filtered_data
            if datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").date() <= end_date.date()
        ]

    sorted_records = sorted(
        filtered_data, key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S")
    )

    changes = []
    for i in range(1, len(sorted_records)):
        prev_record = sorted_records[i - 1]
        curr_record = sorted_records[i]
        if prev_record[attribute] != curr_record[attribute]:
            changes.append({
                "from": prev_record["timestamp"],
                "to": curr_record["timestamp"],
                "old_value": prev_record[attribute],
                "new_value": curr_record[attribute]
            })

    return changes

target_identity = input("Enter the identity to analyze: ")
attribute = input("Enter the attribute to check for changes: ")
start_date = input("Enter the start date (YYYY-MM-DD) or leave blank: ") or None
end_date = input("Enter the end date (YYYY-MM-DD) or leave blank: ") or None

attribute_changes = analyze_changes_for_attribute(json_data, target_identity, attribute, start_date, end_date)

if attribute_changes:
    print(f"Changes for attribute '{attribute}' for {target_identity}:")
    for change in attribute_changes:
        print(f"  From {change['from']} to {change['to']}: '{change['old_value']}' -> '{change['new_value']}'")
else:
    print(f"No changes detected for attribute '{attribute}' for {target_identity}.")