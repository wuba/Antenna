$(function () {
    chrome.storage.sync.get('total', function (budget) {
        $('#total').text(budget.total);
    })
    $('#add').click(function () {
        chrome.storage.sync.get(['total', 'limit'], function (budget) {
            var totalAmount = 0;
            if (budget.total) {
                totalAmount = parseFloat(budget.total)
            }
            //2、将本次金额加到总金额并存储
            var mount = $("#amount").val();
            if (mount) {
                totalAmount += parseFloat(mount);
                chrome.storage.sync.set({'total': totalAmount}, function () {
                    if (totalAmount > parseFloat(budget.limit)) {
                        const notifyOptions = {
                            //type 有四种类型，basic\image\simple\list
                            type: 'basic',
                            title: 'antenna消息提示',
                            iconUrl: 'img/logo.png',
                            message: '您有一条新的请求记录'
                        };
                        chrome.notifications.create('limitNotify', notifyOptions);
                    }
                });
            }
            //3、更新显示UI
            $('#total').text(totalAmount)
            $('#amount').val('')

        })

    })

    $('a.layui-btn[href]').click(e => {
        chrome.tabs.create({url: $(e.target).attr('href')})
    })


    //监听设置按钮
    $('#btn_option').click(function () {
        window.close()
        var url = 'options.html'
        chrome.tabs.create({url: url})
    })


    $('#btn_result').click(function () {
        window.close()
        chrome.storage.sync.get(['apikey', 'server'], function (budge) {
            var server = budge.server
            var apikey = budge.apikey
            var messageinfo = server + '/api/v1/messages/manage/api/?apikey=' + apikey

            chrome.tabs.create({url: messageinfo})
        })
    })


});

const extstatus = (method = false) => {
    if (method !== false) {
        localStorage.setItem('extstatus', method)
    }
    return localStorage.getItem('extstatus')
};


if (extstatus() === 'on') {
    $('#status + div').click()

}

layui.use(['form'], function () {
    form = layui.form
    form.on('switch(switchStatus)', function (data) {
        extstatus(this.checked ? 'on' : '')
        if (this.checked) {
            chrome.storage.sync.set({'message_type': 1})
        } else {
            chrome.storage.sync.set({'message_type': 0})
        }
    })
})



