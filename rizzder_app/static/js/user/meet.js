$(document).ready(function() {
    $.ajax({
		url: "/api/user/info/getLocation/",
		type: "POST",
		data: {
			token : getCookie('token')
		},
		success: function(json) {
			getPreferredUsers();
		},
		error: function(err) {
			alert("MESSAGE ERRORS")
		},

	});
});

function getPreferredUsers() {
	$.ajax({
		url: "/api/user/getPreferredUsers/",
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
}