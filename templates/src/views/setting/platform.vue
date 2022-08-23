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
                    <a-form-model-item label="开放注册">
                        <a-switch v-model="form.OPEN_REGISTER" @click="openBtn($event, 'OPEN_REGISTER')" />
                    </a-form-model-item>
                    <a-form-model-item label="仅允许邀请注册">
                        <a-switch v-model="form.INVITE_TO_REGISTER" @click="openBtn($event, 'INVITE_TO_REGISTER')" />
                    </a-form-model-item>
                    <a-form-model-item ref="PLATFORM_DOMAIN" label="平台域名" prop="PLATFORM_DOMAIN">
                        <a-input v-model="form.PLATFORM_DOMAIN" addon-before="http://" placeholder="请输入" />
                    </a-form-model-item>
                    <!-- </div> -->
                    <!-- <div class="title clearfix">
        <div class="left">通知设置</div>
      </div> -->
                    <!-- <div class="content"> -->
                    <a-form-model-item label="开启邮件通知">
                        <a-switch v-model="form.OPEN_EMAIL" @click="openBtn($event, 'OPEN_EMAIL')" />
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
                    <a-form-model-item ref="DNS_DOMAIN" label="DNS记录域名" prop="DNS_DOMAIN">
                        <a-input v-model="form.DNS_DOMAIN" placeholder="必填,仅支持smtp协议,如：smtp.xxx.com" />
                    </a-form-model-item>
                    <a-form-model-item ref="SERVER_IP" label="解析IP" prop="SERVER_IP">
                        <a-input v-model="form.SERVER_IP" placeholder="必填,如0.0.0.0" />
                    </a-form-model-item>
                    <a-form-model-item ref="NS1_DOMAIN" label="NS1域名" prop="NS1_DOMAIN">
                        <a-input v-model="form.NS1_DOMAIN" placeholder="必填,仅支持smtp协议,如：smtp.xxx.com" />
                    </a-form-model-item>
                    <a-form-model-item ref="NS2_DOMAIN" label="NS2域名" prop="NS2_DOMAIN">
                        <a-input v-model="form.NS2_DOMAIN" placeholder="必填,如：334" />
                    </a-form-model-item>
                    <a-form-model-item ref="JNDI_PORT" label="JNDI监听端口" prop="JNDI_PORT">
                        <a-input v-model="form.JNDI_PORT" placeholder="必填,如：text@xxx.com" />
                    </a-form-model-item>
                    <a-form-model-item :wrapper-col="{ span: 4, offset: 4 }" class="wb-m-t-20">
                        <a-button type="primary" @click="onSubmit('ruleForm1')" :loading="protocalUpdateLoafing">
                            保存
                        </a-button>
                        <a-button @click="resetForm('ruleForm1')" class="wb-m-l-5">重置</a-button>
                    </a-form-model-item>
                </div>
            </a-form-model>
        </div>
        <!-- <div class="div_card">
      <div class="title clearfix">
        <div class="left">项目文档</div>
      </div>
      <div class="content">
        <a-row>
          <a-col :span="16">
            <a-form-model :model="form2" :label-col="labelCol" :wrapper-col="wrapperCol1">
              <a-form-model-item label="Wiki">
                <p>https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd=vscode%E8%87%AA%E5%8A%A8%E4%BF%9D%E5%AD%98%E8%AE%BE%E7%BD%AE&oq=Apifox%2520%25E8%25B4%25A6%25E5%258F%25B7&rsv_pq=c59bbfb40006010d&rsv_t=b27d1lbdqRYuFhCd4nc7GhjubIajtHgyYZ5KyFrZ3aguyuK9pB4OasuuMpQ&rqlang=cn&rsv_enter=1&rsv_dl=ts_1&rsv_sug3=16&rsv_sug1=18&rsv_sug7=100&rsv_sug2=1&rsv_btype=t&prefixsug=vscode%2520zidong&rsp=1&inputT=6815&rsv_sug4=6814</p>
              </a-form-model-item>
              <a-form-model-item label="Github">
                <p>https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd=vscode%E8%87%AA%E5%8A%A8%E4%BF%9D%E5%AD%98%E8%AE%BE%E7%BD%AE&oq=Apifox%2520%25E8%25B4%25A6%25E5%258F%25B7&rsv_pq=c59bbfb40006010d&rsv_t=b27d1lbdqRYuFhCd4nc7GhjubIajtHgyYZ5KyFrZ3aguyuK9pB4OasuuMpQ&rqlang=cn&rsv_enter=1&rsv_dl=ts_1&rsv_sug3=16&rsv_sug1=18&rsv_sug7=100&rsv_sug2=1&rsv_btype=t&prefixsug=vscode%2520zidong&rsp=1&inputT=6815&rsv_sug4=6814</p>
              </a-form-model-item>
              <a-form-model-item label="Introduction">
                <p>https://modao.cc/app/c56b8515498f9a55900af02f5b72f0778579869d#screen=skw3ojf0kcekzh7</p>
              </a-form-model-item>
            </a-form-model>
          </a-col>
          <a-col :span="8" class="Textright">
            <a-space :size="24">
              <div class="Textcenter">
                <img src="@/assets/WechatIMG24.png" alt="" width="80">
                <p class="">扫码加入</p>
                <p>XXXX开发者微信群</p>
              </div>
              <div class="Textcenter">
                <img src="@/assets/WechatIMG24.png" alt="" width="80">
                <p>扫码加入</p>
                <p>58安全应急响应中心</p>
              </div>
            </a-space>
          </a-col>
        </a-row>
      </div>
    </div> -->
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
                name: '',
                INVITE_TO_REGISTER: '',
                PLATFORM_DOMAIN: '',
                OPEN_EMAIL: '',
                EMAIL_HOST: '',
                EMAIL_HOST_USER: '',
                EMAIL_PORT: '',
                EMAIL_HOST_PASSWORD: '',

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
        }
    },
    created() {
        this.initData()
    },
    mounted() {},
    methods: {
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
}
</style>
