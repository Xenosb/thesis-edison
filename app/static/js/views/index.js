$(document).ready(function ($) {
  sensor_refresher = setInterval(ajax_refresh_sensor_values, 1000);
});

function ajax_set_sensor_value(data) {
  $("#s1-val").text(data.result.last_value);
}

function ajax_get_sensor_value(sensor_id) {
  sensor_url = 'api/sensor?id=' + sensor_id;
  sensor_div = $('#s' + sensor_id + '-val')

  $.ajax({
    url: sensor_url,
    type: "GET",
    data: {'id': sensor_id},
    dataType: 'json',
    success: function (data) {
      sensor_div.text(data.result.last_value);
    }
  });
}

function ajax_refresh_sensor_values() {
  ajax_get_sensor_value(1);
}