from utils.enumeration import Enumeration

# 组件是否公开
PRIVATE_TYPES = Enumeration([
    (1, "PUBLIC", "公开"),
    (0, "PRIVATE", "私有"),
])

# 组件所属类型
TEMPLATE_TYPES = Enumeration([
    (1, "LISTEN", "监听"),
    (0, "PAYLOAD", "利用"),
])

# 组件是否多选
CHOICE_TYPES = Enumeration([
    (1, "MULTIPLE", "多选"),
    (0, "SINGLE", "单选"),
])
