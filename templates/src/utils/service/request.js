import axios from 'axios'
import { notification } from 'ant-design-vue'
import router from '@/router/index'

// create an axios instance
const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
    //baseURL: '/api', // url = base url + request url
    // withCredentials: true, // send cookies when cross-domain requests
    // timeout: 5000, // request timeout
    // headers:{
    //   'Authorization': 'Token 98f8c60bfc4683524ae2927162ec5ee6d97fbc1c',
    // }
    // withCredentials: true //
})

// 异常拦截处理器
const errorHandler = (error) => {
    // console.log('error - 异常拦截处理器', error, error.response)
    let { response } = error
    if (response.status === 401) {
        notification.error({
            message: 'err',
            description: 'token过期,登录态失效,即将跳到登陆',
        })
        sessionStorage.clear()
        setTimeout(() => {
            router.push({ name: 'login' })
        }, 2000)
        return
    }
    if (response.data.message) {
        notification.error({
            message: 'err',
            description: response.data.message,
        })
    } else {
        notification.error({
            message: 'err',
            description: `${response.status} ${response.statusText} 请稍后再试`,
        })
    }
    return Promise.reject()
    // return
}

// request interceptor
service.interceptors.request.use((config) => {
    let t = sessionStorage.getItem('token')
    if (t) {
        config.headers.Authorization = `Token ${t}`
    }
    return config
}, errorHandler)

// response interceptor
service.interceptors.response.use((response) => {
    const res = response.data
    return res
}, errorHandler)

export default {
    all(requests) {
        return axios.all(requests)
    },
    post(url, data) {
        return service({
            method: 'POST',
            url: url,
            data: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
            // responseType: 'json',
            // responseEncoding: 'utf8',
            // transformResponse: [function (data) {
            //     return data;
            // }],
        })
    },
    pat(url, data) {
        return service({
            method: 'patch',
            url: url,
            data: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
    },
    put(url, data) {
        return service({
            method: 'PUT',
            url: url,
            data: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
    },
    get(url, params) {
        return service({
            method: 'get',
            url: url,
            params: params,
            // responseType: 'json',
            // responseEncoding: 'utf8',
            // transformResponse: [function (data) {
            //     return data
            // }],
        })
    },
    del(url, params) {
        return service({
            method: 'delete',
            url: url,
            params: params, // 请求参数拼接在url上
            // data: {}  // 请求参数放在请求体
        })
    },
}
