# -*- coding: utf-8 -*-

import sys
import frida


# app_package_name = "com.wudaokou.hippo"
app_package_name = "盒马"


jscode = """
setImmediate(function() {
    console.log('start hook ......');
    Java.perform(function () {
        var Response = Java.use('mtopsdk.network.domain.Response');
        Response.$init.overload('mtopsdk.network.domain.Response$Builder').implementation = function() {
            var ret = this.$init.apply(this, arguments);
            console.log("Response: "+this.toString());
            this.toString().match(/ url=([^,]+),/gm).forEach((m) => {
                console.log(m.replace(' url=', '').replace(',', ''));
            });
            this.toString().match(/ headers=\{(.+)\}, body/gm).forEach((m) => {
                console.log(m.replace(' headers=\{', '').replace('\}, body', ''));
            })
            return ret
        };
        var cls = Java.use('mtopsdk.security.InnerSignImpl');
        cls.getUnifiedSign.implementation = function(a, b, c, d, e, f) {
            console.log(a, b, c, d, e, f);
            // console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
            var result = this.getUnifiedSign(a, b, c, d, e, f);
            return result
        };
    });
});
"""


def on_message(message, data):
    print(message)

def get_rpc(jscode, app_package_name):
    device = frida.get_usb_device()
    try:
        process = device.attach(app_package_name)
    except frida.ProcessNotFoundError:
        print('app未启动，开始启动app...')
        pid = device.spawn([app_package_name])
        device.resume(pid)
        time.sleep(10)
        process = frida.get_usb_device().attach(app_package_name)
    script = process.create_script(jscode)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()

if __name__ == "__main__":
    get_rpc(jscode, app_package_name)
