define(["lib/app_controller"], function(AppController){
    var LoginController = function() {
        var self = this;

        App.route('/', function(){
            // init main viewports
            var app_viewport = new Ext.Viewport({
                layout: 'border',
                items: [
                    {
                        region: "center",
                        title: "CMMS",
                        titleAlign: 'center',
                        layout: 'fit',
                        html: "<div id='content-viewport'></div>",
                        autoScroll: true,
                        id: 'content-viewport-cmp'
                    }
                ]
            }).show();

            self.render('main/login'); 
        });
    }

    LoginController.prototype = new AppController();
    return new LoginController();
});
