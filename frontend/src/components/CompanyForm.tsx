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
  const fooURL = "http://127.0.0.1:5000/foo";
  const barURL = "http://127.0.0.1:5000/bar";

  const [companyName, setCompanyName] = useState("");
  const [usePdf, setUsePdf] = useState(false);
  const [text, setText] = useState("");
  const [files, setFiles] = useState([] as File[]);
  const [error, setError] = useState(false);

  const handleSubmit = async () => {
    if (files.length === 0 && text === "") {
      setError(true);
      setTimeout(() => {
        setError(false);
      }, 3000);
      return;
    }
    const formData = new FormData();
    formData.append("companyName", companyName);
    if (usePdf) {
      files.forEach((file, i) => formData.append(`file${i}`, file));
    } else {
      formData.append("text", text);
    }
    try {
      setDisplay((displayData: Display) => {
        return {
          ...displayData,
          loading: true,
        };
      });
      const URL: string = usePdf ? fooURL : barURL;
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
            required
          />
          <Form.Text className="text-muted">The Name of the Company.</Form.Text>
        </Form.Group>

        {usePdf ? (
          <Form.Group
            controlId="formFileMultiple"
            className="mb-4"
            style={{ textAlign: "left" }}
          >
            <Form.Label>Company Info Pdf</Form.Label>
            <Button size="sm" variant="link" onClick={() => setUsePdf(false)}>
              Use Text?
            </Button>
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
        ) : (
          <Form.Group
            className="mb-4"
            controlId="exampleForm.ControlTextarea1"
            style={{ textAlign: "left" }}
          >
            <Form.Label>Example textarea</Form.Label>
            <Button size="sm" variant="link" onClick={() => setUsePdf(true)}>
              Use Pdf?
            </Button>
            <Form.Control
              as="textarea"
              rows={3}
              onChange={(e) => setText(e.target.value)}
            />
          </Form.Group>
        )}
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
