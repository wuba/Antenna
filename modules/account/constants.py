from utils.enumeration import Enumeration

# 用户存活状态
ALIVE_TYPES = Enumeration([
    (1, "ALIVE", "alive"),
    (0, "DEATH", "death"),
])

# 用户是否是第一次登录
FIRST_LOGIN = Enumeration([
    (0, "FALSE", "false"),
    (1, "TRUE", "true"),
])

# 平台注册方式
REGISTER_TYPE = Enumeration([
    (0, "REFUSE", "refuse"),
    (1, "EMAIL", "email"),
    (2, "INVITE", "invite"),
])
