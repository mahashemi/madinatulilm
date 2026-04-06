from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_founder_phone_max_length_60'),
    ]

    operations = [
        # Remove old text blob
        migrations.RemoveField(
            model_name='partnerpage',
            name='bank_details',
        ),
        # Bank 1
        migrations.AddField(
            model_name='partnerpage',
            name='bank1_name',
            field=models.CharField(blank=True, default='ICICI Bank', help_text='Display name, e.g. ICICI Bank', max_length=200),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank1_beneficiary',
            field=models.CharField(blank=True, default='Muhammadiyyah Educational & Social Welfare Trust', max_length=300),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank1_branch',
            field=models.CharField(blank=True, default='Siwan, Bihar', max_length=200),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank1_account_no',
            field=models.CharField(blank=True, help_text='Account number', max_length=50),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank1_ifsc',
            field=models.CharField(blank=True, help_text='IFSC / Swift code', max_length=20),
        ),
        # Bank 2
        migrations.AddField(
            model_name='partnerpage',
            name='bank2_name',
            field=models.CharField(blank=True, default='State Bank of India', help_text='Display name, e.g. State Bank of India', max_length=200),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank2_beneficiary',
            field=models.CharField(blank=True, default='Muhammadiyyah Educational & Social Welfare Trust', max_length=300),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank2_branch',
            field=models.CharField(blank=True, default='Gopal Pur, Bihar', max_length=200),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank2_account_no',
            field=models.CharField(blank=True, help_text='Account number', max_length=50),
        ),
        migrations.AddField(
            model_name='partnerpage',
            name='bank2_ifsc',
            field=models.CharField(blank=True, help_text='IFSC / Swift code', max_length=20),
        ),
        # Cheque name
        migrations.AddField(
            model_name='partnerpage',
            name='cheque_name',
            field=models.CharField(
                blank=True,
                default='Muhammadiyyah Educational & Social Welfare Trust',
                help_text='Name to write on cheques',
                max_length=300,
            ),
        ),
    ]
