<template>
    <a-layout-sider collapsible v-model="collapsed" width="208px" :trigger="null">
        <div class="imgContainer">
            <img class="titleImg" src="@/assets/logo.png" alt="" />
            <div class="title">Antenna</div>
        </div>
        <a-menu
            mode="inline"
            class="my-navbar"
            :open-keys="openKeys"
            :selectedKeys="selectedKeys"
            @openChange="changeOpen"
        >
            <template v-for="(item, index) in baseRoute">
                <a-menu-item v-if="!item.redirect" :key="item.path" @click="jump(item.path)">
                    <!-- <router-link :to="item.path"> <a-icon :type="item.meta.icon" v-if="item.meta.icon"/> {{ item.meta.title }}</router-link> -->
                    <a-icon :type="item.meta.icon" />
                    <!-- <span><router-link :to="item.path" class="a_inline">{{ item.meta.title }}</router-link></span> -->
                    <span>{{ item.meta.title }}</span>
                </a-menu-item>
                <SubMenu v-else :key="index" :currentRoute="item" />
            </template>
        </a-menu>
    </a-layout-sider>
</template>

<script>
import baseRoute1 from '@/router/list'
import SubMenu from './subMenu.vue'
export default {
    components: {
        SubMenu,
    },
    props: {
        collapsed: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            baseRoute: [],
            openKeys: [],
            selectedKeys: [],
            rootSubmenuKeys: [],
        }
    },
    watch: {
        $route: function (n, o) {
            this.getopenKeys()
        },
    },
    created() {
        this.getRootSubmenu()
        this.getopenKeys()
        this.baseRoute = this.getRouter()
    },
    mounted() {},
    methods: {
        getopenKeys() {
            let matched = [...this.$route.matched]
            matched.splice(0, 1)
            this.selectedKeys = []
            if (matched.length > 1) {
                let len = matched.length - 1,
                    len1 = matched.length - 2
                if (!matched[len1].redirect) {
                    this.selectedKeys.push(matched[len1].path)
                } else {
                    this.selectedKeys.push(this.$route.path)
                }
                for (let i = 0; i < len; i++) {
                    this.openKeys.push(matched[i].path)
                }
            } else {
                this.selectedKeys.push(this.$route.path)
            }
        },
        getRootSubmenu() {
            let len = this.baseRoute.length
            for (let i = 0; i < len; i++) {
                this.rootSubmenuKeys.push(this.baseRoute[i].path)
            }
        },
        changeOpen(openKeys) {
            const latestOpenKey = openKeys.find((key) => this.openKeys.indexOf(key) === -1)
            if (this.rootSubmenuKeys.indexOf(latestOpenKey) === -1) {
                this.openKeys = openKeys
            } else {
                this.openKeys = latestOpenKey ? [latestOpenKey] : []
            }
        },
        jump(path) {
            this.$router.push({ path: path })
        },
        getRouter() {
            let data = baseRoute1[0].children
            let role = sessionStorage.getItem('role')
            for (let i = 0; i < data.length; i++) {
                let arr = data[i].meta.permission
                if (arr.indexOf(role) === -1) {
                    data.splice(i, 1)
                    i--
                }
            }
            return data
        },
    },
}
</script>

<style lang="less" scoped>
.my-navbar {
    height: 90%;
    border-right: 0;
    overflow-y: auto;
    overflow-x: hidden;
}
.imgContainer {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    .title {
        margin-left: 10px;
        font-size: 23px;
        margin-top: 18px;
        font-weight: 600;
    }
    .titleImg {
        width: 40px;
    }
}

a.a_inline {
    display: inline-block;
}
.ant-layout-sider {
    background-color: #ffffff !important;
}
.ant-menu-inline .ant-menu-item,
.ant-menu-inline .ant-menu-submenu-title {
    width: calc(100% + 0px);
}

.ant-pro-sider-menu-logo {
    position: relative;
    height: 48px;
    overflow: hidden;
    -webkit-transition: all 0.3s;
    transition: all 0.3s;
    line-height: 48px;
    background-image: url('~@/assets/logo.png');
    background-size: 24px;
    // background-position: 16px;
    background-repeat: no-repeat;
    padding-left: 32px;
    h1 {
        color: #ffffff;
        font-size: 20px;
        padding: 0 10px;
        margin: 0 0 0 12px;
        font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
        font-weight: 600;
        vertical-align: middle;
    }
}

.ant-pro-sider-menu-logo.t {
    background-position: 30px;
}

.ant-pro-sider-menu-logo.f {
    background-position: 16px;
}
</style>
