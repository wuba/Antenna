<template>
    <div>
        <a-drawer
            :title="title"
            placement="right"
            :closable="id ? true : false"
            :visible.sync="visible"
            @close="onClose"
            width="40%"
            wrapClassName="wb-drawer-div"
            :destroyOnClose="true"
            :maskClosable="id ? true : false"
            :drawerStyle="drawerBodyStyle"
        >
            <a-card :bordered="false" class="wb-m-b-30 clearfix border-radius-5">
                <div slot="title">
                    <a-icon twoToneColor="#eb0806" type="crown" theme="twoTone" class="wb-m-r-5" />
                    任务
                    <a-tooltip>
                        <template slot="title">关于监听的介绍</template>
                        <a-icon type="info-circle" />
                    </a-tooltip>
                    <a-button v-if="id" icon="to-top" class="wb-m-r-5 float-right" size="small" @click="submitAddName">
                        保存
                    </a-button>
                </div>
                <a-form-model
                    ref="taskNameForm"
                    :model="taskNameForm"
                    :rules="rules"
                    :label-col="labelCol"
                    :wrapper-col="wrapperCol"
                >
                    <a-form-model-item ref="name" prop="name">
                        <span slot="label">任务名称</span>
                        <a-input v-model="taskNameForm.name" />
                    </a-form-model-item>
                    <a-form-model-item ref="callback_url" prop="callback_url">
                        <span slot="label">首页关注</span>
                        <a-switch v-model="taskNameForm.show_dashboard" />
                        <a-button
                            style="float: right; font-size: 16px"
                            type="link"
                            @click="
                                () => {
                                    downAdUp = !downAdUp
                                }
                            "
                        >
                            高级配置
                            <a-icon type="down" v-if="downAdUp" />
                            <a-icon type="up" v-else />
                        </a-button>
                    </a-form-model-item>
                    <a-form-model-item ref="zzz" prop="zzz" v-show="!downAdUp">
                        <span slot="label">通知接口</span>
                        <a-input v-model="taskNameForm.callback_url" />
                    </a-form-model-item>
                    <a-form-model-item ref="xxx" prop="xxx" v-show="!downAdUp">
                        <span slot="label">接口header</span>
                        <a-input v-model="taskNameForm.callback_url_headers" />
                    </a-form-model-item>
                </a-form-model>
            </a-card>
            <a-card :bordered="false" class="wb-m-b-30 border-radius-5">
                <div slot="title" class="clearfix">
                    <a-icon type="notification" theme="twoTone" class="wb-m-r-5" />
                    监听组件
                    <a-tooltip>
                        <template slot="title">关于监听的介绍</template>
                        <a-icon type="info-circle" />
                    </a-tooltip>
                    <a-button icon="plus" class="wb-m-r-5 float-right" size="small" @click="openAddDomain(null, 1)">
                        新建
                    </a-button>
                </div>
                <a-form-model
                    ref="dynamicValidateForm"
                    class="wb-form-drawer"
                    :model="dynamicValidateForm"
                    v-bind="formItemLayoutWithOutLabel"
                >
                    <a-form-model-item
                        v-for="(domain, index) in dynamicValidateForm.domains"
                        :key="index"
                        :ref="'domains.' + index + '.value'"
                    >
                        <a-row :gutter="3" class="tipTop">
                            <a-col :span="4">
                                <a-button block type="primary" ghost>{{ domain.template_name }}</a-button>
                            </a-col>
                            <a-col :span="16">
                                <a-input v-model="domain.key" placeholder="请输入域名" :readOnly="true">
                                    <my-copy slot="suffix" :text="domain.key"></my-copy>
                                </a-input>
                            </a-col>
                            <a-col :span="1">
                                <a-icon class="dynamic-delete-button" type="edit" @click="openAddDomain(domain, 1)" />
                            </a-col>
                            <a-col :span="1">
                                <a-icon
                                    class="dynamic-delete-button"
                                    type="minus-circle-o"
                                    @click="removeDomain(domain, 1)"
                                />
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                </a-form-model>
            </a-card>
            <a-card :bordered="false" class="wb-m-b-30 border-radius-5">
                <div slot="title" class="clearfix">
                    <a-icon type="thunderbolt" theme="twoTone" class="wb-m-r-5" />
                    利用组件
                    <a-tooltip>
                        <template slot="title">关于监听的介绍</template>
                        <a-icon type="info-circle" />
                    </a-tooltip>
                    <a-button icon="plus" class="wb-m-r-5 float-right" size="small" @click="openAddDomain(null, 0)">
                        新建
                    </a-button>
                </div>
                <a-form-model
                    ref="dynamicValidateForm"
                    class="wb-form-drawer"
                    :model="dynamicValidateForm"
                    v-bind="formItemLayoutWithOutLabel"
                >
                    <a-form-model-item
                        v-for="(domain, index) in dynamicValidateForm.utilize"
                        :key="index"
                        :ref="'utilize.' + index + '.value'"
                    >
                        <a-row :gutter="3">
                            <a-col :span="22" class="contain">
                                <template>
                                    <a-tooltip>
                                        <template slot="title">
                                            {{ domain.template_name }}
                                        </template>
                                        <a-button block type="primary" ghost class="b titileButton">
                                            <div class="overflow">{{ domain.template_name }}</div>
                                        </a-button>
                                    </a-tooltip>
                                </template>
                                <a-input
                                    style="width: 80%"
                                    class="marginright3"
                                    v-model="domain.key"
                                    placeholder="请输入域名"
                                    :readOnly="true"
                                >
                                    <my-copy slot="suffix" :text="domain.key"></my-copy>
                                </a-input>
                                <a-icon
                                    class="dynamic-delete-button marginright3"
                                    type="edit"
                                    @click="openAddDomain(domain, 0)"
                                />
                                <a-icon
                                    class="dynamic-delete-button"
                                    type="minus-circle-o"
                                    @click="removeDomain(domain, 2)"
                                />
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                </a-form-model>
            </a-card>
            <div class="footBtn">
                <a-button v-if="!id" @click="onClose" class="wb-m-r-5">取消</a-button>
                <a-button v-if="!id" @click="onSure" class="wb-m-r-5">确定</a-button>
            </div>
        </a-drawer>
        <a-modal v-model="addModalVisible" title="配置" @ok="addConfigureOk" @cancel="onCloseAddDomain">
            <a-form-model ref="ruleForm" :model="form" :rules="rules" :label-col="labelCol" :wrapper-col="wrapperCol">
                <a-form-model-item ref="template" label="组件" prop="template">
                    <a-select v-model="form.template" placeholder="请选择组件" @change="selectManage">
                        <a-select-option v-for="i in manageData" :key="i.value" :value="i.value">
                            {{ i.lable }}
                        </a-select-option>
                    </a-select>
                </a-form-model-item>
                <div v-if="isSingleConfig">
                    <a-form-model-item label="配置" prop="configs">
                        <a-select v-model="form.configs" placeholder="请选择配置" @change="selectConfig($event)">
                            <a-select-option v-for="i in regionData" :key="i.value" :value="i.value">
                                {{ i.lable }}
                            </a-select-option>
                        </a-select>
                    </a-form-model-item>
                    <div v-if="form.singConfigs.length">
                        <a-form-model-item v-for="(it, k) in form.singConfigs" :key="k" :label="it.name">
                            <a-input v-model="it.value"></a-input>
                        </a-form-model-item>
                    </div>
                </div>
                <div v-else>
                    <div v-for="(domain, index) in form.domains" :key="index">
                        <a-form-model-item label="配置" :rules="rules1">
                            <a-row :gutter="3">
                                <a-col :span="20">
                                    <a-select
                                        :ref="'domains.' + index + '.value'"
                                        :prop="'domains.' + index + '.value'"
                                        v-model="domain.configs"
                                        placeholder="请选择配置"
                                        @change="selectConfig($event, index)"
                                        @blur="upDataValidateField(index)"
                                    >
                                        <a-select-option v-for="i in regionData" :key="i.value" :value="i.value">
                                            {{ i.lable }}
                                        </a-select-option>
                                    </a-select>
                                </a-col>
                                <a-col :span="2" class="Textright">
                                    <a-icon
                                        class="dynamic-delete-button"
                                        type="plus-circle-o"
                                        :disabled="form.domains.length === 1"
                                        @click="addDomain(domain)"
                                    />
                                </a-col>
                                <a-col :span="2" class="Textright">
                                    <a-icon
                                        v-if="form.domains.length > 1"
                                        class="dynamic-delete-button"
                                        type="minus-circle-o"
                                        :disabled="form.domains.length === 1"
                                        @click="removeConfig(index)"
                                    />
                                </a-col>
                            </a-row>
                        </a-form-model-item>
                        <div v-if="domain.value.length">
                            <a-form-model-item v-for="(it, k) in domain.value" :key="k" :label="it.name">
                                <a-input v-model="it.value"></a-input>
                            </a-form-model-item>
                        </div>
                    </div>
                </div>
                <a-form-model-item label="生成链接" prop="configs">
                    <a-select v-model="form.url_template" placeholder="请选择生成链接" @change="changeLink">
                        <a-select-option v-for="i in linkList" :key="i.id" :value="i.id">
                            {{ i.payload }}
                        </a-select-option>
                    </a-select>
                </a-form-model-item>
            </a-form-model>
        </a-modal>
    </div>
</template>

<script>
import MyCopy from '@/components/copy.vue'
import Service from '@/utils/service/service'
import Driver from 'driver.js'
export default {
    props: {
        visible: false,
        id: null,
    },
    components: {
        MyCopy,
    },
    data() {
        return {
            title: '新建',
            downAdUp: true,
            // 新增编辑的弹窗
            addModalVisible: false,
            labelCol: { span: 5 },
            wrapperCol: { span: 18 },
            wrapperCol1: { span: 3, offset: 21 },
            form: {
                url_template: undefined,
                template: undefined,
                configs: undefined,
                domains: [
                    {
                        configs: '',
                        value: [],
                    },
                ],
                singConfigs: [
                    // {name:'ip', value:''},
                    // {name:'port', value:'666'},
                ],
                task_config_id: undefined,
            },
            rules: {
                template: [{ required: true, message: '组件必填', trigger: 'blur' }],
                configs: [{ required: true, message: '配置必填', trigger: 'change' }],
                name: [{ required: true, message: '任务名称必填', trigger: 'change' }],
            },
            rules1: [{ required: true, message: '必填', trigger: 'blur' }],
            // 查看详情的
            visibleDetail: false,
            //
            drawerBodyStyle: {
                background: '#ededed',
            },
            formItemLayoutWithOutLabel: {
                wrapperCol: {
                    xs: { span: 24, offset: 0 },
                    sm: { span: 20, offset: 2 },
                },
            },
            dynamicValidateForm: {
                domains: [],
                utilize: [],
            },
            taskNameForm: {
                name: '',
                callback_url: '',
                callback_url_headers: '',
                show_dashboard: true,
            },
            manageData: [],
            manageDataChoice: {},
            configDataChoice: {},
            regionData: [],
            linkList: [],
            onSubmitLoading: false,
            isSingleConfig: true,
            task_id: '',
            modalType: null, // 弹窗操作类型  1 ==> 修改   2 ==> 新建
        }
    },
    created() {
        this.initData()
    },
    methods: {
        initData() {
            if (this.id) {
                this.title = '编辑'
                this.task_id = this.id
                this.getData(this.id, 1)
            } else {
                Service.create_tmp_task().then(
                    (res) => {
                        if (res.code === 1) {
                            this.task_id = res.data.task_info.task_id
                            this.taskNameForm.name = res.data.task_info.task_name
                            this.taskNameForm.callback_url = res.data.task_info.callback_url
                            this.taskNameForm.callback_url_headers = res.data.task_info.callback_url_headers
                            this.taskNameForm.show_dashboard = res.data.task_info.show_dashboard

                            this.dynamicValidateForm.domains = res.listen_template_info
                            this.dynamicValidateForm.utilize = res.payload_template_info
                        } else {
                            this.$message.error(res.message)
                            this.onClose()
                        }
                    },
                    (err) => {
                        this.onClose()
                    }
                )
            }
        },
        getData(id) {
            Service.getTasksConfigs({ task: id }).then(
                (res) => {
                    if (res.code === 1) {
                        let {
                            data: { task_info, payload_template_info, listen_template_info },
                        } = res
                        this.taskNameForm.name = task_info.task_name
                        this.taskNameForm.callback_url = task_info.callback_url
                        this.taskNameForm.callback_url_headers = task_info.callback_url_headers
                        this.taskNameForm.show_dashboard = task_info.show_dashboard
                        this.dynamicValidateForm.domains = listen_template_info
                        this.dynamicValidateForm.utilize = payload_template_info
                    } else {
                        this.$message.error(res.message)
                        this.onClose()
                    }
                    this.initTip()
                },
                (err) => {
                    this.onClose()
                }
            )
        },
        initTip() {
            //新手导航
            let flag = sessionStorage.getItem('firstLogin')
            if (flag == 'true') {
                const driver = new Driver({ animate: false, allowClose: false })
                let timer = setTimeout(() => {
                    let out = true
                    driver.defineSteps([
                        {
                            element: document.getElementsByClassName('tipTop')[0],
                            popover: {
                                title: '组件链接',
                                description: '新建与编辑组件可获取到可以使用的链接',
                                position: 'bottom',
                            },
                            showButtons: true,
                            doneBtnText: '下一步',
                            closeBtnText: '跳出',
                            onNext: () => {
                                out = false
                                this.$router.push({ path: '/components' })
                            },
                            onDeselected: () => {
                                if (out) {
                                    sessionStorage.setItem('firstLogin', 'false')
                                }
                            },
                        },
                    ])
                    driver.start()
                    clearTimeout(timer)
                }, 100)
            }
        },
        addConfigureOk() {
            this.$refs.ruleForm.validate((valid) => {
                if (valid) {
                    let data = {
                        task: this.task_id,
                        template: this.form.template,
                        url_template: this.form.url_template,
                        template_config_item_list: [],
                    }
                    if (this.isSingleConfig) {
                        data.template_config_item_list.push({
                            template_config_item: this.form.configs,
                        })
                        if (this.form.singConfigs.length) {
                            let len1 = this.form.singConfigs.length,
                                obj = {}
                            for (let i = 0; i < len1; i++) {
                                obj[this.form.singConfigs[i].name] = this.form.singConfigs[i].value
                            }
                            data.template_config_item_list[0].value = obj
                        }
                    } else {
                        let len2 = this.form.domains.length
                        for (var i = 0; i < len2; i++) {
                            let obj1 = {}
                            obj1.template_config_item = this.form.domains[i].configs
                            obj1.value = this.handleData(this.form.domains[i].value)
                            // console.log(this.handleData(this.form.domains[i].value), '这是处理完的的数据');
                            data.template_config_item_list.push(obj1)
                        }
                    }
                    // console.log(data, '=== 请求的参数', this.form)
                    if (this.modalType === 1) {
                        data.task_config = this.form.task_config_id
                        if (this.id) {
                            Service.getTasksConfigsUpdate(data).then((res) => {
                                if (res.code === 1) {
                                    let {
                                        data: { listen_template_info, payload_template_info },
                                    } = res
                                    this.dynamicValidateForm.domains = listen_template_info
                                    this.dynamicValidateForm.utilize = payload_template_info
                                    this.$message.success('操作成功')
                                    this.onCloseAddDomain()
                                    this.form.task_config_id = null
                                } else {
                                    this.$message.error(res.message)
                                }
                            })
                        } else {
                            Service.tmp_update_config(data).then((res) => {
                                if (res.code === 1) {
                                    let {
                                        data: { listen_template_info, payload_template_info },
                                    } = res
                                    this.dynamicValidateForm.domains = listen_template_info
                                    this.dynamicValidateForm.utilize = payload_template_info
                                    this.$message.success('操作成功')
                                    this.onCloseAddDomain()
                                    this.form.task_config_id = null
                                } else {
                                    this.$message.error(res.message)
                                }
                            })
                        }
                    } else {
                        if (this.id) {
                            Service.getTasksConfigsAdd(data).then((res) => {
                                if (res.code === 1) {
                                    let {
                                        data: { listen_template_info, payload_template_info },
                                    } = res
                                    this.dynamicValidateForm.domains = listen_template_info
                                    this.dynamicValidateForm.utilize = payload_template_info
                                    this.$message.success('操作成功')
                                    this.onCloseAddDomain()
                                } else {
                                    this.$message.error(res.message)
                                }
                            })
                        } else {
                            Service.tasks_tmp(data).then((res) => {
                                if (res.code === 1) {
                                    let {
                                        data: { listen_template_info, payload_template_info },
                                    } = res
                                    this.dynamicValidateForm.domains = listen_template_info
                                    this.dynamicValidateForm.utilize = payload_template_info
                                    this.$message.success('操作成功')
                                    this.onCloseAddDomain()
                                } else {
                                    this.$message.error(res.message)
                                }
                            })
                        }
                    }
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        },
        onClose() {
            this.dynamicValidateForm.domains = []
            this.dynamicValidateForm.utilize = []
            this.$refs.taskNameForm.resetFields()
            this.id ? null : Service.cancel_tmp_task({ task_id: this.task_id })
            this.task_id = null
            this.$emit('editEvent', { event: false, id: this.id })
        },
        onSure() {
            if (!this.id) {
                if (this.taskNameForm.name == '') {
                    this.$message.error('任务名称不能为空')
                    return
                }
                Service.getCreatTask({
                    task_id: this.task_id,
                    task_name: this.taskNameForm.name,
                    callback_url: this.taskNameForm.callback_url,
                    callback_url_headers: this.taskNameForm.callback_url_headers,
                    show_dashboard: this.taskNameForm.show_dashboard,
                }).then((res) => {
                    if (res.code === 1) {
                        this.$message.success('保存成功')
                    }
                })
            }
            this.dynamicValidateForm.domains = []
            this.dynamicValidateForm.utilize = []
            this.$refs.taskNameForm.resetFields()
            this.task_id = null
            this.$emit('editEvent', { event: false, id: this.id })
        },
        submitAddName() {
            this.$refs.taskNameForm.validate((valid) => {
                if (valid) {
                    // console.log(this.taskNameForm, '要保存的数据')
                    let data = {
                        name: this.taskNameForm.name,
                        callback_url: this.taskNameForm.callback_url,
                        callback_url_headers: this.taskNameForm.callback_url_headers,
                        show_dashboard: this.taskNameForm.show_dashboard,
                    }
                    Service.getTasksManageEdit(this.task_id, data).then((res) => {
                        // console.log('res, 保存名称成功', res)
                        if (res.code === 1) {
                            this.$message.success('操作成功')
                        } else {
                            this.$message.error('操作成功')
                        }
                    })
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        },
        removeConfig(key) {
            this.form.domains.splice(key, 1)
        },
        removeDomain(item, type) {
            let _this = this
            this.$confirm({
                title: '提示',
                content: '确认删除',
                onOk() {
                    if (_this.id) {
                        Service.getTasksConfigsDel(item.task_config_id).then((res) => {
                            if (res.code === 1) {
                                _this.$message.success('操作成功')
                                let index =
                                    type === 1
                                        ? _this.dynamicValidateForm.domains.indexOf(item)
                                        : _this.dynamicValidateForm.utilize.indexOf(item)
                                if (index !== -1) {
                                    type === 1
                                        ? _this.dynamicValidateForm.domains.splice(index, 1)
                                        : _this.dynamicValidateForm.utilize.splice(index, 1)
                                }
                            } else {
                                _this.$message.error(res.massage)
                            }
                        })
                    } else {
                        Service.tmp_delete_config(item.task_config_id).then((res) => {
                            // console.log(res, '要删除的信息 的返回值', item);
                            if (res.code === 1) {
                                _this.$message.success('操作成功')
                                let index =
                                    type === 1
                                        ? _this.dynamicValidateForm.domains.indexOf(item)
                                        : _this.dynamicValidateForm.utilize.indexOf(item)
                                if (index !== -1) {
                                    type === 1
                                        ? _this.dynamicValidateForm.domains.splice(index, 1)
                                        : _this.dynamicValidateForm.utilize.splice(index, 1)
                                }
                            } else {
                                _this.$message.error(res.massage)
                            }
                        })
                    }
                },
                onCancel() {},
            })
        },
        getLinkList(template) {
            Service.linkList({ template: template }).then((res) => {
                this.linkList = res?.data?.results
            })
        },
        changeLink(i) {
            this.form.url_template = i
        },
        openAddDomain(item, type) {
            if (item?.template) {
                this.getLinkList(item.template)
            }
            // console.log(item, '编辑的时候的数据', this.form)
            Service.getTemplatesManage({ type }).then((res) => {
                if (res.code === 1) {
                    if (item) {
                        this.modalType = 1
                        this.getConfigSelectData(item.template)
                        this.hanlderEidtData(item)
                    } else {
                        this.modalType = 2
                    }
                    this.addModalVisible = true
                    this.manageData = []
                    this.manageDataChoice = {}
                    let {
                            data: { results },
                        } = res,
                        len = results.length
                    for (let i = 0; i < len; i++) {
                        let o = {
                            lable: results[i].name,
                            value: results[i].id,
                        }
                        // this.manageDataChoice[results[i].name] = results[i].choice_type
                        this.manageDataChoice[results[i].id] = results[i].choice_type
                        this.manageData.push(o)
                    }
                } else {
                    this.$message.error(res.message)
                }
            })
        },
        hanlderEidtData(item) {
            this.form.template = item.template
            this.form.url_template = item.url_template

            this.form.task_config_id = item.task_config_id
            if (item.template_choice_type === 1) {
                this.isSingleConfig = false
                let data = item.task_config_item_list,
                    len = data.length
                if (len) {
                    this.form.domains = []
                    for (let i = 0; i < len; i++) {
                        let obj = { value: [] },
                            { value } = data[i]
                        obj.configs = data[i].template_config_item
                        Object.keys(value).forEach(function (key) {
                            let o = {}
                            o.name = key
                            o.value = value[key]
                            obj.value.push(o)
                        })
                        this.form.domains.push(obj)
                    }
                }
            } else {
                this.isSingleConfig = true
                this.form.configs = item.task_config_item_list[0].template_config_item
                let data = item.task_config_item_list[0].value,
                    _this = this
                if (JSON.stringify(data) == '{}') {
                    this.form.singConfigs = []
                } else {
                    Object.keys(data).forEach(function (key) {
                        let obj = {}
                        obj.name = key
                        obj.value = data[key]
                        _this.form.singConfigs.push(obj)
                    })
                }
            }
        },
        selectManage(i) {
            if (this.manageDataChoice[i] === 1) {
                this.isSingleConfig = false
            } else {
                this.isSingleConfig = true
            }
            this.form.singConfigs = []
            this.form.domains = [
                {
                    configs: '',
                    value: [],
                },
            ]
            this.form.configs = this.form.configs ? '' : this.form.configs
            this.getConfigSelectData(this.form.template)
            this.getLinkList(i)
            this.form.url_template = undefined
        },
        getConfigSelectData(data) {
            Service.getTemplatessConfigs({ template: data }).then((res) => {
                if (res.code === 1) {
                    this.regionData = []
                    this.configDataChoice = {}
                    let {
                            data: { results },
                        } = res,
                        len = results.length
                    for (let i = 0; i < len; i++) {
                        let o = {
                            lable: results[i].name,
                            value: results[i].id,
                        }
                        this.configDataChoice[results[i].id] = results[i].config
                        this.regionData.push(o)
                    }
                }
            })
        },
        selectConfig(i, d) {
            let len = this.configDataChoice[i].length,
                data = this.configDataChoice[i]
            if (this.isSingleConfig) {
                this.form.singConfigs = []
                for (let i = 0; i < len; i++) {
                    let o = {
                        name: data[i],
                        value: '',
                    }
                    this.form.singConfigs.push(o)
                }
            } else {
                this.form.domains[d].value = []
                if (len) {
                    for (let i = 0; i < len; i++) {
                        let o = {
                            name: data[i],
                            value: '',
                        }
                        this.form.domains[d].value.push(o)
                    }
                }
            }
        },
        upDataValidateField(index) {
            let name = 'domains.' + index + '.value'
            this.$refs.ruleForm.validateField(name)
        },
        onCloseAddDomain() {
            this.form.singConfigs = []
            this.$nextTick(() => {
                this.modalType = null
                this.form.template = undefined
                this.form.configs = undefined
                this.form.domains = [
                    {
                        configs: '',
                        value: [],
                    },
                ]
            })
            this.isSingleConfig = true
            this.regionData = []
            this.addModalVisible = false
            this.$refs.ruleForm.resetFields()
        },
        addDomain() {
            this.form.domains.push({
                configs: null,
                value: [],
                key: Date.now(),
            })
        },
        resetForm() {
            this.$refs.ruleForm.resetFields()
        },
        handleData(data) {
            let len = data.length,
                obj = {}
            if (len === 0) return obj
            for (let i = 0; i < len; i++) {
                obj[data[i].name] = data[i].value
            }
            return obj
        },
    },
}
</script>

<style>
.border-radius-5 {
    border-radius: 5px;
}
.contain {
    display: flex;
    align-items: center;
}
.marginright3 {
    margin-right: 3px;
}
.titileButton {
    width: 19.5%;
    margin-right: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.overflow {
    width: 34px;
    overflow: hidden;
    box-sizing: border-box;
    text-overflow: ellipsis;
    text-align: center;
}
</style>
