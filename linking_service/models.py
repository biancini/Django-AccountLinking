from django.db import models
from datetime import datetime

# Classi di modellazione degli attori


#   Column   |         Type          |                              Modifiers                               
#------------+-----------------------+----------------------------------------------------------------------
# id         | integer               | not null default nextval('account_linking_profile_id_seq'::regclass)
# al_name    | character varying(50) | not null
# al_mail    | character varying(50) | not null
# al_surname | character varying(50) | not null

class AccountLinkingProfile(models.Model):
    al_id = models.AutoField(primary_key=True, db_column='id')
    al_name = models.CharField(max_length=50, db_column='al_name')
    al_surname = models.CharField(max_length=50, db_column='al_surname')
    al_mail = models.CharField(max_length=50, db_column='al_mail')

    class Meta:
        db_table = 'account_linking_profile'

#           Column           |          Type          | Modifiers 
#----------------------------+------------------------+-----------
# account_linking_profile_id | integer                | 
# ad_authid                  | character varying(100) | not null
# ad_name                    | character varying(50)  | 
# ad_surname                 | character varying(50)  | 
# ad_mail                    | character varying(50)  | 
# ad_type                    | character varying(10)  | 
# ad_idp                     | character varying(100) | 
class AuthData(models.Model):
    al_profile = models.ForeignKey('AccountLinkingProfile', db_column='account_linking_profile_id')
    ad_authid = models.CharField(max_length=50, primary_key=True, db_column='ad_authid')
    ad_name = models.CharField(max_length=50, db_column='ad_name')
    ad_surname = models.CharField(max_length=50, db_column='ad_surname')
    ad_mail = models.CharField(max_length=50, db_column='ad_mail')
    ad_type = models.CharField(max_length=10, db_column='ad_type')
    ad_idp = models.CharField(max_length=100, db_column='ad_idp')

    class Meta:
        db_table = 'auth_data'
