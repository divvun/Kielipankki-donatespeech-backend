"""Test discriminated union: PromptItem with itemType=choice."""

from models import ChoicePromptItem, ScheduleItem


def test_prompt_item_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=choice."""
    item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-001",
        itemType="choice",
        options=[
            {"fi": "Option 1", "nb": "Option 1"},
            {"fi": "Option 2", "nb": "Option 2"},
            {"fi": "Option 3", "nb": "Option 3"},
        ],
        isRecording=False,
    )

    assert item.itemType == "choice"
    assert item.isRecording is False


def test_prompt_item_choice_in_schedule():
    """Test PromptItem choice as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "choice-002",
        "itemType": "choice",
        "typeId": None,
        "options": [
            {"fi": "18-25", "nb": "18-25"},
            {"fi": "26-40", "nb": "26-40"},
            {"fi": "41-60", "nb": "41-60"},
            {"fi": "60+", "nb": "60+"},
        ],
        "isRecording": True,
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = ChoicePromptItem(**item_dict)

    assert isinstance(schedule_item, ChoicePromptItem)
    assert schedule_item.itemType == "choice"
    assert len(schedule_item.options) == 4


def test_prompt_item_choice_single_option():
    """Test PromptItem choice with single option."""
    item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-single",
        itemType="choice",
        options=[{"fi": "Yes", "nb": "Yes"}],
        isRecording=False,
    )

    assert item.itemType == "choice"
    assert len(item.options) == 1
    assert item.options[0]["fi"] == "Yes"


def test_prompt_item_choice_many_options():
    """Test PromptItem choice with many options."""
    options = [{"fi": f"Option {i}", "nb": f"Option {i}"} for i in range(1, 101)]

    item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-many",
        itemType="choice",
        options=options,
        isRecording=True,
    )

    assert item.itemType == "choice"
    assert len(item.options) == 100
    assert item.options[99]["fi"] == "Option 100"
