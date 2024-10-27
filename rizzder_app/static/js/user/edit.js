$('#editUserSubmit').on('click', function () {
   var paramDescription = "";
   if (description !== document.getElementById("description").value)
      paramDescription = document.getElementById("description").value;
   $.ajax({
		url: "/api/user/edit/",
		type: "POST",
		data: {
			description : paramDescription,
			token : getCookie('token')
		},
		success: function(json) {

		},
		error: function(err) {
			alert("MESSAGE ERRORS")
		},

	});
});

var noPhotosAdded = 0;

$('#editPhtotoSubmit').on('click', function () {
   var formData = new FormData();
   formData.append('file', $('#photoFile')[0].files[0]);
   $.ajax({
		url: "/api/user/edit/photo/?token=" + getCookie('token'),
		type: "POST",
		data : formData,
	    processData: false,
	    contentType: false,
		success: function(json) {

		},
		error: function(err) {
			alert("MESSAGE ERRORS")
		},

	});
});