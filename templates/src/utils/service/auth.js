import axios from 'axios'

const userApi = {
    Login: '/api/auth/login/',
    GetInfo: '/api/auth/user/info/',
    Auth: '/api/auth/user/info/?platform_code=WAF',
}

const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API_AUTH,
})

function get(url, params) {
    return service({
        method: 'get',
        url: url,
        params: params,
    })
        .then(function (response) {
            return response
        })
        .catch(function (error) {
            if (error.response) {
                // console.log(error.response.data);
                // console.log(error.response.status);
                // console.log(error.response.headers);
            } else if (error.request) {
                console.log(error.request)
            } else {
                console.log('Error', error.message)
            }
            // console.log(error.config);
            return error
        })
}

export default {
    all(requests) {
        return axios.all(requests)
    },
    login(params) {
        return service({
            method: 'POST',
            url: userApi.Login,
            data: params,
        })
    },
    getInfo(params) {
        return get(userApi.GetInfo, params)
    },
    getAuth() {
        // return get(userApi.Auth)
        return service({
            method: 'GET',
            url: userApi.Auth,
            headers: {
                Authorization: sessionStorage.getItem('token'),
            },
        })
    },
}
