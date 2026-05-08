"""Test discriminated union: PromptItem with itemType=choice."""

from app.models import ChoicePromptItem


def test_prompt_item_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=choice."""
    item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-001",
        itemType="choice",
        options=[
            "Option 1",
            "Option 2",
            "Option 3",
        ],
        isRecording=False,
    )

    assert item.itemType == "choice"
    assert item.isRecording is False


def test_prompt_item_choice_in_schedule():
    """Test PromptItem choice as ScheduleItem discriminated union."""
    schedule_item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-002",
        itemType="choice",
        typeId=None,
        options=[
            "18-25",
            "26-40",
            "41-60",
            "60+",
        ],
        isRecording=True,
    )

    assert isinstance(schedule_item, ChoicePromptItem)
    assert schedule_item.itemType == "choice"
    assert len(schedule_item.options) == 4


def test_prompt_item_choice_single_option():
    """Test PromptItem choice with single option."""
    item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-single",
        itemType="choice",
        options=["Yes"],
        isRecording=False,
    )

    assert item.itemType == "choice"
    assert len(item.options) == 1
    assert item.options[0] == "Yes"


def test_prompt_item_choice_many_options():
    """Test PromptItem choice with many options."""
    options = [f"Option {i}" for i in range(1, 101)]

    item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-many",
        itemType="choice",
        options=options,
        isRecording=True,
    )

    assert item.itemType == "choice"
    assert len(item.options) == 100
    assert item.options[99] == "Option 100"
