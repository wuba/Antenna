import axios from './request'
export default {
    all(requests) {
        return axios.all(requests)
    },
    // 登陆
    getLogin(data) {
        return axios.post('/api/v1/auth/user/login/', data)
    },
    // 获取验证码
    getSendmail(data) {
        return axios.post('/api/v1/auth/sendmail/', data)
    },
    // 注册
    getRegister(data) {
        return axios.post('/api/v1/auth/user/register/', data)
    },
    // 忘记密码
    getForgetPassword(data) {
        return axios.post('/api/v1/auth/user/forget_password/', data)
    },
    getLogout(data) {
        return axios.get('/api/v1/auth/user/logout/', data)
    },
    getChangePassword(data) {
        return axios.post('/api/v1/auth/user/change_password/', data)
    },
    getUser(data) {
        return axios.get('/api/v1/auth/user/', data)
    },
    getInvitCode() {
        return axios.get('/api/v1/auth/user/invite_code/')
    },
    getChangeUserStatus(id, data) {
        return axios.pat(`/api/v1/auth/user/${id}/`, data)
    },
    getSendMail(data) {
        return axios.post('/api/v1/auth/sendmail/test/', data)
    },
    getManage(data) {
        return axios.get('/api/v1/messages/manage/', data)
    },
    getManageDelete(data) {
        return axios.del('/api/v1/messages/manage/multiple_delete/', data)
    },
    // openAPI
    getOpenAPI() {
        return axios.get('/api/v1/openapi/key/')
    },
    getRefreshOpenAPI() {
        return axios.get('/api/v1/openapi/key/refresh/')
    },
    getOpenAPIUrl() {
        return axios.get('/api/v1/openapi/key/url_list/')
    },
    // 组件
    getTemplatesManage(data) {
        return axios.get('/api/v1/templates/manage/', data)
    },
    // 系统 平台配置
    getConfigsManage(data) {
        return axios.get('/api/v1/configs/manage/', data)
    },
    getConfigsRenew(data) {
        return axios.post('/api/v1/configs/manage/platform_update/', data)
    },
    getConfigsProtocalUpdate(data) {
        return axios.post('/api/v1/configs/manage/protocal_update/', data)
    },
    // 任务管理
    getTasksManage(data) {
        return axios.get('/api/v1/tasks/manage/', data)
    },
    // 创建缓存任务
    create_tmp_task(data) {
        return axios.get('/api/v1/tasks/manage/create_tmp_task/', data)
    },
    getTasksConfigs(data) {
        return axios.get('/api/v1/tasks/configs/', data)
    },
    cancel_tmp_task(data) {
        return axios.post('/api/v1/tasks/manage/cancel_tmp_task/', data)
    },
    getTemplatessConfigs(data) {
        return axios.get('/api/v1/templates/configs/', data)
    },
    getTasksManageStatus(data) {
        return axios.post('/api/v1/tasks/manage/multi_update_status/', data)
    },
    getTasksManageDele(data) {
        return axios.del('/api/v1/tasks/manage/multiple_delete/', data)
    },
    getTasksManageEdit(id, data) {
        return axios.pat(`/api/v1/tasks/manage/${id}/`, data)
    },
    getTasksConfigsDel(id) {
        return axios.del(`/api/v1/tasks/configs/delete_config/?id=${id}`)
    },
    tmp_delete_config(id) {
        return axios.del(`/api/v1/tasks/tmp/delete_config/?id=${id}`)
    },
    getTasksConfigsAdd(data) {
        return axios.post('/api/v1/tasks/configs/', data)
    },
    tasks_tmp(data) {
        return axios.post('/api/v1/tasks/configs/', data)
    },
    getTasksConfigsUpdate(data) {
        return axios.post('/api/v1/tasks/configs/update_config/', data)
    },
    tmp_update_config(data) {
        return axios.post('/api/v1/tasks/tmp/update_config/', data)
    },
    getCreatTask(data) {
        return axios.post('/api/v1/tasks/manage/create_task/', data)
    },
    // 主页
    getDashboard(data) {
        return axios.get('/api/v1/messages/manage/dashboard/', data)
    },
    // 邀请码
    getOpenInvite() {
        return axios.get('/api/v1/configs/manage/open_invite/')
    },
    // 是否为第一次登录
    first_login() {
        return axios.get('/api/v1/auth/user/first_login/')
    },
    templatesManage(data) {
        return axios.post('/api/v1/templates/manage/', data)
    },
    delete_template(data) {
        return axios.post('/api/v1/templates/manage/delete_template/', data)
    },
    template_info(data) {
        return axios.get('/api/v1/templates/manage/template_info/', data)
    },
    update_template(data) {
        return axios.post('/api/v1/templates/manage/update_template/', data)
    },
    //重启平台
    platform_restart(data) {
        return axios.get('/api/v1/configs/manage/platform_restart/', data)
    },
    //重启平台
    initial_template(data) {
        return axios.get('/api/v1/templates/manage/initial_template/', data)
    },
    //获取linkList
    linkList(data) {
        return axios.get('/api/v1/templates/url/', data)
    },
    //获取dns解析配置
    get_dns(data) {
        return axios.get('/api/v1/configs/dns/', data)
    },
    //修改dns解析配置
    dns_update(data) {
        return axios.post('/api/v1/configs/dns/dns_update/', data)
    },
    //删除dns解析配置
    dns_delete(data) {
        return axios.del('/api/v1/configs/dns/dns_delete/', data)
    },
}
