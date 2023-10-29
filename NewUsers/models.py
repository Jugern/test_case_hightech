from django.db import models, migrations
from django.contrib.auth.models import User, AbstractUser
from uuid import uuid4


class Migration(migrations.Migration):
    dependencies = [
        ('CustomUsers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='new_id',
            field=models.UUIDField(default=uuid4, editable=False),
            preserve_default=False,
        ),
        migrations.RunSQL('UPDATE CustomUsers_customuser SET new_id = id'),
        migrations.RemoveField(
            model_name='customuser',
            name='id',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='new_id',
            new_name='id',
        ),
    ]


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username


class EmailChangeToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    old_email = models.EmailField()
    new_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
    key = models.CharField(max_length=32)


class InactiveUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)





