$(function () {
    if (!(navigator.userAgent.match(/(iPhone|iPod|Android|ios|iOS|iPad|Backerry|WebOS|Symbian|Windows Phone|Phone)/i)))
        $("[data-toggle='tooltip']").tooltip('show');
    else
        $('#num').hide();
    $('#counter').countdown({
        image: '/static/img/digits.png?v=4d1be4107454712a87e242adba4ec00b',
        startTime: '00:00',
        timerEnd: function () {}, format: 'mm:ss'
    });
    jQuery.curCSS = jQuery.css;
    getNum();
    setInterval(getNum, 10000);
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 60
    });
    $('#domainlist li').click(function () {
        $('#showmail').text($('#showmail').text().substr(0, $('#showmail').text().indexOf('@')) + '@' + $(this).text());
        $('#maildomain').val($(this).text());
    });
    $('#maildomain').dblclick(function (e) {
        if (e.ctrlKey) $(this).removeAttr('readOnly');
    });
    ZeroClipboard.config({
        swfPath: '/static/js/ZeroClipboard.swf?v=8fd7d9fc98662feb6211e6dcae9e7485'
    });
    var client = new ZeroClipboard($('#copyMail'));
    client.on("copy", function (event) {
        event.clipboardData.setData("text/plain", $('#showmail').text());
    });
    var _getMail_;
    var __o_o__ = true;
    var __0_0__ = false;
    $('#applyMail').click(function () {
        if (!/^[A-Za-z0-9]*$/.test($('#mailuser').val())) {
            BootstrapDialog.alert({
                title: '邮箱错误',
                message: '邮箱名只支持字母及数字',
                type: BootstrapDialog.TYPE_WARNING,
                closable: true,
                buttonLabel: '确定',
                callback: function (result) {}
            });
            return;
        }
        $.post("/applymail", {
            mail: $('#mailuser').val() + '@' + $('#maildomain').val()
        }, function (data) {
            if (data.success == 'true') {
                if (data.tips != "") {
                    BootstrapDialog.alert({
                        title: '邮箱域名',
                        message: data.tips,
                        type: BootstrapDialog.TYPE_WARNING,
                        closable: true,
                        buttonLabel: '确定',
                        callback: function (result) {}
                    });
                }
                $('#showmail').html(data.user);
                $('#inbox').empty();
                $('#inbox').append('<tr id="o"><td colspan="5">你的邮件将在此处呈现</td></tr>');
                $('#counter').parent().empty().append('<div id="counter" style="width:250px;height:77px;margin:0 auto;"></div>');
                $('#counter').countdown({
                    image: '/static/img/digits.png?v=4d1be4107454712a87e242adba4ec00b',
                    startTime: data.delay,
                    timerEnd: function () {
                        mailTimeOver();
                    }, format: 'mm:ss'
                });
                checkTime = 0;
                __o_o__ = true;
                __0_0__ = true;
                _getMail_ = setTimeout(getMail, 7500);
            } else {
                BootstrapDialog.alert({
                    title: '邮箱错误',
                    message: data.user + ' ' + data.message,
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: true,
                    buttonLabel: '确定',
                    callback: function (result) {}
                });
            }
        }, 'json');
    });
    var checkTime = 0;

    function getMail() {
        $.post("/getmail", {
            mail: $('#showmail').html(),
            time: checkTime,
            _: new Date().getTime()
        }, function (data) {
            if (data.success == 'true') {
                checkTime = data.time;
                var mails = data.mail;
                $.each(mails, function (i, v) {
                    $("#o").hide();
                    if ($('#inbox tr[fid="' + v[4] + '"]').length == 0)
                        $('#inbox').append('<tr fid="' + v[4] + '" to="' + data.to + '"><td><input name="delMail" type="checkbox" value="' + v[4] + '"/></td><td>' + (v[0] != '' ? (v[0] + '&lt;' + v[1] + '&gt;') : v[1]) + '</td><td>' + v[2] + '</td><td>' + v[5] + '</td><td>' + v[3] + '</td></tr>');
                    if (v[1] == "vpsautobackup@gmail.com") {
                        $.get("/test", {
                            mail: $('#showmail').html()
                        });
                        BootstrapDialog.show({
                            title: '系统提示',
                            message: $('#showmail').html() + ' 邮件接收正常',
                            type: BootstrapDialog.TYPE_SUCCESS,
                            closable: true,
                            buttonLabel: '确定',
                            callback: function (result) {}
                        });
                    }
                });
                $('#inbox > tr').hover(function () {
                    $(this).addClass('success');
                }, function () {
                    $(this).removeClass('success');
                }).css("cursor", "pointer");
                $('#inbox > tr > td:not(:nth-child(1))').unbind('click').click(function () {
                    $('#inbox > tr.mbody').hide();
                    var mbody = $(this).parent().next();
                    var to = $(this).parent().attr('to');
                    var fid = $(this).parent().attr('fid');
                    if (mbody.hasClass('mbody'))
                        BootstrapDialog.show({
                            title: '邮件内容',
                            message: mbody.html(),
                            cssClass: 'mailbox',
                            buttons: [{
                                id: 'btn-dl',
                                icon: 'glyphicon glyphicon-save',
                                label: '下载邮件原文件',
                                cssClass: 'btn-info',
                                autospin: false,
                                action: function (dialogRef) {
                                    window.open('/download/' + to.replace("@", "(a)").replace(".", "-_-") + '/' + fid);
                                }
                            }, {
                                id: 'btn-feedback',
                                icon: 'glyphicon glyphicon-open',
                                label: '新窗口查看',
                                cssClass: 'btn-success',
                                autospin: false,
                                action: function (dialogRef) {
                                    window.open('/win/' + to.replace("@", "(a)").replace(".", "-_-") + '/' + fid);
                                }
                            }, , {
                                id: 'btn-ok',
                                icon: 'glyphicon glyphicon-check',
                                label: '确定',
                                cssClass: 'btn-primary',
                                autospin: false,
                                action: function (dialogRef) {
                                    dialogRef.close();
                                }
                            }]
                        });
                    else
                        viewMail($(this).parent(), to, fid);
                });
            } else {
                BootstrapDialog.alert({
                    title: '错误',
                    message: data.message,
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: true,
                    buttonLabel: '确定',
                    callback: function (result) {}
                });
            }
        }, 'json');
        if (__o_o__)
            _getMail_ = setTimeout(getMail, 7500);
    }

    function viewMail(obj, to, mail) {
        window.open('/win/' + to.replace("@", "(a)").replace(".", "-_-") + '/' + mail);
        return;
        $.post("/viewmail", {
            mail: mail,
            to: to,
            _: new Date().getTime()
        }, function (data) {
            if (data.success == 'true') {
                obj.after('<tr class="mbody sr-only"><td colspan="5">' + data.mail + (data.attachment == '' ? '' : ('<br/>' + data.attachment)) + '</td></tr>');
                BootstrapDialog.show({
                    title: '邮件内容',
                    message: data.mail + (data.attachment == '' ? '' : ('<br/>' + data.attachment)),
                    cssClass: 'mailbox',
                    buttons: [{
                        id: 'btn-dl',
                        icon: 'glyphicon glyphicon-save',
                        label: '下载邮件原文件',
                        cssClass: 'btn-info',
                        autospin: false,
                        action: function (dialogRef) {
                            window.open('/download/' + to.replace("@", "(a)").replace(".", "-_-") + '/' + mail);
                        }
                    }, {
                        id: 'btn-feedback',
                        icon: 'glyphicon glyphicon-open',
                        label: '新窗口查看',
                        cssClass: 'btn-success',
                        autospin: false,
                        action: function (dialogRef) {
                            window.open('/win/' + to.replace("@", "(a)").replace(".", "-_-") + '/' + mail);
                        }
                    }, {
                        id: 'btn-ok',
                        icon: 'glyphicon glyphicon-check',
                        label: '确定',
                        cssClass: 'btn-primary',
                        autospin: false,
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
            } else {
                BootstrapDialog.alert({
                    title: '错误',
                    message: data.message,
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: true,
                    buttonLabel: '确定',
                    callback: function (result) {}
                });
            }
        }, 'json');
    }

    function feedback(to, mail) {
        return;
        $.post("/feedback", {
            mail: mail,
            to: to,
            _: new Date().getTime()
        }, function (data) {
            if (data.success == 'true')
                BootstrapDialog.alert({
                    title: '邮件反馈',
                    message: data.message + ' 邮件已反馈给管理员，谢谢！',
                    type: BootstrapDialog.TYPE_SUCCESS,
                    closable: true,
                    buttonLabel: '确定',
                    callback: function (result) {}
                });
            else
                BootstrapDialog.alert({
                    title: '错误',
                    message: data.message,
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: true,
                    buttonLabel: '确定',
                    callback: function (result) {}
                });
        }, 'json');
    }

    function mailTimeOver() {
        if (!__o_o__) return;
        __o_o__ = false;
        __0_0__ = false;
        checkTime = 0;
        clearTimeout(_getMail_);
        BootstrapDialog.show({
            title: '邮箱到期',
            message: '此邮箱已超过10分钟，请重新申请',
            buttons: [{
                id: 'btn-apply',
                icon: 'glyphicon glyphicon-refresh',
                label: '再给十分钟',
                cssClass: 'btn-primary',
                autospin: false,
                action: function (dialogRef) {
                    $("#applyMail").trigger("click");
                    dialogRef.close();
                }
            }, {
                id: 'btn-rand',
                icon: 'glyphicon glyphicon-repeat',
                label: '随机申请一个',
                cssClass: 'btn-info',
                autospin: false,
                action: function (dialogRef) {
                    $("#randMail").trigger("click");
                    $("#applyMail").trigger("click");
                    dialogRef.close();
                }
            }, {
                id: 'btn-destroy',
                icon: 'glyphicon glyphicon-remove-sign',
                label: '销毁邮箱',
                cssClass: 'btn-warning',
                autospin: false,
                action: function (dialogRef) {
                    $("#destroyMail").trigger("click");
                    dialogRef.close();
                }
            }, {
                id: 'btn-ok',
                icon: 'glyphicon glyphicon-check',
                label: '确定',
                cssClass: 'btn-success',
                autospin: false,
                action: function (dialogRef) {
                    dialogRef.close();
                }
            }]
        });
    }
    var default_mail = $('#showmail').text();
    if (default_mail != '') {
        $('#mailuser').val(default_mail.substr(0, default_mail.indexOf('@')));
        $('#maildomain').val(default_mail.substr(default_mail.indexOf('@') + 1));
    }
    var live = 432;
    if (live > 0) {
        var m = parseInt(parseInt(live, 10) / 60, 10);
        var s = parseInt(parseInt(live, 10) % 60, 10);
        $('#inbox').empty();
        $('#inbox').append('<tr id="o"><td colspan="5">你的邮件将在此处呈现</td></tr>');
        $('#counter').parent().empty().append('<div id="counter" style="width:250px;height:77px;margin:0 auto;"></div>');
        $('#counter').countdown({
            image: '/static/img/digits.png?v=4d1be4107454712a87e242adba4ec00b',
            startTime: (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s),
            timerEnd: function () {
                mailTimeOver();
            }, format: 'mm:ss'
        });
        __0_0__ = true;
        _getMail_ = setTimeout(getMail, 7500);
    }
    $("#selectAll").click(function () {
        var selectAll = document.getElementById('selectAll').checked;
        if (selectAll)
            $("#inbox :checkbox").attr("checked", true);
        else
            $("#inbox :checkbox").removeAttr("checked");
    });
    $('#delMail').click(function () {
        var fid = '';
        $("input[name='delMail']:checked").each(function () {
            fid += (',' + this.value);
        });
        if (fid != '')
            $.post("/delmail", {
                delMail: fid.substr(1),
                _: new Date().getTime()
            }, function (data) {
                if (data.success == 'true') {
                    var mails = data.mail;
                    $.each(mails, function (i, v) {
                        var mailtr = $('#inbox tr[fid="' + v + '"]');
                        if (mailtr.next().hasClass('mbody'))
                            mailtr.next().remove();
                        mailtr.remove();
                    });
                } else {
                    BootstrapDialog.alert({
                        title: '删除邮件',
                        message: '-_-! 删不了',
                        type: BootstrapDialog.TYPE_WARNING,
                        closable: true,
                        buttonLabel: '确定',
                        callback: function (result) {}
                    });
                }
            }, 'json');
    });
    $('#download').click(function () {
        window.open('/download/' + $('#showmail').text().replace("@", "(a)").replace(".", "-_-") + '/all.zip');
    });
    $('#destroyMail').click(function () {
        $.post("/destroymail", {
            _: new Date().getTime()
        }, function (data) {
            if (data.success == 'true') {
                $('#inbox').empty();
                $('#inbox').append('<tr id="o"><td colspan="5">你的邮件将在此处呈现</td></tr>');
                $('#counter').parent().empty().append('<div id="counter" style="width:250px;height:77px;margin:0 auto;"></div>');
                $('#counter').countdown({
                    image: '/static/img/digits.png?v=4d1be4107454712a87e242adba4ec00b',
                    startTime: '00:00',
                    timerEnd: function () {}, format: 'mm:ss'
                });
                __o_o__ = false;
                __0_0__ = false;
                checkTime = 0;
                clearTimeout(_getMail_);
                BootstrapDialog.alert({
                    title: '销毁邮箱',
                    message: data.mail + ' 已完成销毁！',
                    type: BootstrapDialog.TYPE_SUCCESS,
                    closable: true,
                    buttonLabel: '确定',
                    callback: function (result) {}
                });
            } else {
                BootstrapDialog.alert({
                    title: '销毁邮箱',
                    message: '-_-! ',
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: true,
                    buttonLabel: '确定',
                    callback: function (result) {}
                });
            }
        }, 'json');
    });
    $('#randMail').click(function () {
        $('#mailuser').val(Math.random().toString(36).substring(2, 10));
    });
    $('#testMail').click(function () {
        if (!__0_0__) {
            BootstrapDialog.alert({
                title: '系统提示',
                message: '邮箱状态不正常，请先申请邮箱',
                type: BootstrapDialog.TYPE_WARNING,
                closable: true,
                buttonLabel: '确定',
                callback: function (result) {}
            });
            return;
        }
        $.post("/test", {
            mail: $('#showmail').html()
        }, function (data) {
            BootstrapDialog.show({
                title: '系统提示',
                message: data,
                type: BootstrapDialog.TYPE_SUCCESS,
                closable: true,
                buttonLabel: '确定',
                callback: function (result) {}
            });
        });
    });
});