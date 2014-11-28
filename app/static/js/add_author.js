$("#badder").click(function(){
    $.ajax({
        type: "GET",
        url: $SCRIPT_ROOT + "/add_author",
        contentType: "application/json; charset=utf-8",
        data: { author: $('input[name="adder"]').val() },
        success: function(data) {
            $('div.authors').prepend(data);
        }
    });
});