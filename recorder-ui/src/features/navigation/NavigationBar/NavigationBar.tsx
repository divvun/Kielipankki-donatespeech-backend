import React from "react";
import { useLocation } from "react-router-dom";
import Navbar from "react-bootstrap/Navbar";
import NavItem from "react-bootstrap/NavItem";
import Nav from "react-bootstrap/Nav";
import NavigationItem from "../NavigationItem/NavigationItem";
import TotalRecordingDuration from "../../playlist/components/TotalRecordingDuration/TotalRecordingDuration";
import routes from "../../../config/routes";

import "./NavigationBar.css";

type NavigationBarProps = {};

const NavigationBar: React.FC<NavigationBarProps> = () => {
  const { pathname } = useLocation();
  if (pathname && pathname.startsWith(routes.SCHEDULE)) {
    // Do not show navbar for playlist
    return null;
  }

  return (
    <Navbar expand="lg">
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav>
          <NavItem>
            <NavigationItem
              isFirst={true}
              text="Project name"
              to={routes.HOME}
            />
          </NavItem>
          <NavItem>
            <NavigationItem text="Partners" to={routes.PARTNERS} />
          </NavItem>
          <NavItem>
            <NavigationItem text="Privacy" to={routes.PRIVACY} />
          </NavItem>
          <NavItem>
            <NavigationItem text="About the project" to={routes.INFO} />
          </NavItem>
          <Nav.Link
            target="_blank"
            rel="noopener noreferrer"
            href="https://example.com/hankkeen-nimi"
          >
            Campaign website
          </Nav.Link>
        </Nav>
      </Navbar.Collapse>
      <div className="float-right mt-3">
        <TotalRecordingDuration label="You have donated:" />
      </div>
    </Navbar>
  );
};

export default NavigationBar;
