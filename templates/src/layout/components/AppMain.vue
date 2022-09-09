<template>
    <section class="app-main">
        <transition name="fade-transform" mode="out-in">
            <router-view :key="key" />
        </transition>
    </section>
</template>

<script>
export default {
    name: 'AppMain',
    computed: {
        key() {
            return this.$route.path
        },
    },
}
</script>

<style scoped>
/* .app-main {
    min-height: 780px;
} */
</style>
