from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_trustee_is_founder'),
    ]

    operations = [
        migrations.AddField(
            model_name='trustee',
            name='member_type',
            field=models.CharField(
                choices=[('trustee', 'Trustee'), ('consultant', 'Consulting Member')],
                default='trustee',
                help_text="Select 'Trustee' for board members or 'Consulting Member' for advisory/consulting members.",
                max_length=20,
                verbose_name='Member Type',
            ),
        ),
    ]
