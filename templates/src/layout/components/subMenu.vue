<template functional>
    <a-sub-menu :key="props.currentRoute.path">
        <span slot="title" class="menu-title">
            <a-icon :type="props.currentRoute.meta.icon" v-if="props.currentRoute.meta.icon" />
            <span v-if="props.currentRoute.meta">
                {{ props.currentRoute.meta.title }}
            </span>
        </span>
        <template v-for="item in props.currentRoute.children">
            <a-menu-item v-if="!item.children && !item.meta.hidden" :key="item.path">
                <router-link :to="item.path">
                    {{ item.meta.title }}
                </router-link>
            </a-menu-item>
            <sub-menu v-else-if="item.children" :key="item.path" :currentRoute="item" />
        </template>
    </a-sub-menu>
</template>

<script>
// import menuItem from './menuItem';
export default {
    name: 'subMenu',
    // components: { menuItem },
    props: {
        currentRoute: {
            type: Object,
            required: true,
        },
    },
    created() {
        console.log(this.currentRoute, 'naoda')
    },
}
</script>
