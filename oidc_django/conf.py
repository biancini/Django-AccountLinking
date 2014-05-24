PORT = 443
BASE = "https://account-linking.mib.garr.it:" + str(PORT) + "/oidc/"

# If BASE is https these has to be specified
SERVER_KEY = ''
SERVER_CERT = ''
CA_BUNDLE = None

VERIFY_SSL = False

# information used when registering the client, this may be the same for all OPs
ME = {
    "application_type": "web",
    "contacts": ["ops@example.com"],
    "redirect_uris": ["%sauthz_cb" % BASE],
    "post_logout_redirect_uris": ["%slogout" % BASE]
}

BEHAVIOUR = {
    "response_type": "code",
    "scope": ["openid", "profile", "email", "address", "phone"],
}

# The keys in this dictionary are the OPs short user friendly name
# not the issuer (iss) name.

CLIENTS = {
    # The ones that support webfinger, OP discovery and client registration
    # This is the default, any client that is not listed here is expected to
    # support dynamic discovery and registration.
    "": {
        "client_info": ME,
        "behaviour": BEHAVIOUR
    },

}
