$('#editUserSubmit').on('click', function (event) {
    event.preventDefault(); // Prevents the default form submission behavior.

    var paramDescription = "";
    if (description !== document.getElementById("description").value)
        paramDescription = document.getElementById("description").value;
		console.log(paramDescription);

    $.ajax({
        url: "/api/user/edit/",
        type: "POST",
        data: {
            description: paramDescription,
            gender: document.getElementById("userGenderSelect").value,
            genderPreference: document.getElementById("userGenderPreferenceSelect").value,
            token: getCookie('token')
        },
        success: function (json) {
            // window.location.reload();
			console.log(this.data)
			console.log(json)
        },
        error: function (err) {
            alert("MESSAGE ERRORS");
        }
    });
});

var noPhotosAdded = 0;

$('#editPhotoSubmit').on('click', function () {
   var formData = new FormData();
   formData.append('file', $('#photoFile')[0].files[0]);

   console.log(formData);

   $.ajax({
		url: "/api/user/edit/photo/?token=" + getCookie('token'),
		type: "POST",
		data : formData,
	    processData: false,
	    contentType: false,
		success: function(json) {
			// TODO sa afiseze daca are deja 5 poze
			window.location.reload();
		},
		error: function(err) {
			alert("MESSAGE ERRORS")
		},

	});
});

$('.deleteButton').on('click', function () {
	image_id = $(this).attr("data-id");

	$.ajax({
		url: "/api/user/edit/delete/photo/",
		type: "POST",
		data: {
			id : image_id,
			token : getCookie('token')
		},
		success: function(json) {
			window.location.reload();
		},
		error: function(err) {
			alert("MESSAGE ERRORS")
		},

	});
});

$(document).ready(function() {
    $.ajax({
		url: "/api/user/genders/",
		type: "POST",
		data: {
			token : getCookie('token')
		},
		success: function(json) {
			html = "";
			for (i = 0; i < json['genders'].length; i++) {
				html += '<option value="' + json['genders'][i]['key'] + '">' + json['genders'][i]['value'] + '</option>';
			}

			$("#userGenderSelect").html(html);
			$("#userGenderPreferenceSelect").html(html);

			document.getElementById("userGenderSelect").value = gender;
			document.getElementById("userGenderPreferenceSelect").value = gender_preference;
		},
		error: function(err) {
			alert("MESSAGE ERRORS")
		},

	});
});