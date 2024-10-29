$(document).ready(function() {
    $.ajax({
		url: "/api/user/info/getLocation/",
		type: "POST",
		data: {
			token : getCookie('token')
		},
		success: function(json) {

		},
		error: function(err) {
			alert("MESSAGE ERRORS")
		},

	});
});