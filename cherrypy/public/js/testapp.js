$(document).ready(function() {
	$("#getTempBtn").click(function(e) {
		window.alert("inside click")
		$.post("/sensor")
		 .done(function(string) {
		 	$("#the-temp input").val(string);
		 });
		 e.preventDefault();
	});
});