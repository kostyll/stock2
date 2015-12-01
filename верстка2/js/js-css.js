$(document).ready(function() {


	$('input.ShowOrHide').click(function() { 
	    var checked = $("input.ShowOrHide:checked"); 
	    if ( checked.length == 0 ) {
	        $("div.ShowOrHide").slideUp(500);
	    } else {
	        $("div.ShowOrHide").slideDown(500);
	        checked.each(function() {
	            $( 'div#' + $(this).val() ).show();
	        });
	    }
	});



}); //end of all code