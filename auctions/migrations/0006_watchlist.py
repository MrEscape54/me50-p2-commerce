# Generated by Django 3.0.5 on 2020-08-17 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='auctions.Auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('user', 'auction')},
            },
        ),
    ]
