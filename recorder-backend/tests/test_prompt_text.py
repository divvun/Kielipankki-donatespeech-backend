"""Test discriminated union: PromptItem with itemType=text."""

from models import PromptItem, ScheduleItem


def test_prompt_item_text_valid():
    """Test valid PromptItem with kind=prompt and itemType=text."""
    item = PromptItem(
        kind="prompt",
        itemId="text-prompt-001",
        itemType="text",
        typeId=None,
        url=None,
        description="Enter your response",
        options=[],
        isRecording=True,
    )
    
    assert item.kind == "prompt"
    assert item.itemType == "text"
    assert item.typeId is None
    assert item.url is None
    assert item.options == []
    assert item.isRecording is True


def test_prompt_item_text_in_schedule():
    """Test PromptItem text as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "text-prompt-002",
        "itemType": "text",
        "typeId": None,
        "url": None,
        "description": "What is your name?",
        "options": [],
        "isRecording": False,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = PromptItem(**item_dict)
    
    assert isinstance(schedule_item, PromptItem)
    assert schedule_item.kind == "prompt"
    assert schedule_item.itemType == "text"
    assert schedule_item.options == []


def test_prompt_item_text_no_options():
    """Test PromptItem text with empty options array."""
    item = PromptItem(
        kind="prompt",
        itemId="text-prompt-no-opts",
        itemType="text",
        typeId=None,
        url=None,
        description="Free text input",
        options=[],
        isRecording=True,
    )
    
    assert item.itemType == "text"
    assert item.options == []
    assert len(item.options) == 0


def test_prompt_item_text_no_other_entry_label():
    """Test PromptItem text without otherEntryLabel (defaults to None)."""
    item = PromptItem(
        kind="prompt",
        itemId="text-prompt-basic",
        itemType="text",
        typeId=None,
        url=None,
        description="Simple text question",
        options=[],
        isRecording=False,
    )
    
    assert item.itemType == "text"
    assert item.otherEntryLabel is None


def test_prompt_item_text_with_long_description():
    """Test PromptItem text with long description."""
    long_desc = """Please describe your experience in detail. 
    Include information about:
    - What you liked
    - What you disliked
    - Suggestions for improvement
    """
    
    item = PromptItem(
        kind="prompt",
        itemId="text-prompt-long",
        itemType="text",
        typeId=None,
        url=None,
        description=long_desc,
        options=[],
        isRecording=True,
    )
    
    assert item.itemType == "text"
    assert long_desc in item.description
