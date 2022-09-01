import Vue from 'vue'
import {
    Alert,
    Avatar,
    Badge,
    Breadcrumb,
    Button,
    Card,
    Col,
    ConfigProvider,
    Divider,
    Dropdown,
    Form,
    FormModel,
    Icon,
    Input,
    InputNumber,
    Layout,
    List,
    LocaleProvider,
    message,
    Menu,
    Modal,
    notification,
    Pagination,
    Popconfirm,
    Popover,
    Row,
    Select,
    Steps,
    Switch,
    Table,
    Tabs,
    Tag,
    Tooltip,
    Drawer,
    Result,
    PageHeader,
    Space,
    Upload,
    Radio,
} from 'ant-design-vue'
import 'driver.js/dist/driver.min.css'

import 'ant-design-vue/dist/antd.css'
import App from './App.vue'

import './style/global.less' // global style
import router from './router'

import filters from './utils/filters'

Object.keys(filters).forEach((k) => Vue.filter(k, filters[k]))

Vue.use(Alert)
    .use(Avatar)
    .use(Badge)
    .use(Breadcrumb)
    .use(Button)
    .use(Card)
    .use(Col)
    .use(ConfigProvider)
    .use(Divider)
    .use(Dropdown)
    .use(Form)
    .use(FormModel)
    .use(Icon)
    .use(Input)
    .use(InputNumber)
    .use(Layout)
    .use(List)
    .use(LocaleProvider)
    .use(message)
    .use(Menu)
    .use(Modal)
    .use(notification)
    .use(Pagination)
    .use(Popconfirm)
    .use(Popover)
    .use(Row)
    .use(Select)
    .use(Steps)
    .use(Switch)
    .use(Table)
    .use(Tag)
    .use(Tooltip)
    .use(Drawer)
    .use(Result)
    .use(PageHeader)
    .use(Space)
    .use(Tabs)
    .use(Upload)
    .use(Radio)

Vue.config.productionTip = false
Vue.prototype.$message = message

Vue.prototype.$notification = notification
Vue.prototype.$confirm = Modal.confirm

new Vue({
    router,
    render: (h) => h(App),
}).$mount('#app')
