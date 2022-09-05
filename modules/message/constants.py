from utils.enumeration import Enumeration

# tag类型
MESSAGE_TYPES = Enumeration([
    (1, "HTTP", "http"),
    (2, "DNS", "dns"),
    (3, "LDAP", "ldap"),
    (4, "RMI", "rmi"),
    (5, "FTP", "ftp"),
])
