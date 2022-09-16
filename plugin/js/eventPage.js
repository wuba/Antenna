chrome.notifications.onButtonClicked.addListener((notificationId, index) => {
    chrome.browserAction.setBadgeText({text: "0"});
    chrome.notifications.clear(notificationId)
    if(index === 0){
        chrome.storage.sync.get(['apikey', 'server'], function (budge) {
            var server = budge.server
            var apikey = budge.apikey
            var messageinfo = server + '/api/v1/messages/manage/api/?apikey=' + apikey

            chrome.tabs.create({url: messageinfo})
        })
    }

});
chrome.notifications.onClosed.addListener(function (data) {
    chrome.browserAction.setBadgeText({text: "0"});


});


const payload_parent_contextMenu = {
    id: "payload_parent",
    title: "选择Antenna-Payload",
    contexts: ["all"]
};
chrome.contextMenus.create(payload_parent_contextMenu);


var get_payload = () => {
    chrome.storage.sync.get(['apikey', 'server'], function (budge) {
        var server = budge.server
        var apikey = budge.apikey
        var payloadinfo = server + '/api/v1/tasks/configs/api/?apikey=' + apikey
        var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
        httpRequest.open('GET', payloadinfo, true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
        httpRequest.send();//第三步：发送请求  将请求参数写在URL中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function () {
            if (httpRequest.status === 200) {
                var response = JSON.parse(httpRequest.responseText);//获取到json字符串，还需解析
                var element = response["data"];
                for (i in element["payload"]) {
                    var payload = element["payload"][i];
                    var payload_child_contextMenu = {
                        id: payload.toString(),
                        title: payload.toString(),
                        parentId: "payload_parent",
                    }
                    chrome.contextMenus.create(payload_child_contextMenu);

                }

            }


        }
    })

};


get_payload();

//2、为contextMenus添加点击事件的监听
chrome.contextMenus.onClicked.addListener(function (clickDate) {
    // clickDate.menuItemId: 菜单选项卡的id
    // clickDate.selectionText:选中改的内容
    if (clickDate.parentMenuItemId === "payload_parent") {
        var textarea = document.createElement('textarea');
        document.body.appendChild(textarea);
        // 隐藏此输入框
        textarea.style.position = 'fixed';
        textarea.style.clip = 'rect(0 0 0 0)';
        textarea.style.top = '10px';
        // 赋值
        textarea.value = clickDate.menuItemId;
        // 选中
        textarea.select();
        // 复制
        document.execCommand('copy', true);
        // 移除输入框
        document.body.removeChild(textarea);
    }


});

//监听滑动按钮开启
var get_message = () => {
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    chrome.storage.sync.get(['apikey', 'server'], function (budge) {
            var server = budge.server
            var apikey = budge.apikey
            var messageinfo = server + '/api/v1/messages/manage/api/?apikey=' + apikey
            httpRequest.open('GET', messageinfo, true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
            httpRequest.send();//第三步：发送请求  将请求参数写在URL中
            /**
             * 获取数据后的处理程序
             */
            httpRequest.onreadystatechange = function () {
                if (httpRequest.status === 200) {
                    var response = JSON.parse(httpRequest.responseText);//获取到json字符串，还需解析
                    var element = response["data"];
                    var message_new_count = parseInt(element["count"])
                    chrome.storage.sync.get("message_count", function (budge) {
                            if (budge.message_count) {
                                var message_count = budge.message_count

                            } else {
                                var message_count = 0
                            }
                            if (message_new_count > message_count) {
                                if (message_count === 0) {
                                    chrome.browserAction.setBadgeText({text: "0"});
                                } else {
                                    const notifyOptions = {
                                        //type 有四种类型，basic\image\simple\list
                                        type: 'basic',
                                        title: 'antenna消息提示',
                                        iconUrl: 'img/logo.png',
                                        message: '您有一条新的请求记录',
                                        buttons: [{title: "消息详情"}, {title: "我知道了"}],
                                        isClickable: true,
                                        requireInteraction: true
                                    };
                                    chrome.browserAction.setBadgeText({text: (message_new_count - message_count).toString()});
                                    chrome.notifications.create(notifyOptions);
                                }
                                chrome.browserAction.setBadgeBackgroundColor({color: '#a80f71'});
                            }
                            chrome.storage.sync.set({"message_count": message_new_count});
                        }
                    )

                }
            }
        }
    )

}




chrome.storage.sync.get("message_type", function (budge) {
    if (budge.message_type === 1) {
        a = window.setInterval(get_message, 4000)
    } else {
        window.clearInterval(a)

    }
})

var a = null;
chrome.storage.onChanged.addListener(function (changes, storageName) {
    if (changes.message_type.newValue === 1) {
        a = window.setInterval(get_message, 4000)
    } else {
        window.clearInterval(a)

    }

});




