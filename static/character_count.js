$(document).ready(function() {
	var pathname = window.location.pathname;
	var isbn = pathname.split("/")[2]
	$.ajax({
		url: '/get_user_rating',
		type: 'GET',
		dataType: 'json',
		contentType: "application/json",
		data: {'isbn':isbn},
	})
	.done(function(data) {
		user_rating = data.user_rating;
		if(user_rating != null) {
			$(".stars").each(function(obj,i) {
				$(this).children().each(function(e) {
					if(e < user_rating) {
						$(this).addClass('current')
					}
				})
			})
		}
	})
	.fail(function() {
		console.log("error");
	})
	$('textarea#review').on('keyup', function() {
		var length = $(this).val().length;
		var charactersLeft = 20000 - length;
		var html = `${charactersLeft} characters left`
		$("#character-count").empty().append(html);
	})
	$('.stars li').mouseover(function() {
		var total = parseInt($(this).data('value'))
		$(this).parent().children('li.star').each(function(e) {
			if(e < total) {
				$(this).addClass('hover')
				$(this).removeClass('not-hover')
			}
			else {
				$(this).addClass('not-hover')
			}
		})
	}).mouseout(function() {
		$(this).parent().children('li.star').each(function(e) {
			$(this).removeClass('hover')
			$(this).removeClass('not-hover')
		})
	}).click(function() {
		console.log("hello")
		var total_stars = parseInt($(this).data('value'))
		$(this).parent().children('li.star').each(function(e) {
			if(e < total_stars) {
				$(this).addClass('selected')
			}
		})

		//add rating to server
		var data = {
			'stars': total_stars,
			'isbn': isbn,
			'current_rating': user_rating
		}
		$.ajax({
			url: '/add_rating',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify(data),
		})
		.done(function() {
			console.log("success");
		})
		.fail(function() {
			console.log("error");
		})
	})
})
