<template>
    <div>
        <div class="div_card">
            <div class="title clearfix">
                <div class="left">最新任务</div>
            </div>
            <div class="content">
                <a-row :gutter="2" class="search-area">
                    <a-col :span="19">
                        <a-button type="primary" icon="plus-circle" class="wb-m-r-5" size="small" @click="addEvent">
                            新建
                        </a-button>
                        <a-button
                            type="primary"
                            icon="check-circle"
                            class="wb-m-r-5"
                            size="small"
                            @click="enableEvent(true)"
                        >
                            启用
                        </a-button>
                        <a-button
                            type="primary"
                            icon="minus-circle"
                            class="wb-m-r-5"
                            size="small"
                            @click="enableEvent(false)"
                        >
                            禁用
                        </a-button>
                        <a-button type="danger" icon="delete" size="small" @click="deleteEvent()">删除</a-button>
                    </a-col>
                    <a-col :span="5">
                        <a-input-search
                            placeholder="输入关键字搜索任务名"
                            @search="onSearch"
                            v-model="searchValue"
                            allowClear
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
                    <a slot="name" slot-scope="text" @click.stop="editEvent(text)">
                        <a-popover>
                            <template slot="content">点击查看详情</template>
                        </a-popover>
                        <div class="topTip">{{ text.name }}</div>
                    </a>
                    <a slot="message_counts" slot-scope="text" @click.stop="jumpEvent(text)">
                        {{ text.message_counts }}
                    </a>
                    <span slot="status" slot-scope="text">
                        <a-switch v-model="text.status" @click="changeStatus($event, text)" />
                    </span>
                    <span slot="update_time" slot-scope="text">{{ text | wuba_dateformat }}</span>
                    <span slot="action" slot-scope="text">
                        <a href="javascript:;" class="wb-m-l-5" @click="deleteEvent(text)">删除</a>
                    </span>
                </a-table>
            </div>
        </div>
        <MydDrawer :visible="visible" :id="editId" @editEvent="update" v-if="visible" />
    </div>
</template>

<script>
import modeData from '@/utils/modeData'
import Service from '@/utils/service/service'
import MydDrawer from './components/TaskCompont.vue'
import Driver from 'driver.js'

export default {
    components: {
        MydDrawer,
    },
    data() {
        return {
            testData: modeData.testData,
            columns: [
                { title: 'ID', dataIndex: 'id', key: 'id' },
                { title: '任务名称', key: 'name', scopedSlots: { customRender: 'name' } },
                { title: '消息总数', key: 'message_counts', scopedSlots: { customRender: 'message_counts' } },
                {
                    title: '更新时间',
                    dataIndex: 'update_time',
                    key: 'update_time',
                    scopedSlots: { customRender: 'update_time' },
                },
                { title: '开启状态', key: 'status', scopedSlots: { customRender: 'status' } },
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
            //
            visible: false,
            editId: null,
            dynamicValidateForm: {
                domains: [],
            },
            taskNameForm: {
                name: '',
                callback_url: '',
            },
            configData: [],
            configDataChoice: {},
            regionData: [],
            onSubmitLoading: false,
            isMoreConfig: false,
            searchValue: '',
        }
    },
    created() {
        this.initData()
    },
    mounted() {},
    methods: {
        initData(params = {}) {
            this.loading = true
            let data = {
                page_size: this.pagination.pageSize,
                search: this.searchValue,
                page: 1,
                ...params,
            }
            if (data.page === 1) {
                this.pagination.current = 1
            }
            // 初始化请求
            Service.getTasksManage(data).then((res) => {
                if (res.code === 1) {
                    let { data } = res
                    const pagination = { ...this.pagination }
                    pagination.total = data.count
                    this.pagination = pagination
                    this.data = data.results
                    this.initTast(this.data[0])
                }
            })
        },
        initTast(text) {
            //新手导航
            let flag = sessionStorage.getItem('firstLogin')
            if (flag == 'true') {
                const driver = new Driver({ allowClose: false })
                let timer = setTimeout(() => {
                    let out = true
                    driver.defineSteps([
                        {
                            element: document.getElementsByClassName('topTip')[0],
                            popover: {
                                title: '任务详情',
                                description: '查看自己任务的详细信息',
                                position: 'right',
                            },
                            showButtons: true,
                            doneBtnText: '下一步',
                            closeBtnText: '跳出',
                            onDeselected: () => {
                                if (out) {
                                    sessionStorage.setItem('firstLogin', 'false')
                                }
                            },
                            onNext: () => {
                                out = false
                                this.editEvent(text)
                            },
                        },
                    ])
                    driver.start()
                    clearTimeout(timer)
                }, 10)
            }
        },
        changeStatus(e, data) {
            let _this = this
            this.$confirm({
                title: '提示',
                content: e ? '是否开启' : '是否关闭',
                onOk() {
                    let datas = {
                        id: [],
                        status: e,
                    }
                    datas.id.push(data.id)
                    _this.getChangeStatus(datas)
                },
                onCancel() {
                    data.status = !e
                },
            })
        },
        update(i) {
            if (i.id) {
                this.editId = null
            }
            this.visible = false
            setTimeout(() => {
                this.initData()
            }, 500)
        },
        changeNum() {
            this.testData.handleNum(9)
        },
        onSearch() {
            this.initData()
        },
        handleTableChange(pagination) {
            const pager = { ...this.pagination }
            pager.current = pagination.current
            pager.pageSize = pagination.pageSize
            this.pagination = pager
            let data = {
                page_size: pagination.pageSize,
                page: pagination.current,
            }
            this.initData(data)
        },
        addEvent() {
            this.visible = true
        },
        editEvent(text) {
            this.editId = text.id
            this.visible = true
        },
        jumpEvent(data) {
            this.$router.push({ name: 'message', query: { id: data.id } })
        },
        enableEvent(status) {
            if (this.selectedRowKeys.length === 0) return this.$message.error('未选择任何数据')
            let data = {
                id: this.selectedRowKeys,
                status,
            }
            this.getChangeStatus(data)
        },
        getChangeStatus(data) {
            Service.getTasksManageStatus(data).then((res) => {
                if (res.code === 1) {
                    this.$message.success('操作成功')
                    this.selectedRowKeys = []
                } else {
                    this.$message.error(res.message)
                }
                this.initData()
            })
        },
        getDeleTask(data) {
            Service.getTasksManageDele(data).then((res) => {
                if (res.code === 1) {
                    this.$message.success('操作成功')
                    this.selectedRowKeys = []
                } else {
                    this.$message.error(res.message)
                }
                this.initData()
            })
        },
        deleteEvent(t = '') {
            let _this = this
            if (t) {
                this.$confirm({
                    title: '提示',
                    content: '确认删除',
                    onOk() {
                        let datas = {
                            id: t.id,
                        }
                        _this.getDeleTask(datas)
                    },
                    onCancel() {},
                })
            } else {
                if (this.selectedRowKeys.length === 0) return this.$message.error('未选择任何数据')
                let data = {
                    id: this.selectedRowKeys.join(','),
                }
                this.getDeleTask(data)
            }
        },
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
        },
    },
}
</script>

<style lang="less" scoped>
.search-area {
    margin-bottom: 5px;
    line-height: 32px;
}

.wb-form-drawer {
    background: #fff;
}

.wb-drawer-div {
    .ant-form-item {
        margin-bottom: 12px;
    }

    .ant-form-item.wb-m-b-0 {
        margin-bottom: 0px;
    }

    .ant-card {
        border-radius: 6px;
    }
}
/deep/ .ant-drawer-body {
    margin-bottom: 30px;
    padding: 12px;
}
</style>
