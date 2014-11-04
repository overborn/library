$(document).ready(function() {
	$(".authorsDiv input").keyup(function(){
		var id = $(this).attr('id').slice(8);
		var query = $(this).val();
		//alert(id);
		// $(this).autocomplete({
		// 	source: '/get_authors/' + id,
		// 	minLength: 3
		// })
	    // $.getJSON('/get_authors/' + id, {"authors-" + id: query}, function(data){
		   //  $(this).html(data);

		   //  $(this).autocomplete({
		   //  	source: data.results,
		   //  	minLength: 3
		   //  });
	    // });
	    	});

});

