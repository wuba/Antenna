<template>
    <div>
        <div class="div_card">
            <div class="title clearfix">
                <div class="left">
                    {{ $route.query.title }}
                </div>
            </div>
            <div class="content">
                简介
                <a-divider />
                使用方法
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    },
    created() {
        this.$route.meta.title = this.$route.query.title
    },
    mounted() {
        console.log('获取参数', this.$route)
        // this.$route.meta.title = this.$route.query.title
    },
    methods: {},
}
</script>

<style lang="less" scoped></style>
