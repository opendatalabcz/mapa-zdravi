var options = {
series: [
    {
    name: "Website Blog",
    type: "column",
    data: {{data}},
    },
    {
    name: "Website Blog",
    type: "column",
    data: {{data}},
    },

    {
    name: "Social Media",
    type: "line",
    data: {{data}},
    },
],

chart: {
    height: 350,
    type: "line",
},
stroke: {
    width: [0, 4],
},
title: {
    text: "Traffic Sources",
},
dataLabels: {
    enabled: true,
    enabledOnSeries: [1],
},
labels: [
    "01 Jan 2001",
    "02 Jan 2001",
    "03 Jan 2001",
    "04 Jan 2001",
    "05 Jan 2001",
    "06 Jan 2001",
    "07 Jan 2001",
    "08 Jan 2001",
    "09 Jan 2001",
    "10 Jan 2001",
    "11 Jan 2001",
    "12 Jan 2001",
],
xaxis: {
    type: "datetime",
},
yaxis: [
    {
    title: {
        text: "Website Blog",
    },
    },
    {
    opposite: true,
    title: {
        text: "Social Media",
    },
    },
],
};
