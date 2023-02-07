from utils.enumeration import Enumeration

# 配置类型
CONFIG_TYPES = Enumeration([
    (0, "PLATFORM", "平台配置"),
    (1, "PROTOCAL", "协议配置"),
    (2, "EMAIL", "邮件配置"),
    (3, "MESSAGE", "消息配置"),
    (4, "DNS", "DNS监听配置"),
    (5, "JNDI", "RMI/LDAP监听配置"),
    (6, "HTTPS", "HTTPS监听配置"),
    (7, "FTP", "FTP监听配置"),
])
