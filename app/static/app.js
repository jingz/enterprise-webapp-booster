// Setup Application Environment
define(["lib/router"], function(Router){
    var $ = window.$;
    // config
    window.$.ajaxSetup({
        dataType: 'json',
        contentType: 'application/json'
    });
    
    // Setup Global App Namespace
    window.App = {};
    
    // init router
    App.router = new Router();
    if(window.APP_ALLOW_ROUTES) 
        App.router.allow_hash = APP_ALLOW_ROUTES;

    App.router.hash_not_allow = function(hash) {
        App.Notify.warn('Page Not Found! ' + hash);
    }
    // for init application routes
    App.route = App.router.route;

    App.redirect = function(url, data) {
        if(App.router) App.router.navigate(url, data);
        else throw new Error('App Router must be inited.');
        return false;
    }

    // open view in dialog
    App.openWindow = function(url, data) {
        data || (data = {});
        url = url || '#/';
        url += (/\?/.test(url)) ? '&_renderMethod=dialog' :
                                  '?_renderMethod=dialog' ;

        App.router.navigate(url, data);
    }

    App.closeWindow = function(scope) {
        Ext.WindowMgr.front.close();
    }

    App.confirm = function (msg, yesDo, noDo) {
        Ext.Msg.confirm("Please Confirm", msg, function (ans) {
            if(ans == "yes"){
                if(typeof yesDo == "function") {
                    yesDo();
                } else throw new Error("need to supply callback function");
            } else if(typeof noDo == "function"){
                    noDo();
            } 
        });
    }

    App.getRouterParams = function() {
        return App.router.getParams(); 
    }

    // build mutiline string from comment of function
    App.buildString = function(fn){
        var reg = /\/\*([\s\S]*)\*\//im;
        if(typeof fn == 'function'){
            return reg.exec(fn.toString())[1];
        }
        return false;
    }

    App.is_route_allowed = function(route) {
        // using const APP_ALLOW_ROUTES
        var reg_route = new RegExp(route, 'i');
        return _.any(APP_ALLOW_ROUTES, function(allow_uri) {
            return reg_route.test(allow_uri);
        });
    }

    // Global Notification Config
    App.Notify = {
        default_config: { globalPosition: 'top center' },

        // options
        /*
        {
          // whether to hide the notification on click
          clickToHide: true,
          // whether to auto-hide the notification
          autoHide: true,
          // if autoHide, hide after milliseconds
          autoHideDelay: 5000,
          // show the arrow pointing at the element
          arrowShow: true,
          // arrow size in pixels
          arrowSize: 5,
          // default positions
          elementPosition: 'bottom left',
          globalPosition: 'top right',
          // default style
          style: 'bootstrap',
          // default class (string or [string])
          className: 'error',
          // show animation
          showAnimation: 'slideDown',
          // show animation duration
          showDuration: 400,
          // hide animation
          hideAnimation: 'slideUp',
          // hide animation duration
          hideDuration: 200,
          // padding between element and notification
          gap: 2
        }
        */

        warn: function  (msg, options) {
            var config = this.default_config;
            config.className = 'warn';
            options = options || {};
            $.extend(config, options);
            $.notify(msg, config);
        },
        succ: function  (msg, options) {
            var config = this.default_config;
            config.className = 'success';
            options = options || {};
            $.extend(config, options);
            $.notify(msg, config);
        },
        erro: function  (msg, options) {
            var config = this.default_config;
            config.className = 'error';
            options = options || {};
            $.extend(config, options);
            $.notify(msg, config);
        },
        info: function  (msg, options) {
            var config = this.default_config;
            config.className = 'info';
            options = options || {};
            $.extend(config, options);
            $.notify(msg, config);
        }
    }

    App.BASE_CONTROLLER_DIR = 'controller';
    App.BASE_TEMPLATE_DIR = 'components';
    App.DEFAULT_MAIN_VIEWPORT_COMPONENT_ID = 'content-viewport-cmp';
    App.DEFAULT_RENDER_METHOD = 'replace';

    Object.freeze(App);
    Object.freeze(App.router);
    return App;
});
