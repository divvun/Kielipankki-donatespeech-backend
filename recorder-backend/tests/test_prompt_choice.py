"""Test discriminated union: PromptItem with itemType=choice."""

from models import ChoicePromptItem, ScheduleItem


def test_prompt_item_choice_valid():
    """Test valid PromptItem with kind=prompt and itemType=choice."""
    item = ChoicePromptItem(
        kind="prompt",
        itemId="choice-001",
        itemType="choice",
        default={"title": {"fi": "Valitse", "nb": "Velg"}, "body1": {"fi": "Valitse yksi vaihtoehto", "nb": "Velg ett alternativ"}, "body2": {"fi": "", "nb": ""}},
        options=["Option 1", "Option 2", "Option 3"],
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
        "url": None,
        "title": {"fi": "Ikäryhmä", "nb": "Aldersgruppe"},
        "body1": {"fi": "Valitse ikäryhmäsi", "nb": "Velg din aldersgruppe"},
        "body2": {"fi": "", "nb": ""},
        "options": ["18-25", "26-40", "41-60", "60+"],
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
        default={"title": {"fi": "Jatka", "nb": "Fortsett"}, "body1": {"fi": "Haluatko jatkaa?", "nb": "Vil du fortsette?"}, "body2": {"fi": "", "nb": ""}},
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
        default={"title": {"fi": "Valinta", "nb": "Valg"}, "body1": {"fi": "Valitse 100 vaihtoehdosta", "nb": "Velg fra 100 alternativer"}, "body2": {"fi": "", "nb": ""}},
        options=options,
        isRecording=True,
    )

    assert item.itemType == "choice"
    assert len(item.options) == 100
    assert item.options[99] == "Option 100"
