from django.db import models


class AbstractBaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        abstract = True
    
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.uuid}>"
