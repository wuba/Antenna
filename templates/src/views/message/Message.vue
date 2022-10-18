<template>
    <div>
        <div class="div_card">
            <div class="title clearfix">
                <div class="left">最新消息</div>
            </div>
            <div class="content">
                <a-row :gutter="2" class="search-area">
                    <a-col :span="16">
                        <a-button type="danger" icon="delete" size="small" @click="deleteEvent()">删除</a-button>
                        <a-button type="primary" class="wb-m-l-10" icon="reload" size="small" @click="onSearch()">
                            刷新
                        </a-button>
                    </a-col>
                    <a-col :span="8">
                        <a-input-search
                            placeholder="输入关键字搜索"
                            allow-clear
                            @search="onSearch"
                            v-model="searchTableValue"
                        />
                    </a-col>
                </a-row>
                <a-table
                    :columns="columns"
                    :data-source="data"
                    rowKey="id"
                    :pagination="pagination"
                    :loading="messageLoading"
                    :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
                    @change="handleTableChange"
                >
                    <span slot="action" slot-scope="text">
                        <a class="wb-m-l-5" @click.stop="deleteEvent(text.id)">删除</a>
                    </span>
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
    </div>
</template>

<script>
import modeData from '@/utils/modeData'
import Service from '@/utils/service/service'
export default {
    data() {
        return {
            testData: modeData.testData,
            columns: [
                { title: '域名', dataIndex: 'domain', key: 'domain' },
                { title: '远程请求地址', dataIndex: 'remote_addr', key: 'remote_addr' },
                {
                    title: '消息类型',
                    dataIndex: 'message_type',
                    key: 'message_type',
                    scopedSlots: { customRender: 'message_type' },
                    filterMultiple: false,
                    filters: [
                        {
                            text: 'http',
                            value: 1,
                        },
                        {
                            text: 'dns',
                            value: 2,
                        },
                        {
                            text: 'ldap',
                            value: 3,
                        },
                        {
                            text: 'rmi',
                            value: 4,
                        },
                    ],
                },
                { title: '所属任务', dataIndex: 'task_name', key: 'task_name' },
                {
                    title: '请求时间',
                    dataIndex: 'create_time',
                    key: 'create_time',
                    scopedSlots: { customRender: 'create_at' },
                },
                // { title: '更新时间', dataIndex: 'updata_time', key: 'updata_time' },
                { title: '操作', key: 'action', scopedSlots: { customRender: 'action' } },
            ],
            data: [],
            pagination: {
                pageSizeOptions: ['10', '20', '30', '40', '50'],
                showSizeChanger: true,
                pageSize: 10,
            },
            messageLoading: false,
            selectedRowKeys: [],
            searchTableValue: '',
        }
    },
    created() {
        this.initData()
        this.testData.handleNum(0)
    },
    watch: {
        $route: {
            handler: function () {
                this.initData()
            },
            // 深度观察监听
            deep: true,
            timer: null,
        },
    },
    mounted() {},
    methods: {
        changeNum() {
            this.testData.handleNum(0)
        },
        initData(params = {}) {
            this.messageLoading = true
            let data = {
                page_size: this.pagination.pageSize,
                search: this.searchTableValue,
                page: 1,
                task: this.$route.query.id,
                ...params,
            }
            if (data.page === 1) {
                this.pagination.current = 1
            }
            Service.getManage(data).then((res) => {
                this.messageLoading = false
                if (res.code === 1) {
                    let { data } = res
                    const pagination = { ...this.pagination }
                    pagination.total = data.count
                    this.pagination = pagination
                    this.data = data.results
                } else {
                    this.$message.error(res.message)
                }
            })
        },
        handleTableChange(pagination, filters, sorter) {
            // console.log(filters['message_type'], filters)
            const pager = { ...this.pagination }
            pager.current = pagination.current
            pager.pageSize = pagination.pageSize
            this.pagination = pager
            let data = {
                page_size: pagination.pageSize,
                page: pagination.current,
            }
            if (filters['message_type'] && filters['message_type'].length) {
                data.message_type = filters['message_type'][0]
            }
            this.initData(data)
        },
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
        },
        onSearch() {
            this.initData()
        },
        deleteEvent(id = '') {
            let _this = this
            if (id) {
                this.$confirm({
                    title: '提示',
                    content: '确认删除',
                    onOk() {
                        _this.deleteEventReq(id)
                    },
                    onCancel() {},
                })
            } else {
                if (this.selectedRowKeys.length === 0) return this.$message.error('未选择任何数据')
                const NUM = this.selectedRowKeys.join(',')
                this.$confirm({
                    title: '提示',
                    content: '确认删除选中的数据',
                    onOk() {
                        _this.deleteEventReq(NUM)
                    },
                    onCancel() {},
                })
            }
        },
        deleteEventReq(id) {
            Service.getManageDelete({ id }).then(
                (res) => {
                    if (res.code === 1) {
                        this.$message.success('操作成功')
                        this.initData()
                    } else {
                        this.$message.error(res.message)
                    }
                    // console.log(res, '删除成功')
                },
                (err) => {
                    // console.log(err, '删除失败')
                }
            )
        },
    },
}
</script>

<style scoped>
.search-area {
    margin-bottom: 5px;
    line-height: 32px;
}
</style>
