import React from "react";
import hyLogo from "./hyBlack.png";
import "./PartnersPage.css";

type PartnersPageProps = {};

const PartnersPage: React.FC<PartnersPageProps> = () => {
  return (
    <div className="partners-page frame--view">
      <h2>Partners</h2>
      <p className="mb-4">
        The “Project name” campaign is carried out in cooperation with the
        University of Helsinki and partner organizations.
      </p>
      <div className="partner-page--icons partner-page--icons-1 d-flex flex-wrap">
        <div className="d-flex flex-wrap justify-content-center">
          <img src={hyLogo} alt="University of Helsinki" />
        </div>
      </div>
    </div>
  );
};

export default PartnersPage;
