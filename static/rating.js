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
		$("#horizontal li").each(function(e) {
			if(e < user_rating) {
				$(this).addClass('current');
			}
		})
	}
	})
	.fail(function() {
		console.log("error");
	})
	$("#horizontal li").mouseover(function() {
		var total_stars = parseInt($(this).data('value'));
		$(this).parent().children("li.star").each(function(e) {
			if(e < total_stars) {
				$(this).addClass('hover');
			}
			else {
				$(this).removeClass('hover');
			}
		})
	}).mouseout(function() {
			$(this).parent().children("li.star").each(function(e) {
				$(this).removeClass('hover');
		})
	});
	$("#horizontal li").click(function() {
		var total_stars = parseInt($(this).data('value'));
		$(this).parent().children("li.star").each(function(e) {
			if(e < total_stars) {
				$(this).addClass('selected')
			}
			else {
				$(this).removeClass('selected')
			}
		})
		var data = {
			'stars': total_stars,
			'isbn': isbn,
			'current_rating': user_rating
		}
		$.ajax({
			url: '/add_rating',
			type: 'POST',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify(data)
		}).done(function() {
			console.log("success");
		}).fail(function() {
			console.log("error");
		})	
	});

})

