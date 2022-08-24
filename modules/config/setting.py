from modules.config.models import Config
from bin.database_config import PLATFORM_DOMAIN, PLATFORM_IP


def get_bool(key):
    if key.lower() == 'true':
        return True
    elif key.lower() == 'false':
        return False


try:
    config_record = Config.objects.all()
    # 平台域名
    PLATFORM_DOMAIN = config_record.get(name="PLATFORM_DOMAIN").value
    # 做 dns 记录的域名,可以和平台域名用作同一个
    DNS_DOMAIN = config_record.get(name="DNS_DOMAIN").value
    # 监听DNS端口
    DNS_PORT = 53
    # NS域名
    NS1_DOMAIN = config_record.get(name="NS1_DOMAIN").value
    NS2_DOMAIN = config_record.get(name="NS2_DOMAIN").value
    # 服务器外网地址
    SERVER_IP = config_record.get(name="SERVER_IP").value
    # JNDI监听端口
    JNDI_PORT = int(config_record.get(name="JNDI_PORT").value)
    # 开放注册
    OPEN_REGISTER = int(get_bool(config_record.get(name="OPEN_REGISTER").value))
    # 邀请注册
    INVITE_TO_REGISTER = int(get_bool(config_record.get(name="INVITE_TO_REGISTER").value))
    # 开放邮箱通知
    OPEN_EMAIL = int(get_bool(config_record.get(name="OPEN_EMAIL").value))
    # 邮箱服务器地址
    EMAIL_HOST = config_record.get(name="EMAIL_HOST").value
    # 邮箱服务器端口
    EMAIL_PORT = int(config_record.get(name="EMAIL_PORT").value)
    # 邮箱账户
    EMAIL_HOST_USER = config_record.get(name="EMAIL_HOST_USER").value
    # 邮箱授权码
    EMAIL_HOST_PASSWORD = config_record.get(name="EMAIL_HOST_PASSWORD").value


except Exception as e:
    print(e)
    PLATFORM_DOMAIN = PLATFORM_DOMAIN
    DNS_DOMAIN = PLATFORM_DOMAIN
    DNS_PORT = 53
    NS1_DOMAIN = f"ns1.{PLATFORM_DOMAIN}"
    NS2_DOMAIN = f"ns2.{PLATFORM_DOMAIN}"
    SERVER_IP = PLATFORM_IP
    JNDI_PORT = 2345
    INVITE_TO_REGISTER = 1
    OPEN_REGISTER = 1
    EMAIL_HOST = "smtp.qq.com"
    EMAIL_PORT = 465
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
