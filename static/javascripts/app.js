$(document).ready( {
	$("#registerButton").on("click", function() {
		$("#registerForm").submit();
	});

	$("#loginButton").on("click", function() {
		$("loginForm").submit()
	});
});