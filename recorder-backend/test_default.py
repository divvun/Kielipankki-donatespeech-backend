import json
from models import Schedule

# Test the refactored structure
with open('content/dev/schedules/f5c5fd20-34f9-4ff8-bdba-666bbf1740ce.json') as f:
    schedule_data = json.load(f)
    schedule = Schedule(**schedule_data)
    
    # Show the first item's default state
    item = schedule.items[0]
    print(f'First item ({item.kind}/{item.itemType}):')
    print(f'  default.title (fi): {item.default.title["fi"]}')
    print(f'  default.body1 (fi): {item.default.body1["fi"][:50]}...')
    print(f'  Has recording state: {item.recording is not None}')
    print(f'  Has finish state: {item.finish is not None}')
    print()
    
    # Show a prompt item
    prompt = [i for i in schedule.items if i.kind == 'prompt'][0]
    print(f'First prompt ({prompt.kind}/{prompt.itemType}):')
    print(f'  default.title (fi): {prompt.default.title["fi"]}')
    print(f'  default.body1 (fi): {prompt.default.body1["fi"][:50]}...')
    print(f'  Options count: {len(prompt.options)}')
