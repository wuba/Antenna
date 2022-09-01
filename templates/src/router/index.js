import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './list'
import NProgress from 'nprogress'
import { notification } from 'ant-design-vue'

const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch((err) => err)
}

Vue.use(VueRouter)

const router = new VueRouter({
    routes,
})

router.beforeEach((to, from, next) => {
    NProgress.start()

    const token = sessionStorage.getItem('token')
    if (token) {
        //判断本地是否存在access_token
        let role = to.meta.permission
        if (role) {
            let i = role.indexOf(sessionStorage.getItem('role'))
            if (i > -1) {
                next()
            } else {
                notification.error({
                    message: 'err',
                    description: '没有权限',
                })
                router.push({ path: '/dashboard' })
                next()
            }
        } else {
            next()
        }
    } else {
        if (to.meta.type === 'login') {
            next()
        } else {
            next({
                path: 'user/login',
            })
        }
    }
    if (to.meta.type === 'login') {
        if (token) {
            next({
                path: from.fullPath,
            })
        } else {
            next()
        }
    }

    /* has token */
    // if (to.meta.type === 'login') {
    //   next();
    // } else {
    //   // 判断是否存在token
    //   const token = sessionStorage.getItem('token');
    //   if (!token) {
    //     // 跳转到登录页
    //     router.push({name: 'login'});
    //     // 提示
    //     return;
    //   }
    // }

    /* 路由发生变化修改页面title */
    if (to.meta.title) {
        document.title = to.meta.title
    }
    next()
})

router.afterEach(() => {
    NProgress.done()
})
export default router
