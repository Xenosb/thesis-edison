$(document).ready(function($) {

  var chart_data = [];
  for (i=0;i<8;i++) {
    chart_data[i] = [];
    for (j=0;j<8;j++) {
      chart_data[i][j] = 0;
    }
  }

  var layout = {
	  showlegend: false
  };
  var data = [
    {
      z: chart_data,
      type: 'heatmap',
      showscale: false
    }
  ];
  
  Plotly.plot('chart-heatmap', data, layout, {displayModeBar: false});

  sensor_refresher = setInterval(update_heatmap_values, 1000);
  
});

function update_heatmap_values(){

  $.ajax({
    url: 'api/chart/heatmap',
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      chart_data = data['result'];

      var layout = {
        showlegend: false
      };

      var data = [
        {
          z: chart_data,
          type: 'heatmap',
          showscale: false
        }
      ];

      Plotly.plot('chart-heatmap', data, layout, {displayModeBar: false});
    }
  });

}