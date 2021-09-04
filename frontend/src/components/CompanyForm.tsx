import React, { useState, useEffect } from "react";
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
  const [companyName, setCompanyName] = useState("");
  const [type, setType] = useState("pdf");
  const [files, setFiles] = useState([] as File[]);
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [error, setError] = useState(false);

  const uploadType = () => {
    switch (type) {
      case "pdf":
        return (
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
        );
      case "text":
        return (
          <Form.Group
            className="mb-4"
            controlId="exampleForm.ControlTextarea1"
            style={{ textAlign: "left" }}
          >
            <Form.Label>Enter Short Text</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              onChange={(e) => setText(e.target.value)}
            />
          </Form.Group>
        );
      case "url":
        return (
          <Form.Group
            controlId="formWebsiteUrl"
            className="mb-4"
            style={{ textAlign: "left" }}
          >
            <Form.Label>Website Url</Form.Label>
            <Form.Control
              type="text"
              placeholder="Website Url"
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <Form.Text className="text-muted">
              The Url of the Website.
            </Form.Text>
          </Form.Group>
        );
    }
  };

  const handleSubmit = async () => {
    if (
      (type === "pdf" && files.length === 0) ||
      (type === "text" && text === "") ||
      (type === "url" && url === "")
    ) {
      setError(true);
      setTimeout(() => {
        setError(false);
      }, 3000);
      return;
    }
    const formData = new FormData();
    formData.append("companyName", companyName);
    if (type === "pdf") {
      files.forEach((file, i) => formData.append(`file${i}`, file));
    } else if (type === "text") {
      formData.append("text", text);
    } else {
      formData.append("url", url);
    }
    try {
      setDisplay((displayData: Display) => {
        return {
          ...displayData,
          loading: true,
        };
      });
      const URL: string = `http://127.0.0.1:5000/${type}`;
      const res = await axios.post(URL, formData);
      setDisplay((displayData: Display) => {
        return {
          ...displayData,
          res: res.data,
          showRes: true,
          loading: false,
        };
      });
    } catch (e) {
      setDisplay((displayData: Display) => {
        return {
          ...displayData,
          showRes: false,
          loading: false,
        };
      });
    }
  };

  return (
    <Col md={9} lg={5} xl={5}>
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
            required
          />
          <Form.Text className="text-muted">The Name of the Company.</Form.Text>
        </Form.Group>
        <Form.Group
          controlId="formBasicSelect"
          className="mb-4"
          style={{ textAlign: "left" }}
        >
          <Form.Label>Select Norm Type</Form.Label>
          <Form.Control
            as="select"
            value={type}
            onChange={(e) => {
              setType(e.target.value);
            }}
          >
            <option value="pdf">Upload PDF File</option>
            <option value="text">Text</option>
            <option value="url">Website URL</option>
          </Form.Control>
        </Form.Group>
        {uploadType()}
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
