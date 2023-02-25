import os

from django.db import migrations


def create_default_config(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Config = apps.get_model("config", "Config")
    # from modules.config.models import Config
    platform_domain = os.getenv("PLATFORM_DOMAIN")
    server_ip = os.getenv("SERVER_IP")

    Config.objects.bulk_create(
        [
            Config(name="PLATFORM_DOMAIN", type=0, value=platform_domain),
            Config(name="SERVER_IP", type=0, value=server_ip),
            Config(name="JNDI_PORT", type=1, value="2345"),
            Config(name="OPEN_EMAIL", type=0, value="0"),
            Config(name="EMAIL_HOST", type=0, value="smtp.qq.com"),
            Config(name="EMAIL_PORT", type=0, value="465"),
            Config(name="EMAIL_HOST_USER", type=0, value="58@qq.com"),
            Config(name="EMAIL_HOST_PASSWORD", type=0, value="123456789"),

        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("config", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_config),
    ]
