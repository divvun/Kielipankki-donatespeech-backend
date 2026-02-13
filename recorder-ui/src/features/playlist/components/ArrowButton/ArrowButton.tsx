import React from "react";
import "./ArrowButton.css";
import ArrowBackward from "./webNavigateTriangle.svg";
import ArrowForward from "./webNavigateTriangleForward.svg";

interface ArrowButtonProps {
  direction: "forward" | "backward";
  onClick: () => void;
  label: string;  
}

const ArrowButton: React.FC<ArrowButtonProps> = ({ direction, onClick, label }) => {
  const icon = direction === "forward" ? ArrowForward : ArrowBackward;
    const ariaLabel = label;
  return (
    <button onClick={onClick} className="arrow-button" aria-label={ariaLabel} tabIndex={0}>
	  <img src={icon} alt={ariaLabel} />
    </button>
  );
};

export default ArrowButton;
