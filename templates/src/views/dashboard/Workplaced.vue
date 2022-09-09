<template>
    <div>
        这是首页的 详情页
        <div @click="jump"></div>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    },
    created() {},
    mounted() {},
    methods: {
        jump() {
            // 跳转到首页详情呀
            this.$router.push({ path: '/dashboard/workplace' })
        },
    },
}
</script>

<style scoped></style>
