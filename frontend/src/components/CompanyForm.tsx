import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Display } from "./MainContent";
import axios from "axios";

interface CompanyFormProps {
  setDisplay: React.Dispatch<React.SetStateAction<Display>>;
}

function CompanyForm({ setDisplay }: CompanyFormProps) {
  const URL = "http://127.0.0.1:5000/foo";

  const [companyName, setCompanyName] = useState("");
  const [files, setFiles] = useState([] as File[]);
  const [error, setError] = useState(false);

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("companyName", companyName);
    files.forEach((file, i) => formData.append(`file${i}`, file));
    try {
      setDisplay((displayData: Display) => {
        return {
          ...displayData,
          loading: true,
        };
      });
      const res = await axios.post(URL, formData);
      console.log(res);
      setDisplay((displayData: Display) => {
        return {
          ...displayData,
          res: res.data,
          showRes: true,
          loading: false,
        };
      });
    } catch (e) {
      console.log(e);
      setDisplay((displayData: Display) => {
        return {
          ...displayData,
          showRes: false,
          loading: false,
        };
      });
      setError(true);
      setTimeout(() => {
        setError(false);
      }, 3000);
    }
  };

  return (
    <Col xs={11} sm={11} md={9} lg={5} xl={5}>
      <Form
        className="companyForm"
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit();
        }}
      >
        <Form.Group
          controlId="formBasicEmail"
          className="mb-4"
          style={{ textAlign: "left" }}
        >
          <Form.Label>Company Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Company Name"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
          />
          <Form.Text className="text-muted">The Name of the Company.</Form.Text>
        </Form.Group>

        <Form.Group
          controlId="formFileMultiple"
          className="mb-4"
          style={{ textAlign: "left" }}
        >
          <Form.Label>Company Info Pdf</Form.Label>
          <Form.Control
            type="file"
            multiple
            accept=".pdf"
            onChange={(e: any) => setFiles(Array.from(e.target.files))}
          />
          <Form.Text className="text-muted">
            You can upload more than 1 file
          </Form.Text>
        </Form.Group>
        <Button
          disabled={error}
          variant={error ? "danger" : "primary"}
          onClick={handleSubmit}
        >
          {error ? "Failed" : "Calculate ESG Score"}
        </Button>
      </Form>
    </Col>
  );
}

export default CompanyForm;
