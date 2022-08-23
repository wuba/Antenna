import { UserLayout } from '@/layout/components'
import layouts from '@/layout/index.vue'
const routes = [
    // 异常处理
]

const RouteView = {
    name: 'RouteView',
    render: (h) => h('router-view'),
}

let guest = ['0', '1'],
    admin = ['1']

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
    {
        path: '/',
        name: 'index',
        component: layouts,
        meta: { title: '主页' },
        redirect: '/dashboard',
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                component: () => import('@/views/dashboard/Workplace'),
                meta: {
                    title: '主页',
                    permission: guest,
                    icon: 'dashboard',
                    isExpanded: false,
                },
                children: [
                    {
                        path: '/dashboard/workplace',
                        name: 'Workplace',
                        component: () => import('@/views/dashboard/Workplaced'),
                        meta: {
                            title: '详情页',
                            keepAlive: true,
                            permission: guest,
                            hidden: true,
                        },
                    },
                ],
            },
            {
                path: '/tasklist',
                name: 'tasklist',
                component: () => import('@/views/manage/Task'),
                meta: {
                    title: '任务管理',
                    keepAlive: true,
                    permission: guest,
                    icon: 'table',
                },
            },
            {
                path: '/components',
                name: 'components',
                component: () => import('@/views/manage/Components'),
                meta: {
                    title: '组件管理',
                    keepAlive: true,
                    permission: guest,
                    icon: 'appstore',
                    isExpanded: false,
                },
                children: [
                    {
                        path: 'componentsdetail',
                        name: 'components-detail',
                        component: () => import('@//views/manage/ComponentsDetail'),
                        meta: {
                            title: '详情页',
                            keepAlive: true,
                            permission: guest,
                            hidden: true,
                        },
                    },
                ],
            },
            {
                path: '/message',
                name: 'message',
                component: () => import('@/views/message/Message'),
                meta: {
                    title: '消息列表',
                    keepAlive: true,
                    permission: guest,
                    icon: 'sound',
                },
                // children:[
                //   {
                //     path: '/tasklist/index',
                //     name: 'tasklist',
                //     component: () => import('@/views/dashboard/Workplace'),
                //     meta: { title: '首页', keepAlive: true, permission: [''] }
                //   }
                // ]
            },
            {
                path: '/setting',
                name: 'setting',
                redirect: '/setting/user',
                component: RouteView,
                meta: {
                    title: '系统设置',
                    keepAlive: true,
                    permission: admin,
                    icon: 'setting',
                },
                children: [
                    {
                        path: '/setting/user',
                        name: 'setting-user',
                        component: () => import('@/views/setting/user'),
                        meta: {
                            title: '用户管理',
                            keepAlive: true,
                            permission: admin,
                        },
                    },
                    {
                        path: '/setting/platform',
                        name: 'setting-platform',
                        component: () => import('@/views/setting/platform'),
                        meta: {
                            title: '平台管理',
                            keepAlive: true,
                            permission: admin,
                        },
                    },
                ],
            },
            {
                path: '/open',
                name: 'open-api',
                component: () => import('@/views/open/Interface'),
                meta: {
                    title: 'OpenAPI',
                    keepAlive: true,
                    permission: guest,
                    icon: 'control',
                },
            },
        ],
    },
    {
        path: '/user',
        component: UserLayout,
        redirect: '/user/login',
        hidden: true,
        children: [
            {
                path: 'login',
                name: 'login',
                component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login'),
                meta: {
                    type: 'login',
                },
            },
            {
                path: 'register',
                name: 'register',
                component: () => import(/* webpackChunkName: "user" */ '@/views/user/Register'),
                meta: {
                    type: 'login',
                },
            },
            {
                path: 'register-result',
                name: 'registerResult',
                // component: () => import(/* webpackChunkName: "user" */ '@/views/user/RegisterResult')
            },
            {
                path: 'recover',
                name: 'recover',
                component: undefined,
            },
        ],
    },

    {
        path: '/404',
        component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404'),
    },
    {
        path: '*',
        redirect: '/404',
        hidden: true,
    },
]

export default constantRouterMap
