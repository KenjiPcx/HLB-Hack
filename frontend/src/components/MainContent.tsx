import React, { useState } from "react";
import Instructions from "./Instructions";
import Stats from "./Stats";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

function MainContent() {
  const [showRes, setShowRes] = useState(false);

  const toggleShowRes = () => {
    setShowRes(!showRes);
  };

  return (
    <Container className="mainContent">
      <Form>
        <Form.Group controlId="formFileMultiple" className="mb-3">
          <Form.Label>Company Info Pdf</Form.Label>
          <Form.Control type="file" multiple />
          <Form.Text className="text-muted">
            You can enter more than 1 file
          </Form.Text>
        </Form.Group>
        <Button onClick={toggleShowRes}>Show Res</Button>
      </Form>
      <Container className="infoContainer">
        {showRes ? <Stats /> : <Instructions />}
      </Container>
    </Container>
  );
}

export default MainContent;
