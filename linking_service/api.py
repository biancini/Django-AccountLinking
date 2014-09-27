from django.http import HttpResponse
from linking_service.models import AuthData, AccountLinkingProfile
import json

def get_userid(request):
    authid = request.GET.get('authid', None)

    if authid:
        authdata = AuthData.objects.get(ad_authid=request.GET.get('authid', None))

        #if not authdata:
        #    profile = AccountLinkingProfile.create(al_name = '', al_surname = '', al_mail = '')
        #    authdata = AuthData.objects.create(al_profile = profile, ad_authid = authid)

    	jsondata = {
            'id': authdata.al_profile.al_id,
            'name': authdata.al_profile.al_name,
            'surname': authdata.al_profile.al_surname,
            'mail': authdata.al_profile.al_mail
        }
        return HttpResponse(json.dumps(jsondata), mimetype="application/json")

    return HttpResponse(status=500)
