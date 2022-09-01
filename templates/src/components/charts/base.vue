<template>
    <div :class="className" :id="id" :style="{ height: height, width: width }"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
    props: {
        className: {
            type: String,
            default: 'chart',
        },
        id: {
            type: String,
            default: 'chart',
        },
        width: {
            type: String,
            default: '100',
        },
        height: {
            type: String,
            default: '100%',
        },
        options: {
            type: Object,
            default: () => {
                return {
                    title: {
                        text: 'ECharts 入门示例',
                    },
                    tooltip: {},
                    xAxis: {
                        data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
                    },
                    yAxis: {},
                    series: [
                        {
                            name: '销量',
                            type: 'bar',
                            data: [5, 20, 36, 10, 10, 20],
                        },
                    ],
                }
            },
        },
    },
    data() {
        return {
            chart: null,
        }
    },
    watch: {
        options: {
            deep: true,
            handler: function () {
                this.initChart()
            },
        },
    },
    mounted() {},
    beforeDestroy() {
        if (!this.chart) {
            return
        }
        this.chart.dispose()
        this.chart = null
    },
    methods: {
        initChart() {
            this.chart = echarts.init(document.getElementById(this.id))
            this.chart.clear() //先clear在重绘，才可以真正重绘
            this.chart.setOption(this.options)
        },
    },
}
</script>
