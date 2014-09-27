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
			<table cellspacing="0" cellpadding="50" width="100%">
			<tr><td width="50%">
				<img src="/static/images/image_shibboleth_logowordmark_color.png" alt="Shibboleth" width="200px"/>
				<p align="left"><b>SAML User</b></p>
				<p align="left">Access to this service using your SAML credentials</p>
				<p align="left"><a href="/shib/shib?next=${next}">Access <img src="/static/images/arrow.svg" width="16px"/></a></p>
			</td><td width="50%">
				<img src="/static/images/openid-logo-wordmark.png" alt="OpenID" width="200px"/>
				<p align="left"><b>OpenID</b></p>
				<p align="left">Access to this service using your OpenID credentials</p>
				<p align="left"><a href="/oidc/openid?next=${next}">Access <img src="/static/images/arrow.svg" width="16px"/></a></p>
			</td></tr>
			</table>
		</div>
		<div id="footer">
			<a href="http://www.geant.net" target="_blank">G&eacute;ant - GN3+</a>
		</div>
	</body>
</html>

