define(["lib/app_controller"], function(AppController){
    var MainController = function() {
        var self = this;

        var treeMenuStore = Ext.create('Ext.data.TreeStore', {
            root: { expanded: true, children: APP_MENU_TREE.children }
        });

        var menuTree = Ext.create('Ext.tree.Panel', {
            title: '', store: treeMenuStore, rootVisible: false
        });

        menuTree.on({
            itemclick: function(t, r){
                console.log(arguments); 
                var text = r.data.text;
                var link = r.data.href;
                Ext.getCmp('content-viewport-cmp').setTitle(text);
                App.redirect(link);
            }
        });

        App.route('/', function(){
            // init main viewports
            var app_viewport = new Ext.Viewport({
                layout: 'border',
                items: [
                    {
                        region: "west",
                        title: 'Menu',
                        // html: "<div id='menu-viewport'>" + menuList + "</div>",
                        layout: 'fit',
                        items: [menuTree],
                        width: "40%",
                        split: true,
                        collapsible: true,
                        collapsed: true,
                        hidden: false,
                        id: 'menu-viewport-cmp'
                    },
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

        });

        App.route('/main/test', function(id) {
            self.render('main/test');
        });

        App.route('/main/client', function  () {
            self.render('main/client');
        });

        App.route('/main/ord_deal', function  () {
            self.render('main/test_inq');
        });

        App.route('/feed/manage', function() {
            console.log('in test inq', arguments)
            self.render('main/feed_list');
        });

        App.route("/feed_entries/manage", function(){
            self.render('main/feed_entries'); 
        });

    }

    MainController.prototype = new AppController();
    return new MainController();
});
