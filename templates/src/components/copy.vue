<template>
    <a-tooltip slot="suffix" :title="copyTitle">
        <a-icon :type="copyIcon" class="copy" @click="copyEvent(text)" @mouseleave="copyMouseleave" />
    </a-tooltip>
</template>

<script>
import { copyText } from '@/utils/tools'
export default {
    data() {
        return {
            copyIcon: 'copy',
            copyTitle: '复制到剪贴板',
        }
    },
    props: {
        text: '',
    },
    methods: {
        copyEvent(txt) {
            let _this = this
            copyText(txt, function () {
                _this.copyIcon = 'check'
                _this.copyTitle = '复制成功'
            })
        },
        copyMouseleave() {
            if (this.copyIcon === 'check') {
                this.copyIcon = 'copy'
            }
        },
    },
}
</script>

<style scoped>
.copy {
    color: rgba(0, 0, 0, 0.45);
}
.anticon-check {
    color: #52c41a;
}
</style>
