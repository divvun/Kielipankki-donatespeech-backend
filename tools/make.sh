#!/bin/bash
# set -x #echo on

SCHEDULE_NAMES=(2elain 3lahella 4urheilu 5korona 6luonto 46media 89media lukiomedia)
SCHEDULE_IDS=(3a73d87a-8856-4ca0-9af2-da66c99a95f9 0598bf14-ab48-4ccb-a50c-0bd779f77933 8aaf82be-de16-4449-9fd2-677291a0e804 f5c5fd20-34f9-4ff8-bdba-666bbf1740ce cbb91217-b323-46d7-b3af-16c41206c60d f5c74c5e-e19c-47f6-beff-9631d9c7b6d6 e6433174-6e3c-470c-8e63-b2ef2335e26a 92d22fe6-ae1d-448a-b17d-d8ac9f274f56)

cd makeschedule
source venv/bin/activate

for i in {0..7}
do
    echo "Processing '${SCHEDULE_NAMES[i]}', scheduleId = ${SCHEDULE_IDS[i]}"
    echo "Copying downloaded CSV file"
    cp ~/Downloads/${SCHEDULE_NAMES[i]}.csv ../../content/${SCHEDULE_NAMES[i]}.csv
    echo "Generating JSON file"
    python3 makeschedule.py ../../content/${SCHEDULE_NAMES[i]}.csv dev >~/tmp/${SCHEDULE_IDS[i]}.json
    echo "Copying result to repository folder"
    cp ~/tmp/${SCHEDULE_IDS[i]}.json ../../content/dev/schedules
    # cp ~/tmp/${SCHEDULE_IDS[i]}.json ../../content/prod/schedules
    echo ""
done

deactivate
cd ..

echo "Use dev-upload.sh to copy the schedule files to Amazon S3"
