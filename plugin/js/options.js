
$(function () {
    chrome.storage.sync.get(['apikey', 'server'], function (budge) {
        $("#apikey").val(budge.apikey);
        $("#server").val(budge.server)
    })

    $('#save').click(function () {
        var apikey = $('#apikey').val();
        var server = $('#server').val();
        if (apikey && server) {
            chrome.storage.sync.set({"apikey": apikey, "server": server}
            )

        }
    });

    $('#reset').click(function () {
        chrome.storage.sync.set({"apikey": "", "server": ""});

    });

    layui.use('element', function () {
        var element = layui.element;
    });


})
;



