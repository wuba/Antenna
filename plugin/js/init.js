
// 加载background的函数

var element = layui.element,
    layer = layui.layer,
    $ = layui.$,
    form = layui.form,
    table = layui.table

// 对象深拷贝, 按值传递
// layui的table修改了原始字典, 浅拷贝会导致修改不成功
var deepCopy = data => {
    // 处理空数据
    if (!data) {
        data = []
    }
    return JSON.parse(JSON.stringify(data))
}


// 解决因CSP原因导致的javascript:;报错问题
$(document).on('click', "a[href='javascript:;']", e => {
    return false
})

