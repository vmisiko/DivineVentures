# Generated by Django 2.2.5 on 2020-01-24 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MpesaApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='B2cTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TransactionID', models.CharField(blank=True, max_length=50, null=True)),
                ('TransactionAmount', models.FloatField(default=0.0)),
                ('B2CWorkingAccountAvailableFunds', models.FloatField(default=0.0)),
                ('B2CUtilityAccountAvailableFunds', models.FloatField(default=0.0)),
                ('TransactionCompletedDateTime', models.DateTimeField(blank=True, null=True)),
                ('ReceiverPartyPublicName', models.CharField(blank=True, max_length=50, null=True)),
                ('B2CChargesPaidAccountAvailableFunds', models.FloatField(default=0.0)),
                ('B2CRecipientIsRegisteredCustomer', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
