<template>
    <div>
        <div v-if="$route.name === 'components'">
            <div class="div_card">
                <div class="title clearfix">
                    <div class="left">
                        组件管理
                        <a-tooltip title="组件管理的额外说明">
                            <a-icon type="question-circle" />
                        </a-tooltip>
                    </div>
                    <div class="right">
                        组件加载
                        <a-button shape="circle" @click="addComponet" icon="sync" size="small" />
                    </div>
                </div>
                <div class="content">
                    <a-divider />
                    <p>
                        模板是漏洞辅助验证平台的核心模块，您可以选择列表中的模板进行验证服务的构建。如果您需要新增其他模板，请按照以下的流程进行操作。
                    </p>
                    <a-row>
                        <a-col :span="18" :offset="3" class="wb-m-t-10 wb-m-b-16">
                            <a-steps size="small">
                                <a-step title="查看模板"></a-step>
                                <a-step title="提交模板代码" status="process" />
                                <a-step title="官方审核完成合并代码" status="process" />
                            </a-steps>
                        </a-col>
                    </a-row>
                </div>
            </div>
            <AppPage ref="child" />
        </div>
        <router-view v-else />
    </div>
</template>

<script>
import AppPage from './components/App.vue'
import Driver from 'driver.js'
import Server from '@/utils/service/service.js'
export default {
    components: {
        AppPage,
    },
    data() {
        return {}
    },
    created() {},
    mounted() {
        this.newNav()
    },
    methods: {
        newNav() {
            //新手导航
            let flag = sessionStorage.getItem('firstLogin')
            let out = true
            if (flag == 'true') {
                const driver = new Driver({
                    animate: false,
                    nextBtnText: '下一步',
                    allowClose: false,
                    onDeselected: () => {
                        if (out) {
                            sessionStorage.setItem('firstLogin', 'false')
                        }
                        out = true
                    },
                })
                driver.defineSteps([
                    {
                        element: document.getElementsByClassName('ant-menu-item')[2],
                        popover: {
                            title: '组件管理',
                            description: '通过新建和编辑组件补充平台支持的能力',
                            position: 'right',
                        },
                        showButtons: true,
                        closeBtnText: '跳出',
                        onNext: () => {
                            out = false
                            this.$router.push({ path: '/message' })
                        },
                    },
                    {
                        element: document.getElementsByClassName('ant-menu-item')[3],
                        popover: {
                            title: '消息管理',
                            description: '可以获取所有的组件链接的请求信息',
                            position: 'right',
                        },
                        showButtons: true,
                        closeBtnText: '跳出',
                        onNext: () => {
                            out = false
                            this.$router.push({ path: '/open' })
                        },
                    },
                    {
                        element: document.getElementsByClassName('ant-menu-item')[4],
                        popover: {
                            title: 'OpenAPI',
                            description: '获取Antenna系统通过api调用的接口',
                            position: 'right',
                        },
                        showButtons: true,
                        doneBtnText: '下一步',
                        closeBtnText: '跳出',
                        onNext: () => {
                            out = false
                        },
                    },
                    {
                        element: document.getElementsByClassName('ant-dropdown-link')[0],
                        popover: {
                            title: '个人账户',
                            description: '修改密码、退出系统',
                            position: 'left',
                        },
                        showButtons: true,
                        doneBtnText: '完成',
                        closeBtnText: '跳出',
                        onNext: () => {},
                    },
                ])
                driver.start()
            }
        },
        addComponet() {
            Server.initial_template().then((res) => {
                if (res.code == 1) {
                    this.$refs.child.initData()
                    this.$message('组件加载成功')
                }
            })
        },
    },
}
</script>

<style lang="less" scoped></style>
