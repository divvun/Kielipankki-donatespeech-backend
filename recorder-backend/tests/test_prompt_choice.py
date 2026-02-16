"""Test discriminated union: PromptItem with itemType=choice."""

from models import PromptItem, ScheduleItem


def test_prompt_item_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=choice."""
    item = PromptItem(
        kind="prompt",
        itemId="choice-001",
        itemType="choice",
        typeId=None,
        url=None,
        description="Choose one option",
        options=["Option 1", "Option 2", "Option 3"],
        isRecording=False,
    )
    
    assert item.kind == "prompt"
    assert item.itemType == "choice"
    assert item.typeId is None
    assert item.url is None
    assert item.options == ["Option 1", "Option 2", "Option 3"]
    assert item.isRecording is False


def test_prompt_item_choice_in_schedule():
    """Test PromptItem choice as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "choice-002",
        "itemType": "choice",
        "typeId": None,
        "url": None,
        "description": "Select your age group",
        "options": ["18-25", "26-40", "41-60", "60+"],
        "isRecording": True,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = PromptItem(**item_dict)
    
    assert isinstance(schedule_item, PromptItem)
    assert schedule_item.kind == "prompt"
    assert schedule_item.itemType == "choice"
    assert len(schedule_item.options) == 4


def test_prompt_item_choice_single_option():
    """Test PromptItem choice with single option."""
    item = PromptItem(
        kind="prompt",
        itemId="choice-single",
        itemType="choice",
        typeId=None,
        url=None,
        description="Continue?",
        options=["Yes"],
        isRecording=False,
    )
    
    assert item.itemType == "choice"
    assert len(item.options) == 1
    assert item.options[0] == "Yes"


def test_prompt_item_choice_many_options():
    """Test PromptItem choice with many options."""
    options = [f"Option {i}" for i in range(1, 101)]
    
    item = PromptItem(
        kind="prompt",
        itemId="choice-many",
        itemType="choice",
        typeId=None,
        url=None,
        description="Choose from 100 options",
        options=options,
        isRecording=True,
    )
    
    assert item.itemType == "choice"
    assert len(item.options) == 100
    assert item.options[99] == "Option 100"
