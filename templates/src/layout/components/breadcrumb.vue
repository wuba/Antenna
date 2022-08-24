<template>
    <a-breadcrumb :routes="routes" class="breadcrumb_div">
        <template slot="itemRender" slot-scope="{ route, params, routes, paths }">
            <span v-if="routes.indexOf(route) === routes.length - 1">
                {{ route.meta.title }}
            </span>
            <!-- <router-link v-else :to="paths.join('/')"> -->
            <router-link v-else :to="route.redirect ? route.redirect : route.path">
                <!-- {{ paths }} -->
                {{ route.meta.title }}
            </router-link>
        </template>
    </a-breadcrumb>
</template>

<script>
export default {
    data() {
        return {
            routes: [
                {
                    path: '/dashboard/workplace',
                    breadcrumbName: 'home',
                },
                {
                    path: 'first',
                    breadcrumbName: 'first',
                },
                {
                    path: 'second',
                    breadcrumbName: 'second',
                },
            ],
        }
    },
    watch: {
        $route(to, from) {
            this.getBreadcrumb()
        },
    },
    created() {
        this.getBreadcrumb()
    },
    mounted() {},
    methods: {
        isHome(route) {
            return route.name === 'dashboard'
        },
        getBreadcrumb() {
            let matched = [...this.$route.matched]
            // console.log(matched, '---')
            if (matched[1].name === 'dashboard') {
                matched.splice(1, 1)
            }
            // 如果不是首页
            // if (!this.isHome(matched[1])) {
            //   matched = [{ path: "/dashboard", meta: { title: "首页" } }].concat(matched);
            // }
            // matched.splice(0,1)
            this.routes = matched
        },
    },
}
</script>

<style scoped>
.breadcrumb_div {
    line-height: 48px;
}
</style>
