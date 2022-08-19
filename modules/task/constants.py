from utils.enumeration import Enumeration

# 任务状态
TASK_STATUS = Enumeration([
    (0, "CLOSE", "关闭"),
    (1, "OPEN", "开启"),
])


# 任务是否为缓存任务

TASK_TMP = Enumeration([
    (0, "TMP", "tmp"),
    (1, "FORMAL", "formal"),
])

# 任务是否展示到首页

SHOW_DASHBOARD = Enumeration([
    (0, "FALSE", "false"),
    (1, "TRUE", "true"),
])
