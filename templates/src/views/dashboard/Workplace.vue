<template>
    <div>
        <div class="bigContainer">
            <div class="waiContainer">
                <div class="container messageCount">
                    <h4 class="title">基础数据</h4>
                    <ul class="ulContainer">
                        <li v-for="(it, d) in basicDataList" :key="d" @click="jumpDetail(it)">
                            <div>{{ it.title }}</div>
                            <div style="font-size: 20px">{{ it.total }}</div>
                            <div>
                                今日更新
                                <span style="color: red">+{{ it.newTotal }}</span>
                            </div>
                        </li>
                    </ul>
                </div>
                <div class="baseCount container" id="echartsW">
                    <h4 class="title">消息统计</h4>
                    <div style="height: 300px; text-align: center" :style="{ width: widthVal }">
                        <VueWcharts :options="lineOptions"></VueWcharts>
                    </div>
                </div>
            </div>

            <div class="container zujian">
                <h4 class="title">组件链接</h4>
                <div class="tabsContain">
                    <a-tabs default-active-key="1" @change="tabChange" v-show="dataContent.length > 1">
                        <a-tab-pane v-for="(item, index) in dataContent" :key="index">
                            <template slot="tab">第{{ index + 1 }}页</template>
                        </a-tab-pane>
                    </a-tabs>
                </div>
                <div class="zsContain" v-for="(item, index) in dataContent[count]" :key="index">
                    <div class="overflow leftbutton" style="color: rgb(138, 226, 223)">
                        {{ item[Object.keys(item)[0]] }}
                    </div>

                    <div class="overflow leftbutton">
                        <a-tooltip>
                            <template slot="title">{{ Object.keys(item)[1] }}</template>
                            {{ Object.keys(item)[1] }}
                        </a-tooltip>
                    </div>
                    <a-input :value="item[Object.keys(item)[1]]" placeholder="请输入域名" :readOnly="true">
                        <my-copy slot="suffix" :text="item[Object.keys(item)[1]]"></my-copy>
                    </a-input>
                </div>
            </div>
        </div>
        <div class="container" style="margin-top: 10px">
            <h4 class="title">
                最新消息
                <a-icon
                    type="reload"
                    :class="[state ? 'g' : '']"
                    style="color: blue; cursor: pointer"
                    @click="initData"
                />
            </h4>
            <a-table
                :columns="columns"
                :data-source="data"
                rowKey="id"
                :loading="messageLoading"
                :expandedRowKeys.sync="expandedRowKeys"
                :pagination="false"
            >
                <span slot="message_type" slot-scope="text">{{ text }}</span>
                <span slot="create_at" slot-scope="text">{{ text | wuba_dateformat }}</span>
                <div slot="expandedRowRender" slot-scope="tags">
                    <p v-if="tags.header">header: {{ tags.header }}</p>
                    <p v-if="tags.content">content: {{ tags.content }}</p>
                    <p v-if="tags.uri">uri: {{ tags.uri }}</p>
                    <a-divider v-show="tags.html" />
                    <p v-show="tags.html" v-for="(item, key) in tags.html.split('\n')" :key="key">{{ item }}</p>
                </div>
            </a-table>
        </div>
    </div>
</template>
<script>
import MyCopy from '@/components/copy.vue'
import VueWcharts from '@dpdfe/wcharts-vue'
import Service from '@/utils/service/service'
export default {
    data() {
        return {
            widthVal: document.body.clientWidth * 0.44 + 'px',
            loading1: false,
            color: ['#32c5d2', '#0d6aaa', '#f6b02c', '#ee5e6b'],
            basicDataList: [
                {
                    name: 'message_count',
                    newName: 'today_message_count',
                    title: '消息总数',
                    path: '/message',
                    total: 0,
                    newTotal: 0,
                },
                {
                    name: 'task_count',
                    newName: 'today_task_count',
                    path: '/tasklist',
                    title: '任务总数',
                    total: 0,
                    newTotal: 0,
                },
                {
                    name: 'template_count',
                    newName: 'today_template_count',
                    path: '/components',
                    title: '组件统计',
                    total: 0,
                    newTotal: 0,
                },
            ],
            echartRadioValue: 'a',
            columns: [
                { title: '域名', dataIndex: 'domain', key: 'domain' },
                { title: '远程请求地址', dataIndex: 'remote_addr', key: 'remote_addr' },
                {
                    title: '消息类型',
                    dataIndex: 'message_type',
                    key: 'message_type',
                    scopedSlots: { customRender: 'message_type' },
                },
                { title: '所属任务', dataIndex: 'task_name', key: 'task_name' },
                {
                    title: '请求时间',
                    dataIndex: 'create_time',
                    key: 'create_time',
                    scopedSlots: { customRender: 'create_at' },
                },
            ],
            data: [],
            messageLoading: false,
            expandedRowKeys: [],
            lineOptions: {
                grid: {
                    left: 20,
                    right: 30,
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        axisLine: {
                            show: true,
                        },
                        data: [],
                    },
                ],
                yAxis: [
                    {
                        gridIndex: 0,
                        splitLine: {
                            show: true,
                        },
                    },
                ],
                series: [
                    {
                        name: '消息统计',
                        type: 'line',
                        smooth: 0.4,
                        data: [],
                        areaStyle: {},
                    },
                ],
            },
            dataContent: [],
            count: 0,
            state: false,
        }
    },
    components: {
        VueWcharts,
        MyCopy,
    },
    created() {
        this.initData()
    },
    mounted() {},

    methods: {
        initData() {
            this.state = true

            Service.getDashboard().then((res) => {
                if (res.code === 1) {
                    let { data } = res
                    this.lineOptions.xAxis[0].data = data.message_date_count.list_day
                    this.lineOptions.series[0].data = data.message_date_count.message_count

                    this.data = data.last_message_list

                    for (let i = 0; i < 3; i++) {
                        let name = this.basicDataList[i].name
                        if (data[name]) {
                            this.basicDataList[i].total = data[name]
                            this.basicDataList[i].newTotal = data[this.basicDataList[i].newName]
                        }
                    }
                    let dashboardLength =
                        Math.ceil(data.dashboard_url.length / 10) > 3 ? 3 : Math.ceil(data.dashboard_url.length / 10)
                    for (let i = 0; i < dashboardLength; i++) {
                        this.dataContent[i] = data.dashboard_url.slice(i * 10, i * 10 + 10)
                    }
                    setTimeout(() => {
                        this.state = false
                    }, 1000)
                } else {
                    this.$message.error(res.message)
                }
            })
        },
        tabChange(e) {
            this.count = Number(e)
        },
        jumpDetail(data) {
            this.$router.push({ path: data.path })
        },
    },
}
</script>

<style lang="less" scoped>
.g {
    transform: rotate(360deg);
    transition: all 1s;
}
.container {
    border-radius: 8px;
    padding: 20px;
    background-color: #fff;
}
.title {
    border-bottom: 1px solid #f6f6f6;
    padding-bottom: 5px;
    width: 100%;
}
.bigContainer {
    display: flex;
    flex-wrap: wrap;
    height: 500px;
    overflow: hidden;
    .baseCount {
        width: 100%;
        margin-top: 10px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    .waiContainer {
        width: 55%;
    }
    .zujian {
        margin-left: 1%;
        width: 44%;
        position: relative;
        .tabsContain {
            position: absolute;
            right: 0;
            top: 3px;
        }
        /deep/ .ant-tabs-nav {
            float: right !important;
        }
        .zsContain {
            display: flex;
            margin-top: 10px;
            .leftbutton {
                text-align: center;
                margin-right: 10px;
                background-color: #eef8fe;
                width: 82px;
                color: rgba(3, 100, 255, 1);
                border-radius: 8px;
                line-height: 32px;
                padding-left: 3px;
            }
        }
    }
    .messageCount {
        .ulContainer {
            display: flex;
            padding: 0;
            li {
                display: flex;
                flex-wrap: wrap;
                flex-grow: 1;
                border-right: 1px solid #f6f6f6;
                justify-content: center;
                div {
                    width: 100%;
                    text-align: center;
                }
            }
            li:last-child {
                border: none;
            }
        }
    }
}

.overflow {
    overflow: hidden;
    box-sizing: border-box;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
