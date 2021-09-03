import React from "react";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";

function TopNavbar() {
  return (
    <Navbar bg="dark" variant="dark" className="topAppBar">
      <Container>
        <Navbar.Brand href="#home">ESG Judger</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default TopNavbar;
