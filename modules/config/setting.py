from modules.config.models import Config



def get_bool(key):
    if key.lower() == "true" or key.lower() == "1":
        return True
    elif key.lower() == "false" or key.lower() == "0":
        return False


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
EMAIL_HOST = config_record.get(name="EMAIL_HOST_USER").value
# 邮箱服务器端口
EMAIL_PORT = int(config_record.get(name="EMAIL_PORT").value)
# 邮箱账户
EMAIL_HOST_USER = config_record.get(name="EMAIL_HOST").value
# 邮箱授权码
EMAIL_HOST_PASSWORD = config_record.get(name="EMAIL_HOST_PASSWORD").value
# 隐藏后台地址
LOGIN_PATH = config_record.get(name="LOGIN_PATH").value
# 消息七天保存
SAVE_MESSAGE_SEVEN_DAYS = int(config_record.get(name="EMAIL_SAVE_MESSAGE_SEVEN_DAYS").value)
# DNS 端口
DNS_PORT = int(config_record.get(name="DNS_PORT").value)
# DNS域名解析IP
DNS_DOMAIN_IP = config_record.get(name="DNS_DOMAIN_IP").value
# FTP 端口
FTP_PORT = int(config_record.get(name="FTP_PORT"))
# HTTPS 端口
HTTPS_PORT = int(config_record.get(name="HTTPS_PORT"))



def reload_config(type):
    config_record = Config.objects.all()
    globals()['PLATFORM_DOMAIN'] = config_record.get(name="PLATFORM_DOMAIN").value
    globals()['DNS_DOMAIN'] = config_record.get(name="DNS_DOMAIN").value
    globals()['NS1_DOMAIN'] = config_record.get(name="NS1_DOMAIN").value
    globals()['NS2_DOMAIN'] = config_record.get(name="NS2_DOMAIN").value
    globals()['SERVER_IP'] = config_record.get(name="SERVER_IP").value
    globals()['JNDI_PORT'] = int(config_record.get(name="JNDI_PORT").value)
    globals()['OPEN_REGISTER'] = int(get_bool(config_record.get(name="OPEN_REGISTER").value))
    globals()['INVITE_TO_REGISTER'] = int(get_bool(config_record.get(name="INVITE_TO_REGISTER").value))
    globals()['OPEN_EMAIL'] = int(get_bool(config_record.get(name="OPEN_EMAIL").value))
    globals()['EMAIL_HOST'] = config_record.get(name="EMAIL_HOST_USER").value
    globals()['EMAIL_PORT'] = int(config_record.get(name="EMAIL_PORT").value)
    globals()['EMAIL_HOST_USER'] = config_record.get(name="EMAIL_HOST").value
    globals()['EMAIL_HOST_PASSWORD'] = config_record.get(name="EMAIL_HOST_PASSWORD").value
