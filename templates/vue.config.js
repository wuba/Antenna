const webpack = require('webpack')
const reqUrl = process.env.SERVER_URL ? process.env.SERVER_URL : ''
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

    configureWebpack: (config) => {
        config.plugins.push(
            new webpack.DefinePlugin({
                reqUrl: JSON.stringify(reqUrl),
            })
        )
    },
    //http://42.187.161.143/aaa#/user/login
    lintOnSave: false, //关闭eslintre语法检查
    devServer: {
        open: true,
        disableHostCheck: true,
        proxy: {
            '^/api': {
                target: 'http://42.187.161.143', //后端地址
                ws: true, //是否代理websockets
                changeOrigin: true,
            },
        },
    },
}

module.exports = vueConfig
