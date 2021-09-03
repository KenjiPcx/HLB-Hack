import React, { useState } from "react";
import Box from "@mui/material/Box";
import Fab from "@mui/material/Fab";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import Container from "react-bootstrap/Container";
import ReactApexChart from "react-apexcharts";

interface StatsProps {
  res: any[];
}

function Stats({ res }: StatsProps) {
  const [page, setPage] = useState(0);
  const state = {
    series: [44, 25, 31],
    chartOptions: {
      labels: ["Apple", "Mango", "Orange"],
    },
  };

  const renderGraphs = () => {
    switch (page) {
      case 0:
        return (
          <>
            <h5>ESG Distribution</h5>
            <ReactApexChart
              options={state.chartOptions}
              series={state.series}
              type="pie"
              className="chart"
              width={500}
            />
          </>
        );
      case 1:
        return (
          <>
            <h5>Environmental</h5>
            <ReactApexChart
              options={state.chartOptions}
              series={state.series}
              type="radar"
              className="chart"
              width={500}
            />
          </>
        );
      case 2:
        return (
          <>
            <h5>Social</h5>
            <ReactApexChart
              options={state.chartOptions}
              series={state.series}
              type="pie"
              className="chart"
              width={500}
            />
          </>
        );
      case 3:
        return (
          <>
            <h5>Governance</h5>
            <ReactApexChart
              options={state.chartOptions}
              series={state.series}
              type="pie"
              className="chart"
              width={500}
            />
          </>
        );
      default:
        setPage(0);
    }
  };

  return (
    <Container className="stats">
      {renderGraphs()}
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
