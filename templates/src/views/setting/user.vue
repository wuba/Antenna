<template>
    <div>
        <div class="div_card">
            <div class="title clearfix">
                <div class="left">最新消息</div>
            </div>
            <div class="content">
                <a-row :gutter="2" class="search-area">
                    <a-col :span="16">
                        <a-popconfirm
                            @visibleChange="handleVisibleChange"
                            :visible="visible"
                            placement="right"
                            overlayClassName="popconfirmDiv"
                        >
                            <div slot="title">
                                <p>邀请码</p>
                                <h5>
                                    {{ inviteCode }}
                                    <my-copy :text="inviteCode"></my-copy>
                                </h5>
                            </div>
                            <a-icon slot="icon" type="question-circle-o" style="color: #c3c3c3" />
                            <a-button
                                type="primary"
                                icon="plus-circle"
                                class="wb-m-r-5"
                                size="small"
                                :loading="popLoading"
                            >
                                邀请码
                            </a-button>
                        </a-popconfirm>
                    </a-col>
                    <a-col :span="8">
                        <a-input-search placeholder="输入账号关键字搜索" @search="onSearch" v-model="searchValue" />
                    </a-col>
                </a-row>
                <a-table
                    :columns="columns"
                    :data-source="data"
                    rowKey="id"
                    :pagination="pagination"
                    :loading="messageLoading"
                    @change="handleTableChange"
                >
                    <span slot="is_staff" slot-scope="text">
                        <a-switch v-model="text.is_staff" @click="changeStatus($event, text, 'is_staff')" />
                    </span>
                    <span slot="date_joined" slot-scope="text">{{ text | wuba_dateformat }}</span>
                    <span slot="is_active" slot-scope="text">
                        <a-switch v-model="text.is_active" @click="changeStatus($event, text, 'is_active')" />
                    </span>
                </a-table>
            </div>
        </div>
    </div>
</template>

<script>
import modeData from '@/utils/modeData'
import Service from '@/utils/service/service'
import { handleFilters } from '@/utils/tools.js'
import MyCopy from '@/components/copy.vue'
export default {
    components: {
        MyCopy,
    },
    data() {
        return {
            testData: modeData.testData,
            // table
            columns: [
                { title: 'ID', dataIndex: 'id', key: 'id' },
                { title: '账号', dataIndex: 'username', key: 'username' },
                {
                    title: '管理权限',
                    key: 'is_staff',
                    scopedSlots: { customRender: 'is_staff' },
                    filterMultiple: false,
                    filters: [
                        {
                            text: 'http',
                            value: 'true',
                        },
                        {
                            text: 'http',
                            value: 'false',
                        },
                    ],
                },
                {
                    title: '存活状态',
                    key: 'is_active',
                    scopedSlots: { customRender: 'is_active' },
                    filterMultiple: false,
                    filters: [
                        {
                            text: 'http',
                            value: 'true',
                        },
                        {
                            text: 'http',
                            value: 'false',
                        },
                    ],
                },
                {
                    title: '注册时间',
                    dataIndex: 'date_joined',
                    key: 'date_joined',
                    scopedSlots: { customRender: 'date_joined' },
                },
            ],
            data: [],
            pagination: {
                pageSizeOptions: ['10', '20', '30', '40', '50'],
                showSizeChanger: true,
                pageSize: 10,
            },
            searchValue: '',
            messageLoading: false,
            //
            popLoading: false,
            visible: false,
            inviteCode: '',
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
            Service.getUser(data).then((res) => {
                if (res.code === 1) {
                    let { data } = res
                    const pagination = { ...this.pagination }
                    pagination.total = data.count
                    this.pagination = pagination
                    this.data = data.results
                }
            })
            // 初始化请求
        },
        onSearch() {
            // console.log(value);
            this.initData()
        },
        handleTableChange(pagination, filters, sorter) {
            let p = handleFilters(filters)
            console.log(filters, p)
            const pager = { ...this.pagination }
            pager.current = pagination.current
            pager.pageSize = pagination.pageSize
            this.pagination = pager
            let data = {
                page_size: pagination.pageSize,
                page: pagination.current,
                ...p,
            }
            this.initData(data)
        },
        changeStatus(e, data, type) {
            let _this = this
            this.$confirm({
                title: '提示',
                content: e ? '是否开启' : '是否关闭',
                onOk() {
                    let datas = {}
                    datas[type] = e
                    Service.getChangeUserStatus(data.id, datas).then(
                        (res) => {
                            if (res.code === 1) {
                                _this.$message.success('变更成功')
                                _this.initData()
                            } else {
                                console.log('zoudaozhelil ?')
                                data[type] = !e
                                _this.$message.error(res.message)
                            }
                        },
                        (err) => {
                            data[type] = !e
                        }
                    )
                },
                onCancel() {
                    data[type] = !e
                },
            })
        },
        handleVisibleChange(visible) {
            if (!visible) {
                this.visible = false
                return
            }
            this.popLoading = true
            Service.getInvitCode().then((res) => {
                this.popLoading = false
                if (res.code === 1) {
                    this.visible = true
                    this.inviteCode = res.data.invite_code
                } else {
                    this.$message.error(res.message)
                }
                console.log('获取到的邀请码', res)
            })
        },
    },
}
</script>

<style lang="less">
.search-area {
    margin-bottom: 5px;
    line-height: 32px;
}

.popconfirmDiv.ant-popover {
    .ant-popover-buttons {
        display: none !important;
    }
}
</style>
