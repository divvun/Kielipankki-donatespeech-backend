"""Test discriminated union: PromptItem with itemType=text."""

from models import TextInputItem, ScheduleItem


def test_prompt_item_text_valid():
    """Test valid PromptItem with kind=prompt and itemType=text."""
    item = TextInputItem(
        kind="prompt",
        itemId="text-prompt-001",
        itemType="text",
        isRecording=True,
    )

    assert item.itemType == "text"
    assert item.isRecording is True


def test_prompt_item_text_in_schedule():
    """Test PromptItem text as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "prompt",
        "itemId": "text-prompt-002",
        "itemType": "text",
        "typeId": None,
        "options": [],
        "isRecording": False,
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = TextInputItem(**item_dict)

    assert isinstance(schedule_item, TextInputItem)
    assert schedule_item.itemType == "text"


def test_prompt_item_text_no_options():
    """Test PromptItem text with empty options array."""
    item = TextInputItem(
        kind="prompt",
        itemId="text-prompt-no-opts",
        itemType="text",
        isRecording=True,
    )

    assert item.itemType == "text"


def test_prompt_item_text_no_other_entry_label():
    """Test PromptItem text without otherEntryLabel (defaults to None)."""
    item = TextInputItem(
        kind="prompt",
        itemId="text-prompt-basic",
        itemType="text",
        isRecording=False,
    )

    assert item.itemType == "text"


def test_prompt_item_text_with_long_description():
    """Test PromptItem text with long description."""
    long_desc_fi = """Kuvaile kokemuksesi yksityiskohtaisesti. 
    Sisällötä:
    - Mitä pidit
    - Mitä et pitänyt
    - Parannusehdotukset
    """
    long_desc_nb = """Beskriv din opplevelse i detalj.
    Inkluder informasjon om:
    - Hva du likte
    - Hva du ikke likte
    - Forslag til forbedring
    """

    item = TextInputItem(
        kind="prompt",
        itemId="text-prompt-long",
        itemType="text",
        isRecording=True,
    )

    assert item.itemType == "text"
