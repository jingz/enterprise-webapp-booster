define(["./login.ui"], function(LoginUI){
    var Login = Ext.extend(LoginUI,{
        initComponent: function(){
            Login.superclass.initComponent.call(this);
            var self = x = this;

            self._login.on({
                click: function(){
                    var d = self._frmLogin.serialize();
                    console.log(d)
                    $.ajax({
                        url: '/login',
                        type: 'POST',
                        data: JSON.stringify(d),
                        contentType: 'application/json',
                        dataType: 'JSON',
                        success: function(res) {
                            console.log(res);
                            if(res.success && res.url){
                                window.location.href = res.url;
                            } else if(!res.success && res.message) {
                                App.Notify.erro(res.message);
                            }
                        }
                    });
                }
            });
        }
    });

    return Login;
});
