import React, { useState } from "react";
import Instructions from "./CompanyForm";
import Stats from "./Stats";
import Container from "react-bootstrap/Container";
import Spinner from "react-bootstrap/Spinner";

export type Display = {
  showRes: boolean;
  loading: boolean;
  res: any[];
};

function MainContent() {
  const [display, setDisplay] = useState<Display>({
    showRes: false,
    loading: false,
    res: [],
  });

  const displayData = () => {
    if (display.loading) {
      return <Spinner animation="border" />;
    } else if (display.showRes) {
      return <Stats res={display.res} />;
    } else {
      return <Instructions setDisplay={setDisplay} />;
    }
  };

  return (
    <Container className="mainContent">
      <div>
        <h2>ESG Judger</h2>
        <div>Judge How ESG Friendly Companies Are</div>
      </div>
      <Container className="infoContainer">{displayData()}</Container>
    </Container>
  );
}

export default MainContent;
