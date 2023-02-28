<template>
    <div class="platform">
        <div class="div_card">
            <a-form-model
                ref="ruleForm"
                :model="form"
                :rules="rules"
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
                :hideRequiredMark="true"
            >
                <div class="title clearfix">
                    <div class="left">平台设置</div>
                </div>
                <div class="content">
                    <a-form-model-item label="平台注册">
                        <a-select v-model="form.REGISTER_TYPE" style="width: 120px" @change="handleChange">
                            <a-select-option :key="1" :value="0">禁止注册</a-select-option>
                            <a-select-option :key="2" :value="1">开放注册</a-select-option>
                            <a-select-option :key="3" :value="2">邀请码注册</a-select-option>
                        </a-select>
                    </a-form-model-item>
                    <a-form-model-item ref="PLATFORM_DOMAIN" label="平台域名" prop="PLATFORM_DOMAIN">
                        <a-input v-model="form.PLATFORM_DOMAIN" addon-before="http://" placeholder="请输入" />
                    </a-form-model-item>
                    <a-form-model-item ref="SERVER_IP" label="公网IP" prop="PLATFORM_DOMAIN">
                        <a-input v-model="form.SERVER_IP" placeholder="请输入" />
                    </a-form-model-item>
                    <a-form-model-item label="开启邮件通知">
                        <a-switch v-model="form.OPEN_EMAIL" @click="openBtn($event, 'OPEN_EMAIL')" />
                    </a-form-model-item>
                    <a-form-model-item label="保留七天消息">
                        <a-switch
                            v-model="form.SAVE_MESSAGE_SEVEN_DAYS"
                            @click="openBtn($event, 'SAVE_MESSAGE_SEVEN_DAYS')"
                        />
                    </a-form-model-item>
                    <a-form-model-item ref="EMAIL_HOST" label="SMTP服务器" prop="EMAIL_HOST">
                        <a-input
                            v-model="form.EMAIL_HOST"
                            @blur="
                                () => {
                                    $refs.EMAIL_HOST.onFieldBlur()
                                }
                            "
                            placeholder="必填,仅支持smtp协议,如：smtp.xxx.com"
                        />
                    </a-form-model-item>
                    <a-form-model-item ref="EMAIL_PORT" label="端口" prop="EMAIL_PORT">
                        <a-input
                            v-model="form.EMAIL_PORT"
                            placeholder="必填,如：334"
                            @blur="
                                () => {
                                    $refs.EMAIL_PORT.onFieldBlur()
                                }
                            "
                        />
                    </a-form-model-item>
                    <a-form-model-item ref="EMAIL_HOST_USER" label="账号" prop="EMAIL_HOST_USER">
                        <a-input
                            v-model="form.EMAIL_HOST_USER"
                            placeholder="必填,如：text@xxx.com"
                            @blur="
                                () => {
                                    $refs.EMAIL_HOST_USER.onFieldBlur()
                                }
                            "
                        />
                    </a-form-model-item>
                    <a-form-model-item
                        ref="EMAIL_HOST_PASSWORD"
                        label="密码/授权码"
                        prop="EMAIL_HOST_PASSWORD"
                        :wrapper-col="{ span: 14 }"
                    >
                        <a-row>
                            <a-col :span="17">
                                <a-input
                                    v-model="form.EMAIL_HOST_PASSWORD"
                                    placeholder="必填,如：text@xxx.com"
                                    @blur="
                                        () => {
                                            $refs.EMAIL_HOST_PASSWORD.onFieldBlur()
                                        }
                                    "
                                />
                            </a-col>
                            <a-col :span="2" class="wb-m-l-5">
                                <a-tooltip>
                                    <template slot="title">发送测试邮件</template>
                                    <a-button @click="getSendMail" :loading="sendMailLoaging" icon="mail" />
                                </a-tooltip>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                    <a-form-model-item :wrapper-col="{ offset: 4 }" class="wb-m-t-20">
                        <a-button type="primary" @click="onSubmit('ruleForm')" :loading="renewLoading">保存</a-button>
                        <a-button @click="resetForm('ruleForm')" class="wb-m-l-5">重置</a-button>
                    </a-form-model-item>
                </div>
            </a-form-model>
        </div>
        <div class="div_card">
            <a-form-model
                ref="ruleForm1"
                :model="form"
                :rules="rules"
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
                :hideRequiredMark="true"
            >
                <div class="title clearfix">
                    <div class="left">协议设置</div>
                </div>
                <div class="content">
                    <a-table :columns="columns" :data-source="tableData" key="id">
                        <a slot="type" slot-scope="type">A</a>
                        <a slot="domain" slot-scope="domain, record">
                            <a-Input :value="domain" @change="inputDomain($event, record)" />
                        </a>
                        <a slot="value" slot-scope="value, record">
                            <a-select @change="(e) => setvalues(e, record)" mode="tags" :value="value" />
                        </a>
                        <a slot="id" slot-scope="id, record">
                            <a-button type="primary" class="mgright5" @click="saveDns(record)">保存</a-button>
                            <a-popconfirm title="确认删除本行吗?" ok-text="是" cancel-text="否" @confirm="onDel(id)">
                                <a-button type="danger">删除</a-button>
                            </a-popconfirm>
                        </a>
                    </a-table>
                </div>
            </a-form-model>
        </div>
    </div>
</template>

<script>
import Service from '@/utils/service/service'
export default {
    data() {
        return {
            labelCol: { span: 4 },
            wrapperCol: { span: 10 },
            wrapperCol1: { span: 20 },
            form: {
                OPEN_REGISTER: '',
                REGISTER_TYPE: 0,
                name: '',
                INVITE_TO_REGISTER: '',
                PLATFORM_DOMAIN: '',
                OPEN_EMAIL: '',
                EMAIL_HOST: '',
                EMAIL_HOST_USER: '',
                EMAIL_PORT: '',
                EMAIL_HOST_PASSWORD: '',
                SAVE_MESSAGE_SEVEN_DAYS: false,
                DNS_DOMAIN: '',
                SERVER_IP: '',
                NS1_DOMAIN: '',
                NS2_DOMAIN: '8080',
                JNDI_PORT: '',
            },
            formSpare: {},
            rules: {
                PLATFORM_DOMAIN: [
                    { required: true, message: '域名必填', trigger: 'blur' },
                    {
                        pattern: new RegExp(
                            '^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$'
                        ),
                        message: '仅支持域名格式',
                        trigger: 'blur',
                    },
                ],
                EMAIL_HOST: [
                    { validator: this.validatePass, trigger: 'blur' },
                    { pattern: new RegExp('^[^\u4E00-\u9FFF]+$'), message: '不支持中文', trigger: 'blur' },
                ],
                EMAIL_PORT: [
                    { validator: this.validatePass, trigger: 'blur' },
                    { pattern: new RegExp('^[0-9]+$'), message: '只支持数字', trigger: 'blur' },
                ],
                EMAIL_HOST_USER: [{ validator: this.validatePass, trigger: 'blur' }],
                EMAIL_HOST_PASSWORD: [{ validator: this.validatePass, trigger: 'blur' }],

                DNS_DOMAIN: [{ required: true, message: '不可为空', trigger: 'blur' }],
                SERVER_IP: [{ required: true, message: '不可为空', trigger: 'blur' }],

                NS1_DOMAIN: [{ required: true, message: '不可为空', trigger: 'blur' }],
                NS2_DOMAIN: [{ required: true, message: '不可为空', trigger: 'blur' }],
                JNDI_PORT: [
                    { required: true, message: '不可为空', trigger: 'blur' },
                    { pattern: new RegExp('^[0-9]+$'), message: '只支持数字', trigger: 'blur' },
                ],
            },
            renewLoading: false,
            protocalUpdateLoafing: false,
            sendMailLoaging: false,
            form2: {},
            num: 1,
            columns: [
                {
                    dataIndex: 'id',
                    key: 'id',
                    title: 'id',
                },
                {
                    dataIndex: 'type',
                    key: 'type',
                    title: '解析类型',
                    scopedSlots: { customRender: 'type' },
                },
                {
                    dataIndex: 'domain',
                    key: 'domain',
                    title: '解析域名(*.test.com)代表所有子域名',
                    scopedSlots: { customRender: 'domain' },
                },
                {
                    dataIndex: 'value',
                    key: 'value',
                    title: '解析内容',
                    scopedSlots: { customRender: 'value' },
                },
                {
                    dataIndex: 'id',
                    key: 'id',
                    title: '操作',
                    scopedSlots: { customRender: 'id' },
                },
            ],
            tableData: [],
        }
    },
    created() {
        this.initData()
    },
    mounted() {
        this.getDnsInfo()
    },
    methods: {
        saveDns(record) {
            Service.dns_update({ id: record.id, value: record.value, domain: record.domain }).then((res) => {
                if (res.code === 1) {
                    //保存成功
                    this.$message.success('保存成功')
                    this.getDnsInfo()
                }
            })
        },
        setvalues(e, r) {
            const a = e.filter((item) => this.isIP(item))

            this.tableData.forEach((item) => {
                if (item.id === r.id) {
                    item.value = a
                }
            })
        },
        isIP(ip) {
            var re =
                /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
            return re.test(ip)
        },
        inputDomain(e, r) {
            this.tableData.forEach((item) => {
                if (item.id === r.id) {
                    item.domain = e.target.value
                }
            })
        },
        onDel(n) {
            const length = this.tableData.length
            if (this.tableData[length - 1].id === n) {
                this.$message.warn('不能删除最后一项')
            } else {
                Service.dns_delete({ id: n }).then((res) => {
                    if (res.code === 1) {
                        //删除成功
                        this.$message.success('删除成功')
                        this.getDnsInfo()
                    }
                })
            }
        },
        getDnsInfo() {
            Service.get_dns().then((res) => {
                const arr = res.data.results
                const length = arr.length
                if (length) {
                    arr.push({ id: arr[length - 1].id + 1, domain: '', value: [] })
                } else {
                    arr.push({ id: 1, domain: '', value: [] })
                }
                this.tableData = arr
            })
        },
        initData() {
            Service.getConfigsManage({ page_size: 20 }).then((res) => {
                if (res.code === 1) {
                    this.form = res.data
                    this.formSpare = Object.assign({}, res.data)
                }
            })
        },
        onSubmit(name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if (name === 'ruleForm') {
                        this.renewLoading = true
                        Service.getConfigsRenew(this.form).then((res) => {
                            // console.log(res, '更新信息的返回')
                            this.renewLoading = false
                            if (res.code === 1) {
                                this.form = res.data
                                this.formSpare = Object.assign({}, res.data)
                                Service.platform_restart()
                                this.$message.success('操作成功')
                            } else {
                                this.$message.error(res.message)
                            }
                        })
                    } else {
                        this.protocalUpdateLoafing = true
                        Service.getConfigsProtocalUpdate(this.form).then((res) => {
                            this.protocalUpdateLoafing = false
                            if (res.code === 1) {
                                this.form = res.data
                                this.formSpare = Object.assign({}, res.data)
                                Service.platform_restart()
                                this.$message.success('操作成功')
                            } else {
                                this.$message.error(res.message)
                            }
                            console.log('更新协议配置的返回', res)
                        })
                    }
                }
            })
        },
        getSendMail() {
            this.sendMailLoaging = true
            let data = {
                EMAIL_HOST: this.form.EMAIL_HOST,
                EMAIL_PORT: this.form.EMAIL_PORT,
                EMAIL_HOST_USER: this.form.EMAIL_HOST_USER,
                EMAIL_HOST_PASSWORD: this.form.EMAIL_HOST_PASSWORD,
            }
            Service.getSendMail(data).then(
                (res) => {
                    this.sendMailLoaging = false
                    if (res.code === 1) {
                        this.$message.success('操作成功')
                    } else {
                        this.$message.error(res.message)
                    }
                },
                (error) => {
                    this.sendMailLoaging = false
                }
            )
        },
        openBtn(e, name) {
            let _this = this,
                title = e ? '是否打开' : '是否关闭'
            this.$confirm({
                title: '提示',
                content: title,
                onOk() {},
                onCancel() {
                    _this.form[name] = !e
                },
            })
        },
        validatePass(rule, value, cb) {
            if (this.form.OPEN_EMAIL) {
                if (!value) cb('不可为空')
            }
            cb()
        },
        resetForm(formName) {
            this.$refs[formName].resetFields()
            this.form = Object.assign({}, this.formSpare)
        },
    },
}
</script>

<style lang="less" scoped>
.search-area {
    margin-bottom: 5px;
    line-height: 32px;
}
.inputWidth {
    width: 100px;
}
.platform {
    .ant-form-item {
        margin-bottom: 12px;
    }
    /deep/ .ant-form-item-control,
    /deep/ .ant-form-item-label {
        line-height: 24px;
    }
    p {
        position: relative;
        overflow: hidden;
        text-overflow: ellipsis;
        -webkit-line-clamp: 3;
        margin-bottom: 0px;
    }
    .mgright5 {
        margin-right: 5px;
    }
}
</style>
