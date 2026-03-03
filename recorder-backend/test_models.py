import json
from models import Schedule
import os

# Test specific schedule files
schedule_files = [
    'content/dev/schedules/f5c5fd20-34f9-4ff8-bdba-666bbf1740ce.json',
    'content/dev/schedules/cbb91217-b323-46d7-b3af-16c41206c60d.json',
    'content/dev/schedules/18644e6b-2807-4047-88aa-f063c9d61a97.json',
]

print(f'Testing {len(schedule_files)} schedule files...\n')

for schedule_file in schedule_files:
    if not os.path.exists(schedule_file):
        print(f'✗ {schedule_file} not found')
        continue
    with open(schedule_file) as f:
        schedule_data = json.load(f)
        schedule = Schedule(**schedule_data)
        print(f'✓ {os.path.basename(schedule_file)}')
        print(f'  Items: {len(schedule.items)}')
        item_types = {}
        for item in schedule.items:
            key = f'{item.kind}/{item.itemType}'
            item_types[key] = item_types.get(key, 0) + 1
        for key, count in sorted(item_types.items()):
            print(f'    - {key}: {count}')
        print()

print('✓ All schedules parsed successfully!')
