from django.db import models

class News(models.Model):
    id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=200) 
    news_content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200)
    author = models.CharField(max_length=100)


class OrgBind(models.Model):
    id = models.AutoField(primary_key = True)
    plat_id = models.IntegerField(db_index = True)
    org_id = models.CharField(max_length = 32, db_index = True)
    member_id = models.CharField(max_length = 32, db_index = True)

