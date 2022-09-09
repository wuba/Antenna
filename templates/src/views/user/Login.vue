<template>
    <div class="bigContain">
        <img class="bgimge" src="@/assets/bgimg.png" alt="" />
        <div class="user-layout-login">
            <img class="logoImg" src="@/assets/logotitle.png" alt="" />
            <div class="topTitle">{{ type === 1 ? '账号登录' : type === 2 ? '注册账号' : '忘记密码' }}</div>
            <div v-show="type === 1">
                <a-form-model ref="ruleFormLogin" :model="form" :rules="rules">
                    <a-form-model-item ref="username" prop="username">
                        <a-input
                            v-model="form.username"
                            placeholder="电子邮箱"
                            @blur="
                                () => {
                                    $refs.username.onFieldBlur()
                                }
                            "
                            @change="
                                () => {
                                    $refs.username.onFieldBlur()
                                }
                            "
                            size="large"
                        >
                            <a-icon slot="prefix" type="user" />
                        </a-input>
                    </a-form-model-item>
                    <a-form-model-item ref="password" prop="loginPd">
                        <a-input-password
                            v-model="form.loginPd"
                            placeholder="密码"
                            size="large"
                            @pressEnter="submitLoginForm('ruleFormLogin')"
                        >
                            <a-icon slot="prefix" type="lock" />
                        </a-input-password>
                    </a-form-model-item>
                    <a-form-model-item>
                        <a-button type="primary" class="login-form-button" @click="submitLoginForm('ruleFormLogin')">
                            登陆
                        </a-button>
                        <a class="login-form-forgot" href="javascript:void(0)" @click="forgetEvent">忘记密码</a>
                        <a href="javascript:void(0)" class="login-form-forgot wb-m-r-10" @click="registerEvent">
                            注册账号
                        </a>
                    </a-form-model-item>
                </a-form-model>
            </div>
            <div v-show="type === 2">
                <a-form-model ref="ruleFormRegister" :model="form" :rules="rules" class="login-form">
                    <a-form-model-item ref="name" prop="username">
                        <a-input
                            v-model="form.username"
                            placeholder="电子邮箱"
                            @blur="
                                () => {
                                    $refs.username.onFieldBlur()
                                }
                            "
                            @change="
                                () => {
                                    $refs.username.onFieldBlur()
                                }
                            "
                            size="large"
                        >
                            <a-icon slot="prefix" type="user" />
                        </a-input>
                    </a-form-model-item>
                    <a-form-model-item ref="VerificationCode" prop="VerificationCode">
                        <a-row :gutter="8">
                            <a-col :span="14">
                                <a-input
                                    v-model="form.VerificationCode"
                                    placeholder="验证码"
                                    @blur="
                                        () => {
                                            $refs.VerificationCode.onFieldBlur()
                                        }
                                    "
                                    @change="
                                        () => {
                                            $refs.VerificationCode.onFieldBlur()
                                        }
                                    "
                                    size="large"
                                >
                                    <a-icon slot="prefix" type="safety-certificate" />
                                </a-input>
                            </a-col>
                            <a-col :span="10">
                                <a-button
                                    size="large"
                                    @click="getVerificationCode('ruleFormRegister')"
                                    :disabled="verificationCodeStatus"
                                >
                                    {{ verificationCodeStatus ? count : '' }}{{ verificationCodeText }}
                                </a-button>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                    <a-form-model-item ref="password" prop="password">
                        <a-input-password
                            v-model="form.password"
                            placeholder="设置密码: 8-16字符,字母区分大小写"
                            @blur="
                                () => {
                                    $refs.password.onFieldBlur()
                                }
                            "
                            @change="getPasswordChange"
                            size="large"
                        >
                            <a-icon slot="prefix" type="lock" />
                        </a-input-password>
                    </a-form-model-item>
                    <a-form-model-item ref="passwordAgain" prop="passwordAgain">
                        <a-input-password v-model="form.passwordAgain" placeholder="确认密码" size="large">
                            <!-- @blur=" () => { $refs.passwordAgain.onFieldBlur();} " -->
                            <a-icon slot="prefix" type="lock" />
                        </a-input-password>
                    </a-form-model-item>
                    <a-form-model-item
                        ref="InvitationCode"
                        :prop="open_invite === 1 ? 'InvitationCode' : ''"
                        v-if="open_invite === 1"
                    >
                        <a-input
                            v-model="form.InvitationCode"
                            placeholder="邀请码"
                            @blur="
                                () => {
                                    $refs.InvitationCode.onFieldBlur()
                                }
                            "
                            @change="
                                () => {
                                    $refs.InvitationCode.onFieldBlur()
                                }
                            "
                            size="large"
                            @pressEnter="submitRegisterForm"
                        >
                            <a-icon slot="prefix" type="lock" />
                        </a-input>
                    </a-form-model-item>
                    <a-form-model-item>
                        <a-button type="primary" class="login-form-button" @click="submitRegisterForm()">注册</a-button>
                        <a class="login-form-forgot" href="javascript:void(0)" @click="loginEvent">使用已有账号登陆</a>
                    </a-form-model-item>
                </a-form-model>
            </div>
            <div v-show="type === 3">
                <a-form-model ref="ruleFormForget" :model="form" :rules="rules" class="login-form">
                    <a-form-model-item ref="username" prop="username">
                        <a-input v-model="form.username" placeholder="电子邮箱" size="large">
                            <a-icon slot="prefix" type="user" />
                        </a-input>
                    </a-form-model-item>
                    <a-form-model-item ref="VerificationCode" prop="VerificationCode">
                        <a-row :gutter="8">
                            <a-col :span="14">
                                <a-input
                                    v-model="form.VerificationCode"
                                    placeholder="验证码"
                                    @blur="
                                        () => {
                                            $refs.VerificationCode.onFieldBlur()
                                        }
                                    "
                                    @change="
                                        () => {
                                            $refs.VerificationCode.onFieldBlur()
                                        }
                                    "
                                    size="large"
                                >
                                    <a-icon slot="prefix" type="safety-certificate" />
                                </a-input>
                            </a-col>
                            <a-col :span="10">
                                <a-button
                                    size="large"
                                    @click="getVerificationCode('ruleFormForget')"
                                    :disabled="verificationCodeStatus"
                                >
                                    {{ verificationCodeStatus ? count : '' }}{{ verificationCodeText }}
                                </a-button>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                    <a-form-model-item ref="password" prop="password">
                        <a-input-password
                            v-model="form.password"
                            placeholder="设置密码: 8-16字符,字母区分大小写"
                            @blur="
                                () => {
                                    $refs.password.onFieldBlur()
                                }
                            "
                            @change="
                                () => {
                                    $refs.password.onFieldBlur()
                                }
                            "
                            size="large"
                        >
                            <a-icon slot="prefix" type="lock" />
                        </a-input-password>
                    </a-form-model-item>
                    <a-form-model-item ref="passwordAgain" prop="passwordAgain">
                        <a-input-password
                            v-model="form.passwordAgain"
                            placeholder="确认密码"
                            @blur="
                                () => {
                                    $refs.passwordAgain.onFieldBlur()
                                }
                            "
                            @change="
                                () => {
                                    $refs.passwordAgain.onFieldBlur()
                                }
                            "
                            size="large"
                        >
                            <a-icon slot="prefix" type="lock" />
                        </a-input-password>
                    </a-form-model-item>
                    <a-form-model-item>
                        <a-button type="primary" class="login-form-button" @click="retrieveEvent()">确认</a-button>
                        <a class="login-form-forgot" href="javascript:void(0)" @click="loginEvent">使用已有账号登陆</a>
                    </a-form-model-item>
                </a-form-model>
            </div>
        </div>
    </div>
</template>

<script>
import Service from '@/utils/service/service'
export default {
    data() {
        return {
            labelCol: { span: 4 },
            wrapperCol: { span: 14 },
            form: {
                username: '',
                password: undefined,
                loginPd: undefined,
                passwordAgain: '',
                InvitationCode: undefined, // 邀请码
                VerificationCode: undefined, // 验证码
            },
            rules: {
                username: [
                    { required: true, message: '邮箱必填', trigger: 'blur' },
                    {
                        pattern: new RegExp(
                            '^[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$'
                        ),
                        message: '邮箱格式不正确',
                        trigger: 'blur',
                    },
                ],
                loginPd: [{ required: true, message: '邮箱必填', trigger: 'blur' }],
                password: [
                    { required: true, message: '密码必填', trigger: 'change' },
                    { min: 6, message: '密码长度最少6位数', trigger: 'blur' },
                    // { pattern: new RegExp('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$'),message: '密码必须同时包含字母和数字', trigger: 'blur'}
                    {
                        pattern: new RegExp('^(?=.*([a-zA-Z].*))(?=.*[0-9].*)[a-zA-Z0-9-*/+.~!@#$%^，,&+=_*()]{6,20}$'),
                        message: '密码必须同时包含字母和数字',
                        trigger: 'blur',
                    },
                ],
                passwordAgain: [
                    { required: true, message: '密码必填', trigger: 'change' },
                    { validator: this.validatePass2, trigger: 'blur' },
                ],
                InvitationCode: [{ required: true, message: '必填', trigger: 'change' }],
                VerificationCode: [{ required: true, message: '验证码必填', trigger: 'change' }],
            },
            type: 1,
            verificationCodeStatus: false,
            verificationCodeText: '获取验证码',
            count: null,
            open_invite: 0,
        }
    },
    created() {},
    mounted() {},
    methods: {
        // 登陆
        submitLoginForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    Service.getLogin({
                        username: this.form.username,
                        password: this.form.loginPd,
                    }).then(
                        (res) => {
                            if (res.code === 1) {
                                const { data } = res
                                this.$message.success('登陆成功')
                                sessionStorage.setItem('username', data.username)
                                sessionStorage.setItem('token', data.token)
                                sessionStorage.setItem('role', data.is_staff)
                                this.$router.push({ name: 'dashboard' })
                            } else {
                                this.$message.error(res.message)
                            }
                        },
                        (err) => {}
                    )
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        },
        // 注册
        submitRegisterForm() {
            this.$refs.ruleFormRegister.validate((valid) => {
                if (valid) {
                    Service.getRegister({
                        username: this.form.username,
                        password: this.form.password,
                        verify_code: this.form.VerificationCode,
                        invite_code: this.form.InvitationCode,
                    }).then((res) => {
                        console.log('注册 正常的返回', res)
                        if (res.code === 1) {
                            this.$message.success('注册成功')
                            this.type = 1
                            this.$refs.ruleFormRegister.resetFields()
                        } else {
                            this.$message.error(res.message)
                        }
                    })
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        },
        // 注册 获取验证码
        getVerificationCode(form) {
            this.$refs[form].validateField('username', (err) => {
                if (err) return
                this.verificationCodeStatus = true
                Service.getSendmail({
                    username: this.form.username,
                }).then(
                    (res) => {
                        if (res.code === 1) {
                            this.$message.info('验证码已发送，请邮箱查看')
                            this.verificationCodeText = 's 后重新获取'
                            const TIME_COUNT = 60
                            if (!this.timer) {
                                this.count = TIME_COUNT
                                this.timer = setInterval(() => {
                                    if (this.count > 1 && this.count <= TIME_COUNT) {
                                        this.count--
                                    } else {
                                        clearInterval(this.timer)
                                        this.timer = null
                                        this.verificationCodeStatus = false
                                        this.verificationCodeText = '获取验证码'
                                    }
                                }, 1000)
                                return
                            }
                        } else {
                            this.$message.error(res.message)
                            this.verificationCodeStatus = false
                            this.verificationCodeText = '获取验证码'
                        }
                    },
                    (err) => {
                        this.verificationCodeStatus = false
                    }
                )
            })
        },
        // 密码框change事件
        getPasswordChange(i) {
            this.form.passwordAgain = ''
        },
        // 忘记密码
        retrieveEvent() {
            this.$refs.ruleFormForget.validate((valid) => {
                if (valid) {
                    Service.getForgetPassword({
                        username: this.form.username,
                        password: this.form.password,
                        verify_code: this.form.VerificationCode,
                        password_confirm: this.form.passwordAgain,
                    }).then((res) => {
                        console.log('忘记密码的返回 正常', res)
                        if (res.code === 1) {
                            this.$message.success('修改成功')
                            this.type = 1
                            this.$refs.ruleFormForget.resetFields()
                        } else {
                            this.$message.error(res.message)
                        }
                    })
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        },
        registerEvent() {
            this.type = 2
            Service.getOpenInvite().then((res) => {
                this.open_invite = res.data.open_invite
            })
            // this.$router.push({path:'/user/register'})ruleFormRegister
            this.$refs.ruleFormRegister.resetFields()
        },
        loginEvent() {
            this.type = 1
            this.$refs.ruleFormLogin.resetFields()
        },
        forgetEvent() {
            this.type = 3
            this.$refs.ruleFormForget.resetFields()
        },
        changeEvent() {
            this.$refs.ruleFormRetrieve.validate((valid) => {
                if (valid) {
                    alert('submit!')
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        },
        emailValidator(rule, value, cb) {
            if (value.length < 2) cb(new Error('长度必须大于2'))
            cb()
        },
        validatePass2(rule, value, cb) {
            this.$refs.ruleFormRegister.validateField('password', (err) => {
                if (err) return
                if (value !== this.form.password) cb(new Error('两次密码不一致'))
                cb()
            })
        },
    },
}
</script>

<style lang="less" scoped>
.bigContain {
    background: #fff;
    border-radius: 8px;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    width: 980px;
    height: 600px;
    margin: auto;
    display: flex;
    .user-layout-login {
        width: 530px;
        padding: 75px;
        .logoImg {
            width: 206.88px;
            height: 55.78px;
            margin: 0 66px 44px 66px;
        }
        .topTitle {
            margin-bottom: 40px;
            font-size: 20px;
            font-weight: 500;
            line-height: 28px;
            color: rgba(29, 33, 41, 1);
        }
        .inputSize {
            width: 100%;
        }
    }
    .bgimge {
        width: 450px;
        height: 600px;
    }
    .login-form {
        // max-width: 360px;
        .ant-form-item {
            margin-bottom: 16px;
        }
        button {
            width: 100%;
        }
    }
    .login-form-forgot {
        float: right;
    }
    .login-form-button {
        width: 100%;
        height: 48px;
        background-color: rgba(3, 100, 255, 1);
    }
}
</style>
