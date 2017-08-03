var histo_columns = 128;
var histo_values = Array.apply(null, Array(128)).map(function (_, i) {return 0;});
var histo_chart_elem = $('#main-chart');

var histo_datasets = {
  labels: Array.apply(null, Array(128)).map(function (_, i) {return i;}),
  datasets: [
    {
      label: 'Sensor values',
      backgroundColor: convertHex($.brandInfo,10),
      borderColor: $.brandInfo,
      pointHoverBackgroundColor: '#fff',
      borderWidth: 2,
      data: histo_values
    }
  ]
};

var histo_options = {
  maintainAspectRatio: false,
  legend: {
    display: false
  },
  scales: {
    xAxes: [{
      gridLines: {
        drawOnChartArea: false
      }
    }],
    yAxes: [{
      ticks: {
        beginAtZero: true,
        maxTicksLimit: 5,
        stepSize: 1
      }
    }]
  },
  elements: {
    point: {
      radius: 0,
      hitRadius: 10,
      hoverRadius: 4,
      hoverBorderWidth: 3,
    }
  },
};

var histo_chart = new Chart(histo_chart_elem, {
  type: 'bar',
  data: histo_datasets,
  options: histo_options
});

$(document).ready(function ($) {

  get_histogram_values();

  sensor_refresher = setInterval(get_histogram_values, 1000);

});

function get_histogram_values(){

  $.ajax({
    url: 'api/chart/histogram',
    type: "GET",
    dataType: 'json',
    success: function (data) {
      for (i in histo_chart.data.datasets[0].data) {
        histo_chart.data.datasets[0].data[i] = 0;
      }
      for (value in data['result']) {
        histo_chart.data.datasets[0].data[Math.round(data['result'][value]/512)] += 1;
      }
      histo_chart.update();
    }
  });

}

function convertHex(hex,opacity){
  hex = hex.replace('#','');
  var r = parseInt(hex.substring(0,2), 16);
  var g = parseInt(hex.substring(2,4), 16);
  var b = parseInt(hex.substring(4,6), 16);

  var result = 'rgba('+r+','+g+','+b+','+opacity/100+')';
  return result;
}

function random(min,max) {
  return Math.floor(Math.random()*(max-min+1)+min);
}