$(document).ready(function(){
	$("div.well").hide()
  $("button").click(function(){
    $("div.well").toggle(500);
  });
});