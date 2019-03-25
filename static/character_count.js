$(document).ready(function() {
	$('textarea#review').on('keyup', function() {
		var length = $(this).val().length;
		var charactersLeft = 20000 - length;
		var html = `${charactersLeft} characters left`
		$("#character-count").empty().append(html);
	})
})
