const list = [
  {
    key: 'Home',
    path: '/home',
    meta: {
      icon: 'dashboard',
      title: '统计信息',
    },
    children: [
      {
        path: '/home',
        meta: {
          title: '总览',
        },
      },
    ],
  },
  {
    icon: 'table',
    path: '/defCenter',
    meta: {
      icon: 'table',
      title: '网站防护',
    },
    children: [
      {
        path: '/protection_list',
        meta: {
          title: '防护列表',
        },
      },
      {
        path: '/protection_log',
        meta: {
          title: '防护日志',
        },
      },
      {
        path: '/protection_business',
        meta: {
          title: '业务防护',
          hidden: true,
        },
      },
    ],
  },
  {
    path: '/rule',
    meta: {
      icon: 'edit',
      title: '规则管理',
    },
    children: [
      {
        path: '/ruleGroup',
        meta: {
          title: '规则组管理',
        },
        children: [
          {
            path: '/ruleGroup_common',
            meta: {
              title: '公共规则组',
            },
          },
          {
            path: '/ruleGroup_customize',
            meta: {
              title: '自定义规则组',
            },
          },
        ],
      },
      {
        path: '/ruleGroup_feature',
        meta: {
          title: '特征规则',
        },
      },
      {
        path: '/ruleGroup_module',
        meta: {
          title: '检测模块',
        },
      },
      {
        path: '/nameList',
        meta: {
          title: '名单管理',
        },
        children: [
          {
            path: '/ruleGroup_iplist',
            meta: {
              title: 'IP名单',
            },
          },
          {
            path: '/ruleGroup_rulelist',
            meta: {
              title: '自定义名单',
            },
          },
        ],
      },
    ],
  },
  {
    path: '/sysConfig',
    meta: {
      icon: 'setting',
      title: '系统配置',
    },
    children: [
      {
        path: '/sysConfig_options',
        meta: {
          title: '全局配置',
        },
      },
      {
        path: '/sysConfig_others',
        meta: {
          title: '默认配置',
        },
      },
      {
        path: '/sysConfig_auth',
        meta: {
          title: '权限管理',
        },
      },
      {
        path: '/sysConfig_log',
        meta: {
          title: '操作日志',
        },
      },
      {
        path: '/sysConfig_api',
        meta: {
          title: 'API管理',
        },
      },
    ],
  },
]

export default list
