$(document).ready(function() {

var MaxInputs       = 8; //maximum input boxes allowed
var InputsWrapper   = $("#InputsWrapper"); //Input boxes wrapper ID
var AddButton       = $("#AddMoreFileBox"); //Add button ID

var x = InputsWrapper.length; //initlal text box count
var FieldCount= $('input:text').length - 1; //to keep track of text box added

$(AddButton).click(function (e)  //on add input button click
{
        if(x <= MaxInputs) //max input box allowed
        {
            FieldCount++; //text box added increment
            //add input box
            //$('form').append('<div><input type="text" class="span4" id="authors-' + FieldCount +'" name="authors[]" placeholder="author ' + FieldCount +'"><a href="#" class="removeclass">&times;</a></div>');
            var a = $("#authorsDiv").clone();
            a.children('input').attr({
            id: 'authors-' + FieldCount,
            name: 'authors-' + FieldCount,
            placeholder: 'author ' + FieldCount,
            value : ''                 
            });
            a.appendTo('form');
            // $('<input>').attr({
            //     type: 'text',
            //     id: 'authors-' + FieldCount ,
            //     name: 'authors-' + FieldCount, 
            //     value: "value"}).appendTo('form');
            x++; //text box increment
        }

return false;
});

$("body").on("click",".removeclass", function(e){ //user click on remove text
        if( $('input:text').length > 2 ) {
                $(this).parent('div').remove(); //remove text box
                x--; //decrement textbox
        }
return false;
}) 

});