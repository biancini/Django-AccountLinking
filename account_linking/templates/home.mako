<!DOCTYPE html>
<html>
	<head>
		<title>Account Linking</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" href="/static/css/garr.css" type="text/css" media="screen" />
	</head>
	<body>
		<div id="header">
			<div class="subheader">
				<div class="logo">
					<img src="/static/images/service-button.png" width="300" height="300" alt="Account Linking" />
				</div>
				<div class="welcome">
					<h3>Account linking</h3>
					<p>Example Service to implement use case.<br/></p>
				</div>
			</div>
		</div>
		<div id="content">
			<h1>Welcome ${user.first_name} ${user.last_name}!!!!</h1>
                        <h2>
				You last login to this service was<br/>
                                on ${login_date}<br/>
				with ${login_method} credentials.
			</h2>
		</div>
		<div id="footer">
			<a href="http://www.geant.net" target="_blank">G&eacute;ant - GN3+</a>
		</div>
	</body>
</html>

