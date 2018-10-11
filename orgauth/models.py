from django.db import models

class OrgUserAuth(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.CharField(max_length=32,db_index=True, unique=True)
    org_id = models.CharField(max_length=32)
    passwd = models.CharField(max_length=160)
    org_role = models.CharField(max_length=16)


class OrgRolePerm(models.Model):
    id = models.AutoField(primary_key = True)
    role_name = models.CharField(max_length = 32, db_index=True)
    perm_list = models.TextField()

