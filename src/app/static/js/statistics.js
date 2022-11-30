var options = {
series: [
    {
        name: "Absolventi VŠ",
        type: "line",
        data: graduates,
        },    
    {
    name: "Noví lékaři v ČLK",
    type: "line",
    data: new_doctors,
    },
    
],

chart: {
    height: 350,
    type: "line",
    stacked: false
},
stroke: {
    width: [4, 4],
},
title: {
    text: "",
},
dataLabels: {
    enabled: true,
    enabledOnSeries: [0,1],
},
labels: years,
xaxis: {
    type: "int",
    title: 'Rok'
},
yaxis: [
    {
    title: {
        text: "Počet",
    },
    }
],
};

var chart = new ApexCharts(document.querySelector("#linechart"), options);
chart.render();