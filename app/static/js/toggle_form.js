$(document).ready(function(){
    $("div.well:eq(1)").hide()
    $("button").not('#badder').click(function(){
        $("div.well:eq(1)").toggle(500);
    });
    
});