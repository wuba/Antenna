/* eslint-disable no-console */

// web容器服务

const express = require('express')
const path = require('path')

const app = express()

app.use(express.static(path.join(__dirname, '../dist')))

app.get('/*', (req, res) => {
    console.log('request path:', req.path)
    res.sendFile(path.join(__dirname, '../dist', 'index.html'))
})

app.listen(8000, (err) => {
    console.log('---Antenna start, listening on port 8000---')
    if (typeof err !== 'undefined') {
        console.log(err)
    }
})
