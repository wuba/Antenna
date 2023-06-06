<template>
    <div>
        <a-modal :title="titles" :visible="visible" @cancel="init" :maskClosable="false" width="1200px" footer="">
            <section style="display: flex">
                <div style="width: 600px">
                    <a-form :form="form" @submit="handleSubmit">
                        <a-form-item label="组件标题" v-bind="waiformItemLayout">
                            <a-input
                                :required="true"
                                style="width: 80%"
                                placeholder="请输入组件标题，例如DNS协议监听组件"
                                v-decorator="[
                                    'title',
                                    { rules: [{ required: true, message: '请输入组件标题，例如DNS协议监听组件' }] },
                                ]"
                            />
                        </a-form-item>
                        <a-form-item label="组件名称" v-bind="waiformItemLayout">
                            <a-input
                                :required="true"
                                style="width: 80%"
                                placeholder="请输入组件名称，例如DNS"
                                v-decorator="[
                                    'name',
                                    { rules: [{ required: true, message: '请输入组件名称，例如DNS' }] },
                                ]"
                            />
                        </a-form-item>
                        <a-form-item label="组件介绍" v-bind="waiformItemLayout">
                            <a-textarea
                                style="width: 80%"
                                placeholder="一段简短的组件介绍"
                                v-decorator="['desc', { rules: [{ message: '请输入组件介绍' }] }]"
                            />
                        </a-form-item>
                        <a-form-item label="生成链接格式" v-bind="waiformItemLayout">
                            <a-select
                                :required="true"
                                mode="tags"
                                style="width: 80%"
                                placeholder="使用http协议为http://{domain}/{key}"
                                v-decorator="[
                                    'payload_list',
                                    { rules: [{ required: true, message: '请输入生成链接格式' }] },
                                ]"
                            />
                        </a-form-item>
                        <a-form-item label="配置信息" v-bind="waiformItemLayout" :required="true">
                            <div class="alertContain" v-for="(t, index) in waiArray" :key="index">
                                <a-icon
                                    class="closeIcon"
                                    type="close"
                                    @click="cloneContainer(index)"
                                    v-if="waiArray.length !== 1"
                                />
                                <a-form-item v-bind="formItemLayout" label="配置名" :required="true">
                                    <a-input
                                        style="width: 80%"
                                        placeholder="请输入配置名"
                                        v-decorator="[
                                            `item_name-${t}`,
                                            { rules: [{ required: true, message: '请输入配置名' }] },
                                        ]"
                                    />
                                </a-form-item>
                                <a-form-item
                                    v-for="(k, index) in form.getFieldValue('keys')[t]"
                                    :key="k"
                                    v-bind="index === 0 ? formItemLayout : formItemLayoutWithOutLabel"
                                    :label="index === 0 ? '参数名' : ''"
                                    :required="true"
                                >
                                    <a-input
                                        v-decorator="[
                                            `config[${k}-${t}]`,
                                            {
                                                validateTrigger: ['change', 'blur'],
                                                rules: [
                                                    {
                                                        required: true,
                                                        whitespace: true,
                                                        message: '请输入参数名',
                                                    },
                                                ],
                                            },
                                        ]"
                                        placeholder="请输入参数名"
                                        style="width: 80%"
                                    />
                                    <a-icon
                                        v-if="form.getFieldValue('keys')[t].length > 1"
                                        class="dynamic-delete-button"
                                        type="minus-circle-o"
                                        style="margin-left: 5px; font-size: 20px"
                                        :disabled="form.getFieldValue('keys').length === 1"
                                        @click="() => remove(t, k)"
                                    />
                                    <a-icon
                                        v-if="form.getFieldValue('keys')[t].length - 1 === index"
                                        class="dynamic-delete-button"
                                        type="plus-circle"
                                        style="margin-left: 5px; font-size: 20px"
                                        :disabled="form.getFieldValue('keys').length === 1"
                                        @click="() => add(t)"
                                    />
                                </a-form-item>
                            </div>
                            <a-button type="dashed" style="width: 60%" @click="addwai">
                                <a-icon type="plus" />
                                添加配置信息
                            </a-button>
                        </a-form-item>
                        <a-form-item label="组件类型" v-bind="waiformItemLayout">
                            <a-radio-group
                                v-decorator="['type', { rules: [{ required: true, message: '请选择组件类型' }] }]"
                            >
                                <a-radio :value="1">监听组件</a-radio>
                                <a-radio :value="0">利用组件</a-radio>
                            </a-radio-group>
                        </a-form-item>
                        <a-form-item label="公开组件" v-bind="waiformItemLayout">
                            <a-radio-group
                                v-decorator="[
                                    'is_private',
                                    { rules: [{ required: true, message: '请选择是否公开组件' }] },
                                ]"
                            >
                                <a-radio :value="1">是</a-radio>
                                <a-radio :value="0">否</a-radio>
                            </a-radio-group>
                        </a-form-item>
                        <a-form-item label="配置支持多选" v-bind="waiformItemLayout">
                            <a-radio-group
                                v-decorator="[
                                    'choice_type',
                                    { rules: [{ required: true, message: '请选择是否配置支持多选' }] },
                                ]"
                            >
                                <a-radio :value="1">是</a-radio>
                                <a-radio :value="0">否</a-radio>
                            </a-radio-group>
                        </a-form-item>
                        <a-form-item label="上传插件" v-bind="waiformItemLayout" :required="true">
                            <a-upload
                                @change="fileChage"
                                v-decorator="[
                                    'file_name',
                                    {
                                        valuePropName: 'fileList',
                                        getValueFromEvent: normFile,
                                    },
                                    { rules: [{ required: true, message: '请上传文件' }] },
                                ]"
                                name="code"
                                action="/api/v1/templates/manage/upload_template/"
                                :withCredentials="true"
                                :headers="headers"
                                :multiple="false"
                                accept="text/x-python-script"
                            >
                                <a-button>
                                    <a-icon type="upload" />
                                    点击上传
                                </a-button>
                            </a-upload>
                        </a-form-item>
                        <a-form-item style="position: absolute; right: 10px; bottom: -10px; z-index: 100">
                            <a-button class="mgLeft10" @click="init">取消</a-button>
                            <a-button class="mgLeft10" type="primary" html-type="submit">确定</a-button>
                        </a-form-item>
                    </a-form>
                </div>
                <div class="edtorClass">
                    <a-icon v-show="flag" @click="handleChange(1)" class="edtorIcon" type="lock" theme="twoTone" />
                    <a-icon v-show="!flag" @click="handleChange(2)" class="edtorIcon" type="unlock" theme="twoTone" />
                    <editor
                        v-model="code"
                        :options="{ readOnly: flag }"
                        lang="python"
                        width="600"
                        height="90%"
                        @init="initEditor"
                    ></editor>
                </div>
            </section>
        </a-modal>
    </div>
</template>

<script>
import Service from '@/utils/service/service'
let id = 1
let waiId = 1
export default {
    name: 'newComponents',
    props: {
        visible: false,
        titles: '',
        content: '',
    },
    components: {
        editor: require('vue2-ace-editor'),
    },
    data() {
        return {
            code: '',
            flag: true,
            //上传需要上送header
            headers: { Authorization: `Token ${sessionStorage.getItem('token')}` },
            waiArray: [0], //决定配置 信息框的多少
            waiformItemLayout: {
                labelCol: {
                    sm: { span: 6 },
                },
                wrapperCol: {
                    sm: { span: 18 },
                },
            },
            formItemLayout: {
                labelCol: {
                    sm: { span: 5 },
                },
                wrapperCol: {
                    sm: { span: 19 },
                },
            },
            formItemLayoutWithOutLabel: {
                wrapperCol: {
                    sm: { span: 19, offset: 5 },
                },
            },
            layoutBottomWithOutLabel: {
                wrapperCol: {
                    sm: { span: 8, offset: 16 },
                },
            },
        }
    },
    created() {
        this.form = this.$form.createForm(this, { name: 'dynamic_form_item' })
        if (this.content) {
            //初始化编辑配置
            this.editConfig()
        } else {
            //新增配置
            this.form.getFieldDecorator('keys', { initialValue: [[0]], preserve: true })
        }
    },
    mounted() {},
    methods: {
        handleChange(flag) {
            if (flag === 1) {
                this.flag = false
            } else {
                this.flag = true
            }
        },
        fileChage(file) {
            const files = file.file
            if (files.status === 'done') {
                this.code = files.response.data.code
            }
        },
        initEditor: function (editor) {
            require('brace/mode/python')
            require('brace/theme/chrome')
            require('brace/ext/language_tools')
        },
        editConfig() {
            let keys = []
            this.waiArray = []
            id = 0
            waiId = 0
            this.content.template_item_info.forEach((item) => {
                let arr = []
                this.form.getFieldDecorator(`item_name-${waiId}`, { initialValue: item.item_name })

                item.config.forEach((childitem) => {
                    this.form.getFieldDecorator(`config[${id}-${waiId}]`, { initialValue: childitem })
                    arr.push(id++)
                })
                keys[waiId] = arr
                this.waiArray.push(waiId++)
            })
            this.form.getFieldDecorator('is_private', { initialValue: this.content.is_private, preserve: true })
            this.form.getFieldDecorator('choice_type', { initialValue: this.content.choice_type, preserve: true })
            this.form.getFieldDecorator('desc', { initialValue: this.content.desc, preserve: true })
            this.form.getFieldDecorator('payload_list', { initialValue: this.content.payload_list, preserve: true })
            this.form.getFieldDecorator('title', { initialValue: this.content.title, preserve: true })
            this.form.getFieldDecorator('name', { initialValue: this.content.name, preserve: true })
            this.form.getFieldDecorator('keys', { initialValue: keys, preserve: true })
            this.form.getFieldDecorator('type', { initialValue: this.content.type, preserve: true })
            this.code = this.content.code
        },
        addwai() {
            // 为外层id赋值 增加外层contain框
            const { form } = this
            const keys = form.getFieldValue('keys')
            keys[waiId] = Array.of(id++)
            const nextKeys = keys
            form.setFieldsValue({
                keys: nextKeys,
            })
            this.waiArray.push(waiId++)
        },
        remove(t, k) {
            const { form } = this
            const keys = form.getFieldValue('keys')
            if (keys.length === 1) {
                return
            }
            keys[t] = keys[t].filter((key) => key !== k)
            form.setFieldsValue({
                keys: keys,
            })
        },

        add(t) {
            const { form } = this
            const keys = form.getFieldValue('keys')
            keys[t] = keys[t].concat(id++)
            const nextKeys = keys
            form.setFieldsValue({
                keys: nextKeys,
            })
        },
        cloneContainer(i) {
            this.waiArray.splice(i, 1)
        },
        configInfo(values) {
            let template_item_info = []
            Object.keys(values).forEach((key) => {
                if (key.includes('item_name')) {
                    let arr = []
                    const config = values.config ? values.config : []
                    Object.keys(config).forEach((childkey) => {
                        if (key.split('-')[1] === childkey.split('-')[1]) {
                            arr.push(values.config[childkey])
                        }
                    })
                    template_item_info.push({ item_name: values[key], config: arr })
                    delete values[key]
                }
            })
            delete values.keys
            values.template_item_info = template_item_info
        },
        callingInter(values) {
            if (this.content) {
                Service.update_template({ ...values, template_id: this.content.id, code: this.code }).then((item) => {
                    this.init()
                    this.$parent.initData()
                })
            } else {
                Service.templatesManage({ ...values, code: this.code }).then((item) => {
                    this.init()
                    this.$parent.initData()
                })
            }
        },
        handleSubmit(e) {
            e.preventDefault()
            if (!this.code) {
                this.$message.warn('上传组件不能为空')
                return
            }
            this.form.validateFields((err, values) => {
                if (!err) {
                    this.configInfo(values) //组装配置信息
                    this.callingInter(values) //调用新增编辑接口
                }
            })
        },
        init() {
            this.$parent.content = ''
            this.form.resetFields()
            id = 1
            waiId = 1
            this.$parent.visible = false
        },
        normFile(e) {
            //antvue 1.7.8版本没有限制只能上送一个的api
            if (Array.isArray(e)) {
                return e
            }
            return e && e.fileList.length == 2 ? [e.fileList[1]] : [e.fileList[0]]
        },
    },
}
</script>

<style lang="less" scoped>
.mgLeft10 {
    margin-left: 10px;
}
.edtorClass {
    position: relative;
    .edtorIcon {
        position: absolute;
        z-index: 100;
        right: 0;
        font-size: 20px;
        top: -20px;
        cursor: pointer;
    }
}
.alertContain {
    border: 1px solid #e8e8e8;
    position: relative;
    padding-top: 30px;
    margin-top: 10px;
    width: 342px;
    .closeIcon {
        font-size: 20px;
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
    }
}
</style>
