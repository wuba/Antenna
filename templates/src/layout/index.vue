<template>
    <a-config-provider :locale="locale">
        <a-layout id="components-layout-demo-top-side-2">
            <navbar :collapsed="collapsed" />
            <a-layout>
                <a-layout-header class="header clearfix">
                    <a-row>
                        <a-col :span="1">
                            <a-icon
                                class="trigger"
                                :type="collapsed ? 'menu-unfold' : 'menu-fold'"
                                @click="() => (collapsed = !collapsed)"
                            />
                        </a-col>
                        <a-col :span="10">
                            <Breadcrumb />
                        </a-col>
                        <a-col :span="13" class="textR">
                            <a-space>
                                <img style="width: 20px" src="@/assets/github.png" alt="" />
                                <a-popover>
                                    <template slot="content">
                                        <img src="@/assets/logo.png" alt="" width="80" />
                                    </template>
                                    <img style="width: 20px" src="@/assets/weixin.png" alt="" />
                                </a-popover>
                                <a-divider type="vertical" />
                                <a-dropdown>
                                    <span class="ant-dropdown-link" @click="(e) => e.preventDefault()">
                                        {{ userName }}
                                    </span>
                                    <a-menu slot="overlay">
                                        <a-menu-item>
                                            <a href="javascript:;" @click="modify">修改密码</a>
                                        </a-menu-item>
                                        <a-menu-item>
                                            <a href="javascript:;" @click="logout">退出</a>
                                        </a-menu-item>
                                    </a-menu>
                                </a-dropdown>
                            </a-space>
                        </a-col>
                    </a-row>
                </a-layout-header>
                <a-layout class="mian-contents">
                    <a-layout-content class="main-down">
                        <app-main style="width: 100%" />
                        <div class="bottomTitle">© {{ currentYear }} Copyright {{ currentYear }} 58同城安全</div>
                    </a-layout-content>
                </a-layout>
            </a-layout>
            <ChangePassword :visible="visible" @onClose="close" />
        </a-layout>
    </a-config-provider>
</template>
<script>
import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN'
import { AppMain, Navbar, ChangePassword } from './components'
import Breadcrumb from './components/breadcrumb'
import modeData from '@/utils/modeData'
import Service from '@/utils/service/service'
import Driver from 'driver.js'
import service from '../utils/service/service'

export default {
    name: 'Layout',
    components: {
        AppMain,
        Navbar,
        Breadcrumb,
        ChangePassword,
    },
    data() {
        return {
            collapsed: false,
            locale: zhCN,
            userName: sessionStorage.getItem('username'),
            testData: modeData.testData,
            visible: false,
            // userName: 'wooyaa'
        }
    },
    created() {
        this.getManageNum()
    },
    async mounted() {
        await this.firstLogin()
        this.newNav()
    },
    computed: {
        currentYear() {
            let myDate = new Date()
            return myDate.getFullYear()
        },
        count: function () {
            //不可使用 modeData.testData.num; 会监听不到修改
            return this.testData.num
        },
    },
    methods: {
        newNav() {
            //新手导航
            let flag = sessionStorage.getItem('firstLogin')
            if (flag == 'true') {
                const driver = new Driver({
                    animate: false,
                    allowClose: false,
                })
                let timer = setTimeout(() => {
                    //为什么要有out 因为driver没有退出调用方法
                    let out = true
                    driver.defineSteps([
                        {
                            element: document.getElementsByClassName('ant-menu-item')[1],
                            popover: {
                                title: '任务管理',
                                description: '管理所有的任务，点击查看所有任务',
                                position: 'right',
                            },
                            showButtons: true,
                            doneBtnText: '下一步',
                            closeBtnText: '跳出',
                            onDeselected: () => {
                                if (out) {
                                    sessionStorage.setItem('firstLogin', 'false')
                                }
                            },
                            onNext: () => {
                                out = false
                                this.$router.push({ path: 'tasklist' })
                            },
                        },
                    ])
                    driver.start()
                    clearTimeout(timer)
                }, 10)
            }
        },
        async firstLogin() {
            await service.first_login().then((res) => {
                if (res.data.first_login) {
                    sessionStorage.setItem('firstLogin', 'false')
                } else {
                    sessionStorage.setItem('firstLogin', 'true')
                }
            })
        },
        logout() {
            Service.getLogout().then((res) => {
                if (res.code === 1) {
                    this.$message.success(res.message)
                    sessionStorage.clear()
                    this.$router.push({ name: 'login' })
                } else {
                    this.$message.error(res.message)
                }
            })
        },
        modify() {
            this.visible = true
        },
        close() {
            this.visible = false
        },
        getManageNum() {
            Service.getManage().then((res) => {
                if (res.code === 1) {
                    this.testData.handleNum(res.data.count)
                }
            })
        },
        getMessageDetail() {
            this.$router.push({ name: 'message' })
        },
    },
}
</script>

<style lang="less" scope>
#components-layout-demo-top-side-2 {
    height: 100vh;
    .ant-layout {
        // background: #fff;
    }
    .logo {
        width: 120px;
        height: 31px;
        background: rgba(255, 255, 255, 0.2);
        margin: 16px 28px 16px 0;
        float: left;
    }
    .tabmenus {
        margin-left: 171px;
        line-height: 48px;
    }
    .ant-layout-header {
        height: 48px;
        line-height: 48px;
        padding: 0 30px;
        background-color: #fff;
        z-index: 8;
        box-shadow: 0 1px 4px 0 #0015291f;
    }
    .mian-contents {
        padding: 24px 16px 0 16px;
        overflow: auto;
        .main-down {
            display: flex;
            flex-wrap: wrap;
            .bottomTitle {
                margin-top: 10px;
                height: 50px;
                width: 100%;
                line-height: 50px;
                background: #fff;
                text-align: center;
                align-self: flex-end;
            }
        }
        .ant-layout-footer {
            background-color: #fff;
        }
        .ant-breadcrumb {
            margin: 0;
        }
    }
    .ant-layout-sider {
        z-index: 9;
    }
    .ant-layout-sider-trigger {
        border-top: 1px solid rgb(240, 240, 240);
    }
    .textR {
        text-align: right;
    }
    .textL {
        text-align: left;
    }
}
</style>
