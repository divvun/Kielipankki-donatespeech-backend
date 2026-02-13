import React, { useState, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Select from "react-select";
import "./PromptElement.css";
import { answerChange, selectCurrentItemAnswer } from "../../playlistSlice";
import { PlaylistAnswer, DisplayedElement } from "../../types";
import Row from "react-bootstrap/Row";
import ItemDescription from "../ItemDescription/ItemDescription";

type PromptElementProps = {
    element: DisplayedElement;
    lang: string;
};

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = { "choose": "Valitse"}
const en_strings: Langstrings = { "choose": "Choose"}
const sv_strings: Langstrings = { "choose": "Välj" }

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

type Option = { label: string; value: string };
type SelectedOption = Option | Option[] | null;

const optionToValue = (o: Option | null) => (o !== null ? o.value : "");
const selectedOptionToValue = (o: SelectedOption) =>
  Array.isArray(o) ? o.map(optionToValue) : optionToValue(o);
const valueToOption = (v: string) => ({ value: v, label: v } as Option);
const valueToSelectedOption = (v: string | string[] | undefined | null) => {
  if (Array.isArray(v)) {
    return v.map(valueToOption);
  }

  return v ? valueToOption(v) : null;
};

const PromptElement: React.FunctionComponent<PromptElementProps> = ({
    element, lang,
}) => {
  const answer = useSelector(selectCurrentItemAnswer);
  const answerValue = answer ? answer.value : "";
  const [value, setValue] = useState<string | string[]>(answer?.value || "");
  const [extraInputValue, setExtraInputValue] = useState<string>(
    answer?.extraValue || ""
  );
  const [selectedOption, setSelectedOption] = useState<SelectedOption>(
    valueToSelectedOption(answerValue)
  );
  const dispatch = useDispatch();

  const inputRef = useRef<HTMLInputElement | null>(null);
  useEffect(() => {
    if (inputRef.current) inputRef.current.focus();
  }, []);

  const { item } = element;
  if (!item) return null;

  const getOtherValue = () => {
    if (item.itemType !== "multi-choice") return undefined;
    // With multi-choice, last options is considered as "other" selection
    const optionsLength = item.options && item.options.length;
    return optionsLength > 0 ? item.options[optionsLength - 1] : undefined;
  };

  const handleValueChange = (newValue: string | string[]) => {
    if (!item) return;

    setValue(newValue);

    const answer: PlaylistAnswer = {
      itemId: item.itemId,
      value: newValue,
      extraValue: extraInputValue,
      otherValueInConfiguration: getOtherValue(),
    };

    dispatch(answerChange(answer));
  };

  const handleExtraInputValueChange = (newExtraValue: string) => {
    if (!item) return;

    setExtraInputValue(newExtraValue);

    const answer: PlaylistAnswer = {
      itemId: item.itemId,
      value: value,
      extraValue: newExtraValue,
      otherValueInConfiguration: getOtherValue(),
    };

    dispatch(answerChange(answer));
  };

  const handleSelectChange = (option: SelectedOption) => {
    setSelectedOption(option);
    handleValueChange(selectedOptionToValue(option));
  };

  const renderSelect = () => {
      const options = item.options
      ? item.options.map(valueToOption).filter(o => o !== null)
	    : [];


    const showExtraInput =
      item.itemType !== "choice" && Boolean(item.otherEntryLabel);
    const extraInputId = `_${item.otherEntryLabel}`;
    return (
      <>
        <Select
            styles={{
		control: (provided, state) => ({
		    ...provided,
		    borderColor: "#123e6c",
		    borderWidth: "medium",
		    borderRadius: "20px",
		}),
		indicatorSeparator: (provided, state) => ({
		    visibility: "hidden",
		}),
		multiValue: (provided, state) => ({
		    ...provided,
		    borderRadius: "10px",
		}),
	    }}
          isMulti={item.itemType === "multi-choice"}
        placeholder={langs[lang]["choose"]}
          value={selectedOption}
          onChange={o => handleSelectChange(o as SelectedOption)}
          options={options}
          menuPosition="fixed"
          menuPlacement="bottom"
          isClearable={false}
          id={element.title}
          name={element.title}
          noOptionsMessage={() => ""}
        />
        {showExtraInput && (
          <>
            <label className="mt-2" htmlFor={extraInputId}>
              {item.otherEntryLabel}
            </label>
            <input
              className="form-control form-control-lg"
              value={extraInputValue}
              onChange={e => handleExtraInputValueChange(e.target.value)}
              id={extraInputId}
              name={item.otherEntryLabel}
            />
          </>
        )}
      </>
    );
  };

  const renderInput = () => {
    return (
      <input
        ref={el => (inputRef.current = el)}
        className="form-control form-control-lg"
        value={value || ""}
        onChange={e => handleValueChange(e.target.value)}
        id={element.title}
        name={element.title}
      />
    );
  };

  const renderControl = () => {
    const { itemType } = item;
    if (itemType === "text") {
      return renderInput();
    } else {
      return renderSelect();
    }
  };

  return (
    <div className="prompt-element">
      <label className="prompt-title" htmlFor={element.title}>
        {element.title}
      </label>
      		  <Row>
		       <ItemDescription
			  isSmall={true}
			  description={element.body1}
		      />
		   </Row>
		   <Row>
		       <ItemDescription
			  isSmall={true}
			  description={element.body2}
		      />
		   </Row>

      {renderControl()}
    </div>
  );
};

export default PromptElement;
