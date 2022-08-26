const vueConfig = {
    productionSourceMap: false,
    css: {
        loaderOptions: {
            less: {
                modifyVars: {
                    'border-radius-base': '2px',
                },
                javascriptEnabled: true,
            },
        },
    },
    lintOnSave: false, //关闭eslintre语法检查
    devServer: {
        open: true,
        disableHostCheck: true,
        proxy: {
            '^/api': {
                target: 'http://127.0.0.1:8000', //后端地址
                ws: true, //是否代理websockets
                changeOrigin: true,
            },
        },
    },
}

module.exports = vueConfig
