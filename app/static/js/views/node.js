var n_sensors = 0;
var chart_all_sensors_data;
var charts = {};

$(document).ready(function ($) {

  init_sensor_values();
  sensor_refresher = setInterval(update_sensor_values, 1000);

});

function init_sensor_values(){

  $.ajax({
    url: chart_data_init_url,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      chart_all_sensors_data = Object.keys(data).map(
        function(key) {
          return [Number(key), data[key]];
      });

      n_sensors = chart_all_sensors_data.length;
      
      var options = {
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              color: 'transparent',
              zeroLineColor: 'transparent'
            },
            ticks: {
              fontSize: 2,
              fontColor: 'transparent',
            }

          }],
          yAxes: [{
            display: false,
            ticks: {
              max: 65535,
              display: false
            }
          }],
        },
        elements: {
          line: {
            borderWidth: 1
          },
          point: {
            radius: 4,
            hitRadius: 10,
            hoverRadius: 4,
          },
        }
      };

      for (i=0;i<n_sensors;i++) {
        var data = {
          labels : Array.apply(null, Array(chart_sample_points)).map(function (_, i) {return i;}),
          datasets: [
            {
              label: 'Sensor '+i,
              backgroundColor: $.brandPrimary,
              borderColor: 'rgba(255,255,255,.55)',
              data: chart_all_sensors_data[i][1]
            },
          ]
        };

        ctx = $('#sensor-chart-'+i);
        card_chart = new Chart(ctx, {
          type: 'line',
          data: data,
          options: options
        });
        charts[i] = card_chart;
      }
    }
  });

}

function update_sensor_values(){

  $.ajax({
    url: chart_data_update_url,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      for (i=0;i<n_sensors;i++) {
        charts[i].data.datasets[0].data.push(data[i][0]);
        charts[i].data.datasets[0].data.shift();
        charts[i].update();
        document.getElementById('sensor-value-'+i).textContent=data[i][0];
      }
    }
  });

}