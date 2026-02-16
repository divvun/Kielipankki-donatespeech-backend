"""Test discriminated union: PromptItem with itemType=super-choice."""

from models import SuperChoicePromptItem, ScheduleItem


def test_prompt_item_super_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=super-choice."""
    item = SuperChoicePromptItem(
        itemId="super-choice-001",
        itemType="super-choice",
        description="Choose one or enter text",
        options=["Predefined 1", "Predefined 2", "Predefined 3"],
        isRecording=True,
        otherEntryLabel="Or type your own",
    )

    assert item.itemType == "super-choice"
    assert item.otherEntryLabel == "Or type your own"
    assert item.isRecording is True


def test_prompt_item_super_choice_in_schedule():
    """Test PromptItem super-choice as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "super-choice-002",
        "itemType": "super-choice",
        "typeId": None,
        "url": None,
        "description": "Select from list or add custom value",
        "options": ["English", "Finnish", "Swedish"],
        "isRecording": False,
        "otherEntryLabel": "Type language",
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = SuperChoicePromptItem(**item_dict)

    assert isinstance(schedule_item, SuperChoicePromptItem)
    assert schedule_item.itemType == "super-choice"
    assert schedule_item.otherEntryLabel == "Type language"


def test_prompt_item_super_choice_without_other_entry():
    """Test PromptItem super-choice without otherEntryLabel (defaults to None)."""
    item = SuperChoicePromptItem(
        itemId="super-choice-no-label",
        itemType="super-choice",
        description="Super-choice without custom entry field",
        options=["Option A", "Option B"],
        isRecording=True,
    )

    assert item.itemType == "super-choice"
    assert item.otherEntryLabel is None


def test_prompt_item_super_choice_with_many_options():
    """Test PromptItem super-choice with many predefined options."""
    options = [f"Item {i}" for i in range(1, 31)]

    item = SuperChoicePromptItem(
        itemId="super-choice-many",
        itemType="super-choice",
        description="Select from 30 items or add custom",
        options=options,
        isRecording=False,
        otherEntryLabel="Add custom item",
    )

    assert item.itemType == "super-choice"
    assert len(item.options) == 30
    assert item.options[0] == "Item 1"
    assert item.options[29] == "Item 30"
    assert item.otherEntryLabel == "Add custom item"
