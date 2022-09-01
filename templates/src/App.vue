<template>
    <div id="app">
        <router-view />
    </div>
</template>
<script>
export default {
    data() {
        return {
            collapsed: false,
        }
    },
    created() {},
    mounted() {},
}
</script>

<style lang="less">
#app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
.driver-next-btn {
    display: block !important;
    font-size: 14px !important;
}
.driver-prev-btn {
    display: none !important;
}
.driver-popover-footer {
    border-top: 1px solid #eaeaea;
    padding-top: 10px;
}
.driver-close-btn {
    position: absolute;
    left: 10px;
    border: none !important;
    background-color: #fff !important;
    color: #6eb0c7 !important;
    font-size: 14px !important;
}
</style>
