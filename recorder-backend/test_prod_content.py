#!/usr/bin/env python3
"""Test if production content files parse correctly with new models."""

import json
import os
from models import Schedule, Theme

def test_prod_schedules():
    """Test production schedule files."""
    print("=== Testing Production Schedules ===")
    schedule_dir = "content/prod/schedules"
    schedule_files = os.listdir(schedule_dir)
    
    success = 0
    failed = 0
    
    for schedule_file in schedule_files:
        if not schedule_file.endswith('.json'):
            continue
            
        filepath = os.path.join(schedule_dir, schedule_file)
        try:
            with open(filepath) as f:
                data = json.load(f)
            schedule = Schedule(**data)
            print(f"✓ {schedule_file}: {len(schedule.items)} items")
            success += 1
        except Exception as e:
            print(f"✗ {schedule_file}: {type(e).__name__}: {str(e)[:80]}")
            failed += 1
    
    print(f"\nSchedules: {success} passed, {failed} failed\n")
    return failed == 0

def test_prod_themes():
    """Test production theme files."""
    print("=== Testing Production Themes ===")
    theme_dir = "content/prod/themes"
    theme_files = os.listdir(theme_dir)
    
    success = 0
    failed = 0
    
    for theme_file in theme_files:
        if not theme_file.endswith('.json'):
            continue
            
        filepath = os.path.join(theme_dir, theme_file)
        try:
            with open(filepath) as f:
                data = json.load(f)
            theme = Theme(**data)
            print(f"✓ {theme_file}")
            success += 1
        except Exception as e:
            print(f"✗ {theme_file}: {type(e).__name__}: {str(e)[:80]}")
            failed += 1
    
    print(f"\nThemes: {success} passed, {failed} failed\n")
    return failed == 0

if __name__ == "__main__":
    schedules_ok = test_prod_schedules()
    themes_ok = test_prod_themes()
    
    if schedules_ok and themes_ok:
        print("✅ All production content files parse successfully!")
        exit(0)
    else:
        print("❌ Some production content files failed to parse")
        exit(1)
