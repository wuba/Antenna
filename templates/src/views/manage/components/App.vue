<template>
    <div class="app-list">
        <a-list :grid="{ gutter: 24, lg: 3, md: 2, sm: 1, xs: 1 }" :dataSource="dataSource" class="card-list">
            <a-list-item slot="renderItem" slot-scope="item">
                <template v-if="item.id == 'new'">
                    <a-button class="new-btn" type="dashed" @click="showModal">
                        <div style="font-size: 90px">+</div>
                    </a-button>
                </template>
                <template v-else>
                    <a-card :hoverable="true">
                        <a-card-meta>
                            <div slot="title">
                                {{ item.title }}
                                <a-tag color="#108ee9" v-if="item.type === 0">利用组件</a-tag>
                                <a-tag color="#f2ab24" v-else>监听组件</a-tag>
                            </div>
                            <a-avatar style="backgroundcolor: #87d068" class="card-avatar" slot="avatar" icon="fire" />
                            <div class="meta-content" slot="description">{{ item.desc ? item.desc : '暂无介绍' }}</div>
                        </a-card-meta>
                        <p class="Textright wb-m-b-1">{{ item.author }}</p>
                        <template class="ant-card-actions" slot="actions">
                            <a href="javascript:void(0)" @click="jump(item)">使用文档</a>
                            <a href="javascript:void(0)" @click="editComponent(item)">修改组件</a>
                            <a href="javascript:void(0)" @click="delete_template(item)">删除组件</a>
                        </template>
                    </a-card>
                </template>
            </a-list-item>
        </a-list>
        <a-pagination
            class="Textright"
            v-model="current"
            :page-size-options="pageSizeOptions"
            :total="total"
            show-size-changer
            :page-size="pageSize"
            @showSizeChange="onShowSizeChange"
            @change="changePage"
        >
            <template slot="buildOptionText" slot-scope="props">
                <span v-if="props.value !== '50'">{{ props.value }}条/页</span>
                <span v-if="props.value === '50'">全部</span>
            </template>
        </a-pagination>
        <newConponets v-if="visible" :visible="visible" :titles="titles" :content="content" />
    </div>
</template>

<script>
import Service from '@/utils/service/service'
import newConponets from './newComponents/index.vue'
import { message } from 'ant-design-vue'
export default {
    name: 'Article',
    components: { newConponets },
    data() {
        return {
            dataSource: [],
            pageSizeOptions: ['10', '20', '30', '40', '50'],
            current: 1,
            pageSize: 10,
            total: 50,
            visible: false,
            titles: '新增组件',
            content: '',
        }
    },
    created() {
        this.initData()
    },
    methods: {
        showModal() {
            this.titles = '新增组件'
            this.visible = true
        },
        editComponent(item) {
            Service.template_info({ template: item.id }).then((res) => {
                if (res.code === 1) {
                    this.visible = true
                    this.titles = '编辑组件'
                    this.content = { ...item, ...res.data }
                } else {
                    message.error(res.message)
                }
            })
        },
        delete_template(item) {
            Service.delete_template({ template_id: item.id }).then((res) => {
                if (res.code === 1) {
                    this.initData()
                    this.$message.success('删除成功')
                } else {
                    message.error(res.message)
                }
            })
        },
        jump(text) {
            window.open('https://github.com/wuba/Antenna#readme', '_blank')
        },
        initData(params = {}) {
            let data = {
                page_size: this.pageSize,
                page: this.current,
                ...params,
            }
            Service.getTemplatesManage(data).then((res) => {
                // console.log(res, '获取所有组件的数据')
                if (res.code === 1) {
                    let { data } = res
                    this.total = data.count
                    data.results.unshift({ id: 'new' })
                    this.dataSource = data.results
                } else {
                    this.$message.error(res.message)
                }
            })
        },
        onShowSizeChange(current, pageSize) {
            // console.log(current, 'onShowSizeChange',pageSize)
            this.pageSize = pageSize
            this.initData()
        },
        changePage(current, size) {
            let data = {
                page_size: size,
                page: current,
            }
            this.initData(data)
        },
    },
}
</script>

<style lang="less" scoped>
.card-list {
    /deep/ .ant-card-body:hover {
        .ant-card-meta-title > a {
            color: #1890ff;
        }
    }

    /deep/ .ant-card-meta-title {
        margin-bottom: 12px;

        & > a {
            display: inline-block;
            max-width: 100%;
            color: rgba(0, 0, 0, 0.85);
        }
    }

    /deep/ .meta-content {
        position: relative;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        height: 64px;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;

        margin-bottom: 1em;
    }
}

.ant-card-actions {
    background: #f7f9fa;

    li {
        float: left;
        text-align: center;
        margin: 12px 0;
        color: rgba(0, 0, 0, 0.45);
        width: 50%;

        &:not(:last-child) {
            border-right: 1px solid #e8e8e8;
        }

        a {
            color: rgba(0, 0, 0, 0.45);
            line-height: 22px;
            display: inline-block;
            width: 100%;
            &:hover {
                color: #1890ff;
            }
        }
    }
}
.new-btn {
    background-color: #fff;
    border-radius: 2px;
    width: 100%;
    height: 225px;
}
</style>
