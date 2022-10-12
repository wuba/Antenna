from utils.enumeration import Enumeration

# tag类型
MESSAGE_TYPES = Enumeration([
    (1, "HTTP", "HTTP"),
    (2, "DNS", "DNS"),
    (3, "LDAP", "LDAP"),
    (4, "RMI", "RMI"),
    (5, "FTP", "FTP"),
    (6, "MYSQL", "MYSQL"),
    (7, "HTTPS", "HTTPS")
])
