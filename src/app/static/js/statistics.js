var new_doctors_options = {
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

var chart = new ApexCharts(document.querySelector("#linechart"), new_doctors_options);
chart.render();

// -----------------------------------------------------------------------------
//  BARCHART
var graduates_options = {
    series: [{
    name: 'Češi',
    data: graduated_czechs
  }, {
    name: 'Slováci',
    data: graduated_slovaks
  }, {
    name: 'Ostatní',
    data: graduated_others
  }],
    chart: {
    type: 'bar',
    height: 350
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '55%',
      endingShape: 'rounded'
    },
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
  xaxis: {
    categories: years ,
  },
  yaxis: {
    title: {
      text: 'Počet'
    }
  },
  fill: {
    opacity: 1
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return  val
      }
    }
  }
  };

  var chart = new ApexCharts(document.querySelector("#barchart"), graduates_options);
  chart.render();



