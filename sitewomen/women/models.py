from datetime import datetime
from django.db import models


class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (f"Women(id={self.pk}, title='{self.title}', content={self.content[:30]}, "
                f"time_create={datetime.strftime(self.time_create, '%d-%b-%Y-%H:%M:%S')}, "
                f"time_update={datetime.strftime(self.time_update, '%d-%b-%Y-%H:%M:%S')}, "
                f"is_published={self.is_published})"
                )

    def __repr__(self) -> str:
        return str(self)

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
