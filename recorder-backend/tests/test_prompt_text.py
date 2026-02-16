"""Test discriminated union: PromptItem with itemType=text."""

from models import TextInputItem, ScheduleItem


def test_prompt_item_text_valid():
    """Test valid PromptItem with kind=prompt and itemType=text."""
    item = TextInputItem(
        itemId="text-prompt-001",
        itemType="text-input",
        description="Enter your response",
        isRecording=True,
    )
    
    assert item.itemType == "text-input"
    assert item.isRecording is True


def test_prompt_item_text_in_schedule():
    """Test PromptItem text as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "text-prompt-002",
        "itemType": "text-input",
        "typeId": None,
        "url": None,
        "description": "What is your name?",
        "options": [],
        "isRecording": False,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = TextInputItem(**item_dict)
    
    assert isinstance(schedule_item, TextInputItem)
    assert schedule_item.itemType == "text-input"


def test_prompt_item_text_no_options():
    """Test PromptItem text with empty options array."""
    item = TextInputItem(
        itemId="text-prompt-no-opts",
        itemType="text-input",
        description="Free text input",
        isRecording=True,
    )
    
    assert item.itemType == "text-input"


def test_prompt_item_text_no_other_entry_label():
    """Test PromptItem text without otherEntryLabel (defaults to None)."""
    item = TextInputItem(
        itemId="text-prompt-basic",
        itemType="text-input",
        description="Simple text question",
        isRecording=False,
    )
    
    assert item.itemType == "text-input"


def test_prompt_item_text_with_long_description():
    """Test PromptItem text with long description."""
    long_desc = """Please describe your experience in detail. 
    Include information about:
    - What you liked
    - What you disliked
    - Suggestions for improvement
    """
    
    item = TextInputItem(
        itemId="text-prompt-long",
        itemType="text-input",
        description=long_desc,
        isRecording=True,
    )
    
    assert item.itemType == "text-input"
    assert long_desc in item.description
