/* 
 * A Simple Router - Borrow from Backbone.Router
 *
 * var r = new Router();
 * r.route('/home/:id', function(id, params){
 *      // do something
 * })
 *
 */
define(function(){

    var Router = function(rules){ 
        var self = this;

        // public
        self.oldurl = "";
        self.newurl = "";
        self.dataState = {}; // hold state's data

        var optionalParam = /\((.*?)\)/g;
        var namedParam    = /(\(\?)?:\w+/g;
        var splatParam    = /\*\w+/g;
        var escapeRegExp  = /[\-{}\[\]+?.,\\\^$|#\s]/g;

        self._routeToRegExp = function(route) {
          route = route.replace(escapeRegExp, '\\$&')
                       .replace(optionalParam, '(?:$1)?')
                       .replace(namedParam, function(match, optional) {
                         return optional ? match : '([^/?]+)';
                       })
                       .replace(splatParam, '([^?]*?)');
          return new RegExp('^' + route + '(?:\\?([\\s\\S]*))?$');
        }

        // keep route rules and handlers
        var handlers = [];

        self.route = function(route, fn){
            var regexpRoute = self._routeToRegExp(route);
            handlers.unshift({ route: regexpRoute, callback: fn });
        }

        // redirect
        self.navigate = function(url, dataState){
            dataState || (dataState = {});
            url || (url = '/');
            
            if(url.substr(0, 1) != '#') url = '#' + url;
            
            window.history.pushState(dataState, document.title, url);
            self.dataState = dataState;
            console.log('navigate pushState', url);
            load();
        }

        // private
        var params = {};
        self.resetParams = function  () {
            params = {};
        }

        self.getParams = function  () {
            return params;
        }

        self.setParams = function(o) {
            params = o; 
        }

        self.allow_hash = '*';
        self.is_hash_allowed = function(hash) {
            if(self.allow_hash == '*') return true;
            var reg_route = new RegExp(hash, 'i');
            return _.any(self.allow_hash, function(allow_uri) {
                return reg_route.test(allow_uri);
            });
        }

        self.hash_not_allow = function(hash) {
            // need to implement
        }

        // private load full url
        function load(){
            var hash = window.location.href.match(/#(.*)$/);
            hash = hash ? hash[1] : '';
            if(!self.is_hash_allowed(hash)){
                return self.hash_not_allow(hash);
            }
            // reset params
            self.resetParams();

            return _.any(handlers, function(h){
                // match the route
                if(h.route.test(hash)){
                    var args = h.route.exec(hash);
                    // convert object the last params
                    if(args.length > 0){
                        var lastMatch = args[args.length - 1];
                        if(/=/.test(lastMatch)){
                            var o = url2object(lastMatch);
                            args[args.length-1] = o;
                            self.setParams(o);
                        }
                    }
                    // TODO passing necessary information to controller via self
                    h.callback.apply(self, args.slice(1));
                }
            });
        }

        // handle back event
        $(window).on('popstate', function(){ 
            self.dataState = window.history.state;
            console.log('load popstate')
            load(); 
        });

        // window.onhashchange = function(changed){
        //     self.hashChangedObj = changed;
        //     self.oldUrl = changed.oldURL;
        //     self.newUrl = changed.newURL;
        //     console.log('load hashchange')
        //     load();
        // }
    }

    return Router;
});
