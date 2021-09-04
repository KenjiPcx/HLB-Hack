import React, { useState, useEffect } from "react";
import Fab from "@mui/material/Fab";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Paragraph from "./Paragraph";
import ReactApexChart from "react-apexcharts";
import Form from "react-bootstrap/Form";

interface StatsProps {
  res: any;
  showRes: boolean;
}

type ChartOptions = {
  labels: any[];
};

type ParagraphObj = {
  paragraph: string;
  tag: string;
};

function Stats({ res, showRes }: StatsProps) {
  const [page, setPage] = useState(0);
  const [label, setLabel] = useState("");

  const getLabels = (data: ParagraphObj[]) => {
    const labels: string[] = [];
    data.forEach((paragraph) => {
      if (!labels.includes(paragraph.tag)) {
        labels.push(paragraph.tag);
      }
    });
    return labels;
  };

  const filterData = (data: ParagraphObj[]) => {
    if (label === "") {
      return data;
    }
    return data.filter((paragraph) => paragraph.tag === label);
  };

  const getSeriesAndLabels = (field: any) => {
    let series: string[] = [];
    let chartOptions: ChartOptions = {
      labels: [],
    };
    field.forEach((item: any) => {
      chartOptions.labels.push(item[0]);
      series.push(item[1]);
    });
    return {
      series: series,
      chartOptions: chartOptions,
    };
  };

  const renderGraphs = () => {
    if (!showRes) return "";
    let chartData;
    switch (page) {
      case -1:
        setPage(5);
        return;
      case 0:
        const labels = getLabels(res.data);
        const paragraphs = filterData(res.data);
        return (
          <>
            <Form.Group
              controlId="formBasicSelect"
              className="mb-4"
              style={{ textAlign: "left" }}
            >
              <Form.Control
                as="select"
                value={label}
                onChange={(e) => {
                  setLabel(e.target.value);
                }}
              >
                <option value={""} key={-1}>
                  All Labels
                </option>
                {labels.map((label: string, key: number) => {
                  return (
                    <option value={label} key={key}>
                      {label}
                    </option>
                  );
                })}
              </Form.Control>
            </Form.Group>
            <Container className="textDisplay">
              {paragraphs.map((paragraph: ParagraphObj, key: number) => {
                return (
                  <Paragraph
                    key={key}
                    paragraph={paragraph.paragraph}
                    tag={paragraph.tag}
                  />
                );
              })}
            </Container>
          </>
        );
      case 1:
        chartData = getSeriesAndLabels(res.merged);
        return (
          <>
            <h5>ESG Distribution</h5>
            <ReactApexChart
              options={chartData.chartOptions}
              series={chartData.series}
              type="pie"
              className="chart"
              width={500}
            />
          </>
        );
      case 2:
        chartData = getSeriesAndLabels(res.enviromental);
        return (
          <>
            <h5>Environmental</h5>
            <ReactApexChart
              options={chartData.chartOptions}
              series={chartData.series}
              type="pie"
              className="chart"
              width={700}
            />
          </>
        );
      case 3:
        chartData = getSeriesAndLabels(res.social);
        return (
          <>
            <h5>Social</h5>
            <ReactApexChart
              options={chartData.chartOptions}
              series={chartData.series}
              type="pie"
              className="chart"
              width={700}
            />
          </>
        );
      case 4:
        chartData = getSeriesAndLabels(res.governance);
        return (
          <>
            <h5>Governance</h5>
            <ReactApexChart
              options={chartData.chartOptions}
              series={chartData.series}
              type="pie"
              className="chart"
              width={700}
            />
          </>
        );
      case 5:
        return (
          <>
            <h5>{`Overall Findings for This Document`}</h5>
            <Container className="overallStats">
              <Row>
                <Col>
                  <h6>Document Contains Information About</h6>
                  {res.top_5_factors.map((factor: string, key: number) => {
                    return <li key={key}>{factor}</li>;
                  })}
                </Col>
              </Row>
            </Container>
          </>
        );
      case 6:
        setPage(0);
        return;
    }
  };

  return (
    <Container className="stats">
      {renderGraphs()}
      <Fab
        color="primary"
        aria-label="add"
        sx={{ position: "absolute", bottom: 15, left: 15 }}
        onClick={() => setPage((page) => page - 1)}
      >
        <ArrowBackIosIcon />
      </Fab>
      <Fab
        color="primary"
        aria-label="add"
        sx={{ position: "absolute", bottom: 15, right: 15 }}
        onClick={() => setPage((page) => page + 1)}
      >
        <ArrowForwardIosIcon />
      </Fab>
    </Container>
  );
}

export default Stats;
