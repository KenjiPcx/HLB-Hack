import React, { useState } from "react";
import Instructions from "./CompanyForm";
import Stats from "./Stats";
import Container from "react-bootstrap/Container";
import Spinner from "react-bootstrap/Spinner";
import { displayPartsToString } from "typescript";

export type Display = {
  showRes: boolean;
  loading: boolean;
  res: any;
};

function MainContent() {
  const [display, setDisplay] = useState<Display>({
    showRes: false,
    loading: false,
    res: null,
  });

  const resetPage = () => {
    setDisplay((displayData: Display) => {
      return {
        ...displayData,
        showRes: false,
        loading: false,
        res: null,
      };
    });
  };

  const displayData = () => {
    if (display.loading) {
      return <Spinner animation="border" />;
    } else if (display.showRes) {
      return <Stats res={display.res} showRes={display.showRes} />;
    } else {
      return <Instructions setDisplay={setDisplay} />;
    }
  };

  return (
    <Container className="mainContent">
      <div onClick={resetPage}>
        <h2>ESG Scout</h2>
        <div>Analyse Esg Contents in Documents</div>
      </div>
      <Container className="infoContainer">{displayData()}</Container>
    </Container>
  );
}

export default MainContent;
