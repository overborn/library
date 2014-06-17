$('form').submit(function() {
	var data = $('#autorsDiv input').val();
	alert(data);
$.ajax({
  //url: "/book/edit",
  type: 'POST',
  data: data,
  success: function(data, status){
    //check status
    //do something with data
    alert(data);
  }
});
});