"""Test discriminated union: PromptItem with itemType=multi-choice."""

from models import MultiChoicePromptItem, ScheduleItem


def test_prompt_item_multi_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=multi-choice."""
    item = MultiChoicePromptItem(
        kind="prompt",
        itemId="multi-choice-001",
        itemType="multi-choice",
        options=[
            {"fi": "Option A", "nb": "Option A"},
            {"fi": "Option B", "nb": "Option B"},
            {"fi": "Option C", "nb": "Option C"},
        ],
        isRecording=False,
        otherEntryLabel={"fi": "Other", "nb": "Other"},
    )

    assert item.itemType == "multi-choice"
    assert item.otherEntryLabel == {"fi": "Other", "nb": "Other"}
    assert item.isRecording is False


def test_prompt_item_multi_choice_in_schedule():
    """Test PromptItem multi-choice as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "multi-choice-002",
        "itemType": "multi-choice",
        "typeId": None,
        "options": [
            {"fi": "TV", "nb": "TV"},
            {"fi": "Radio", "nb": "Radio"},
            {"fi": "Podcast", "nb": "Podcast"},
            {"fi": "Streaming", "nb": "Streaming"},
        ],
        "isRecording": True,
        "otherEntryLabel": {"fi": "Other source", "nb": "Other source"},
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = MultiChoicePromptItem(**item_dict)

    assert isinstance(schedule_item, MultiChoicePromptItem)
    assert schedule_item.itemType == "multi-choice"
    assert schedule_item.otherEntryLabel == {
        "fi": "Other source",
        "nb": "Other source",
    }


def test_prompt_item_multi_choice_without_other_entry():
    """Test PromptItem multi-choice without otherEntryLabel (defaults to None)."""
    item = MultiChoicePromptItem(
        kind="prompt",
        itemId="multi-choice-no-other",
        itemType="multi-choice",
        options=[{"fi": "Opt 1", "nb": "Opt 1"}, {"fi": "Opt 2", "nb": "Opt 2"}],
        isRecording=False,
    )

    assert item.itemType == "multi-choice"
    assert item.otherEntryLabel is None


def test_prompt_item_multi_choice_many_options():
    """Test PromptItem multi-choice with many options and other entry label."""
    options = [{"fi": f"Category {i}", "nb": f"Category {i}"} for i in range(1, 21)]

    item = MultiChoicePromptItem(
        kind="prompt",
        itemId="multi-choice-many",
        itemType="multi-choice",
        options=options,
        isRecording=True,
        otherEntryLabel={"fi": "Specify other", "nb": "Specify other"},
    )

    assert item.itemType == "multi-choice"
    assert len(item.options) == 20
    assert item.otherEntryLabel == {"fi": "Specify other", "nb": "Specify other"}
