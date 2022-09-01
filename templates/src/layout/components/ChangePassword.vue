<template>
    <a-modal v-model="visible" title="修改密码" @ok="handleOk" :closable="false" :maskClosable="false">
        <a-form-model ref="ruleForm" :model="form" :rules="rules" class="login-form" :wrapper-col="wrapperCol">
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
                >
                    <a-icon slot="prefix" type="user" />
                </a-input>
            </a-form-model-item>
            <a-form-model-item ref="oldPassword" prop="oldPassword">
                <a-input-password v-model="form.oldPassword" placeholder="旧密码">
                    <a-icon slot="prefix" type="lock" />
                </a-input-password>
            </a-form-model-item>
            <a-form-model-item ref="password" prop="password">
                <a-input-password
                    v-model="form.password"
                    placeholder="设置密码: 8-16字符,字母区分大小写"
                    @change="getPasswordChange"
                >
                    <a-icon slot="prefix" type="lock" />
                </a-input-password>
            </a-form-model-item>
            <a-form-model-item ref="passwordAgain" prop="passwordAgain">
                <a-input-password v-model="form.passwordAgain" placeholder="确认密码">
                    <a-icon slot="prefix" type="lock" />
                </a-input-password>
            </a-form-model-item>
        </a-form-model>
        <template slot="footer">
            <a-button key="back" @click="onClose">取消</a-button>
            <a-button key="submit" type="primary" :loading="loading" @click="handleOk('ruleForm')">修改</a-button>
        </template>
    </a-modal>
</template>

<script>
import Service from '@/utils/service/service'
export default {
    props: {
        visible: Boolean,
    },
    data() {
        return {
            form: {
                username: '',
                oldPassword: '',
                password: undefined,
                passwordAgain: '',
            },
            labelCol: { span: 4 },
            wrapperCol: { span: 20, offset: 2 },
            rules: {
                username: [
                    { required: true, message: '邮箱必填', trigger: 'blur' },
                    {
                        pattern: '^[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$',
                        message: '邮箱格式不正确',
                        trigger: 'blur',
                    },
                ],
                oldPassword: [
                    { required: true, message: '密码必填', trigger: 'change' },
                    { min: 6, message: 'Length should be 6 to 16', trigger: 'blur' },
                ],
                password: [
                    { required: true, message: '密码必填', trigger: 'change' },
                    { min: 6, message: 'Length should be 6 to 16', trigger: 'blur' },
                    // { pattern: '^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).*$',message: '密码必须同时包含大写字母、小写字母和数字', trigger: 'blur'}
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
            },
            count: null,
            loading: false,
        }
    },
    methods: {
        handleOk(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.loading = true
                    Service.getChangePassword({
                        username: this.form.username,
                        old_password: this.form.oldPassword,
                        password: this.form.password,
                        password_confirm: this.form.password,
                    }).then(
                        (res) => {
                            this.loading = false
                            if (res.code === 1) {
                                sessionStorage.clear()
                                this.$router.push({ name: 'login' })
                                this.$message.success('修改成功')
                            } else {
                                this.$message.error(res.message)
                            }
                        },
                        (err) => {
                            this.loading = false
                        }
                    )
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        },
        onClose() {
            this.$refs.ruleForm.resetFields()
            this.$emit('onClose')
        },
        validatePass2(rule, value, cb) {
            this.$refs.ruleForm.validateField('password', (err) => {
                if (err) return
                if (value !== this.form.password) cb(new Error('两次密码不一致'))
                cb()
            })
        },
        getPasswordChange() {
            this.form.passwordAgain = ''
        },
    },
}
</script>

<style></style>
