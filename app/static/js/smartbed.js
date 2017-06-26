function ajax_set_sensor_value(data) {
  $("#s1-val").text(data.result.last_value);
}

function ajax_get_sensor_value(sensor_id) {
  $.getJSON(
    '/api/node',
    {id: sensor_id},
    ajax_set_sensor_value(data)
  )
}

function ajax_refresh_sensor_values() {
  ajax_get_sensor_value(1);
}