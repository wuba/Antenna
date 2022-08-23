<template>
    <div id="userLayout" :class="['user-layout-wrapper']">
        <div class="container">
            <div class="user-layout-content">
                <img src="" alt="" />
                <router-view />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UserLayout',
    components: {},
    mounted() {},
}
</script>

<style lang="less" scoped>
#userLayout.user-layout-wrapper {
    height: 100%;
    .imgTop {
        width: 758px;
        height: 513px;
        position: absolute;
        top: 0;
        right: 0;
    }
    .imgBootom {
        position: absolute;
        width: 550px;
        height: 333px;
        left: 2%;
        bottom: 0;
    }
    .container {
        background-color: #f6f8fe;
        width: 100%;
        height: 100%;
        background: url(~@/assets/bgtu.png) no-repeat;
        background-size: 100% 100%;
        position: relative;

        .user-layout-content {
            position: relative;
            height: 100%;

            .main {
                min-width: 260px;
                width: 368px;
                margin: 0 auto;
            }

            .footer {
                position: absolute;
                width: 100%;
                bottom: 0;
                padding: 0 16px;
                margin: 48px 0 24px;
                text-align: center;

                .links {
                    margin-bottom: 8px;
                    font-size: 14px;
                    a {
                        color: rgba(0, 0, 0, 0.45);
                        transition: all 0.3s;
                        &:not(:last-child) {
                            margin-right: 40px;
                        }
                    }
                }
                .copyright {
                    color: rgba(0, 0, 0, 0.45);
                    font-size: 14px;
                }
            }
        }

        a {
            text-decoration: none;
        }
    }
}
</style>
