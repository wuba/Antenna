// const webpack = require('webpack')
// const reqUrl = process.env.PLATFORM_DOMAIN ? `http://${process.env.PLATFORM_DOMAIN}` : '/'
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

    // configureWebpack: (config) => {
    //     config.plugins.push(
    //         new webpack.DefinePlugin({
    //             reqUrl: JSON.stringify(reqUrl.toString()),
    //         })
    //     )
    // },
    lintOnSave: false, //关闭eslintre语法检查
    devServer: {
        open: true,
        disableHostCheck: true,
        proxy: {
            '^/api': {
                target: 'http://10.176.237.165', //后端地址
                ws: true, //是否代理websockets
                changeOrigin: true,
            },
        },
    },
}

module.exports = vueConfig