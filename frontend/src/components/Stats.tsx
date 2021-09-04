import React, { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Fab from "@mui/material/Fab";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import Container from "react-bootstrap/Container";
import ReactApexChart from "react-apexcharts";

interface StatsProps {
  res: any;
  showRes: boolean;
}

type ChartOptions = {
  labels: any[];
};

function Stats({ res, showRes }: StatsProps) {
  const [page, setPage] = useState(0);
  if (res) {
    console.log(res.res);
  }

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
      case 0:
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
      case 1:
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
      case 2:
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
      case 3:
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
      default:
        setPage(0);
    }
  };

  useEffect(() => {
    console.log(res);
  }, [res]);

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
