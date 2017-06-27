$(document).ready(function($){
  sensor_refresher = setInterval(ajax_refresh_sensor_values, 300);
});