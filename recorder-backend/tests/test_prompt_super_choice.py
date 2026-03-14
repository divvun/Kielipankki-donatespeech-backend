"""Test discriminated union: PromptItem with itemType=super-choice."""

from models import SuperChoicePromptItem, ScheduleItem


def test_prompt_item_super_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=super-choice."""
    item = SuperChoicePromptItem(
        kind="prompt",
        itemId="super-choice-001",
        itemType="super-choice",
        options=[
            {"fi": "Predefined 1", "nb": "Predefined 1"},
            {"fi": "Predefined 2", "nb": "Predefined 2"},
            {"fi": "Predefined 3", "nb": "Predefined 3"},
        ],
        isRecording=True,
        otherEntryLabel={"fi": "Or type your own", "nb": "Or type your own"},
    )

    assert item.itemType == "super-choice"
    assert item.otherEntryLabel == {
        "fi": "Or type your own",
        "nb": "Or type your own",
    }
    assert item.isRecording is True


def test_prompt_item_super_choice_in_schedule():
    """Test PromptItem super-choice as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "super-choice-002",
        "itemType": "super-choice",
        "typeId": None,
        "options": [
            {"fi": "English", "nb": "English"},
            {"fi": "Finnish", "nb": "Finnish"},
            {"fi": "Swedish", "nb": "Swedish"},
        ],
        "isRecording": False,
        "otherEntryLabel": {"fi": "Type language", "nb": "Type language"},
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = SuperChoicePromptItem(**item_dict)

    assert isinstance(schedule_item, SuperChoicePromptItem)
    assert schedule_item.itemType == "super-choice"
    assert schedule_item.otherEntryLabel == {
        "fi": "Type language",
        "nb": "Type language",
    }


def test_prompt_item_super_choice_without_other_entry():
    """Test PromptItem super-choice without otherEntryLabel (defaults to None)."""
    item = SuperChoicePromptItem(
        kind="prompt",
        itemId="super-choice-no-label",
        itemType="super-choice",
        options=[{"fi": "Option A", "nb": "Option A"}, {"fi": "Option B", "nb": "Option B"}],
        isRecording=True,
    )

    assert item.itemType == "super-choice"
    assert item.otherEntryLabel is None


def test_prompt_item_super_choice_with_many_options():
    """Test PromptItem super-choice with many predefined options."""
    options = [{"fi": f"Item {i}", "nb": f"Item {i}"} for i in range(1, 31)]

    item = SuperChoicePromptItem(
        kind="prompt",
        itemId="super-choice-many",
        itemType="super-choice",
        options=options,
        isRecording=False,
        otherEntryLabel={"fi": "Add custom item", "nb": "Add custom item"},
    )

    assert item.itemType == "super-choice"
    assert len(item.options) == 30
    assert item.options[0]["fi"] == "Item 1"
    assert item.options[29]["fi"] == "Item 30"
    assert item.otherEntryLabel == {"fi": "Add custom item", "nb": "Add custom item"}
