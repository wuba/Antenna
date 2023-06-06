<template>
    <div class="platform">
        <div class="div_card">
            <div class="title clearfix">
                <div class="left">
                    API设置
                    <a-icon type="question-circle" style="cursor: pointer" @click="gotoInfo" />
                </div>
            </div>
            <div class="content">
                <a-form-model :model="form" :label-col="labelCol" :wrapper-col="wrapperCol">
                    <a-form-model-item label="API_Key">
                        <a-row :gutter="6">
                            <a-col :span="18">
                                <a-input v-model="form.domain" placeholder="请输入" readOnly>
                                    <my-copy slot="suffix" :text="form.domain"></my-copy>
                                </a-input>
                            </a-col>
                            <a-col :span="6">
                                <a-button @click="refresh">重置</a-button>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                </a-form-model>
            </div>
        </div>
        <div class="div_card">
            <div class="title clearfix">
                <div class="left">API列表</div>
            </div>
            <div class="content">
                <a-form-model :model="form1" layout="vertical">
                    <a-form-model-item label="获取各类消息记录">
                        <a-input-group compact v-for="(it, d) in urllist" :key="d">
                            <a-button type="primary">{{ it.method }}</a-button>
                            <a-input v-model="it.url" placeholder="请输入" style="width: 60%">
                                <my-copy slot="suffix" :text="it.url"></my-copy>
                            </a-input>
                        </a-input-group>
                    </a-form-model-item>
                    <!-- <a-form-model-item label="获取各类消息记录">
            <a-input-group compact>
              <a-button type="primary">post</a-button>
              <a-select default-value="Zhejiang" v-model="value1" style="width: 60%" dropdownClassName="dropdownClassName">
                <a-select-option value="Zhejiang">
                  Zhejiang
                  <my-copy text="Zhejiang"></my-copy>
                </a-select-option>
                <a-select-option value="Jiangsu">
                  Jiangsu
                  <my-copy text="Jiangsu"></my-copy>
                </a-select-option>
              </a-select>
            </a-input-group>
          </a-form-model-item>
          <a-form-model-item label="判断qi">
            <a-input-group compact>
              <a-button type="danger">get</a-button>
              <a-select default-value="Zhejiang" style="width: 60%" dropdownClassName="dropdownClassName">
                <a-select-option value="Zhejiang">
                  Zhejiang
                  <my-copy text="Zhejiang"></my-copy>
                </a-select-option>
                <a-select-option value="Jiangsu">
                  Jiangsu
                  <my-copy text="Jiangsu"></my-copy>
                </a-select-option>
              </a-select>
            </a-input-group>
          </a-form-model-item>
          <a-form-model-item label="使用DNSLog验证漏洞">
            <a-input-group compact>
              <a-button type="danger">get</a-button>
              <a-select default-value="Zhejiang" style="width: 60%" dropdownClassName="dropdownClassName">
                <a-select-option value="Zhejiang">
                  Zhejiang
                  <my-copy text="Zhejiang"></my-copy>
                </a-select-option>
                <a-select-option value="Jiangsu">
                  Jiangsu
                  <my-copy text="Zhejiang"></my-copy>
                </a-select-option>
              </a-select>
            </a-input-group>
          </a-form-model-item> -->
                </a-form-model>
            </div>
        </div>
    </div>
</template>

<script>
import MyCopy from '@/components/copy.vue'
import Service from '@/utils/service/service'
export default {
    components: {
        MyCopy,
    },
    data() {
        return {
            labelCol: { span: 4 },
            wrapperCol: { span: 10 },
            form: {
                domain: '',
            },
            value1: 'Zhejiang',
            value2: '',
            value3: '',
            form1: {
                notice: true,
                serve: '',
                port: '8080',
                account: '',
                password: '8080',
            },
            urllist: [],
        }
    },
    created() {
        this.initData()
    },
    mounted() {},
    methods: {
        gotoInfo() {
            window.open('https://blog.antenna.cool/docs/api_back')
        },
        initData() {
            Service.all([
                Service.getOpenAPI().then((res) => {
                    if (res.code === 1) {
                        let {
                            data: { results },
                        } = res
                        this.form.domain = results[0].key
                    } else {
                        this.$message.error(res.message)
                    }
                }),
                Service.getOpenAPIUrl().then((res) => {
                    if (res.code === 1) {
                        let {
                            data: { urllist },
                        } = res
                        this.urllist = urllist
                    } else {
                        this.$message.error(res.message)
                    }
                }),
            ]).then((res) => {
                // console.log(res, '所有请求的返回')
            })
        },
        refresh() {
            Service.getRefreshOpenAPI().then((res) => {
                if (res.code === 1) {
                    let { data } = res
                    this.form.domain = data.key
                } else {
                    this.$message.error(res.message)
                }
            })
        },
    },
}
</script>

<style lang="less" scoped>
.search-area {
    margin-bottom: 5px;
    line-height: 32px;
}
.platform {
    .ant-form-item {
        margin-bottom: 12px;
    }
    .copy {
        color: rgba(0, 0, 0, 0.45);
    }
    .anticon-check {
        color: #52c41a;
    }
}

.dropdownClassName .ant-select-dropdown-content li i.anticon {
    display: none !important;
}
</style>
