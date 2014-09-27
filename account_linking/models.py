from django.db import models
from datetime import datetime

# Classi di modellazione degli attori
class LastLogin(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    login_date = models.DateTimeField(default=datetime.now)
    login_method = models.CharField(max_length=10)

    class Meta:
        db_table = 'accountlinking_logins'
