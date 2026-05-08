"""Test discriminated union: PromptItem with itemType=multi-choice."""

from app.models import MultiChoicePromptItem


def test_prompt_item_multi_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=multi-choice."""
    item = MultiChoicePromptItem(
        kind="prompt",
        itemId="multi-choice-001",
        itemType="multi-choice",
        options=[
            "Option A",
            "Option B",
            "Option C",
        ],
        isRecording=False,
        otherEntryLabel="Other",
    )

    assert item.itemType == "multi-choice"
    assert item.otherEntryLabel == "Other"
    assert item.isRecording is False


def test_prompt_item_multi_choice_in_schedule():
    """Test PromptItem multi-choice as ScheduleItem discriminated union."""
    schedule_item = MultiChoicePromptItem(
        kind="prompt",
        itemId="multi-choice-002",
        itemType="multi-choice",
        typeId=None,
        options=[
            "TV",
            "Radio",
            "Podcast",
            "Streaming",
        ],
        isRecording=True,
        otherEntryLabel="Other source",
    )

    assert isinstance(schedule_item, MultiChoicePromptItem)
    assert schedule_item.itemType == "multi-choice"
    assert schedule_item.otherEntryLabel == "Other source"


def test_prompt_item_multi_choice_without_other_entry():
    """Test PromptItem multi-choice without otherEntryLabel (defaults to None)."""
    item = MultiChoicePromptItem(
        kind="prompt",
        itemId="multi-choice-no-other",
        itemType="multi-choice",
        options=["Opt 1", "Opt 2"],
        isRecording=False,
    )

    assert item.itemType == "multi-choice"
    assert item.otherEntryLabel is None


def test_prompt_item_multi_choice_many_options():
    """Test PromptItem multi-choice with many options and other entry label."""
    options = [f"Category {i}" for i in range(1, 21)]

    item = MultiChoicePromptItem(
        kind="prompt",
        itemId="multi-choice-many",
        options=options,
        itemType="multi-choice",
        isRecording=True,
        otherEntryLabel="Specify other",
    )

    assert item.itemType == "multi-choice"
    assert len(item.options) == 20
    assert item.otherEntryLabel == "Specify other"
