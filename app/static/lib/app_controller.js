define(["app"], function(App){

    var AppController = function(options){
        var self = this;

        options || (options = {});

        this.is_rendered = false; 

        /*
         * ExtJS Render Template Helper
         * template : client/client_info_view
         * reserve options : { _renderTo: 'extjs-component-id', _renderMethod: 'replace' }
         */
        this.render = function(template, options) {
            var self = this;
            options || (options = {})
            self.params = App.getRouterParams(); // depend parameter from router via App object

            // cmp_id must be ExtJS component
            // modes : replace / append / prepend / dialog(window) / specific container(renderTo)
            var default_options = {
                cmp_id: options._renderTo || self.params._renderTo || App.DEFAULT_MAIN_VIEWPORT_COMPONENT_ID,
                method: options._renderMethod || self.params._renderMethod || App.DEFAULT_RENDER_METHOD,
                data: {}
            };

            options = _.extend(default_options, options);
            
            // making script path
            var script_path = App.BASE_TEMPLATE_DIR + "/" + template;

            // Load Ext Component
            requirejs([script_path], function(View) {
                switch(options.method){
                    case 'replace':
                        var view = new View(options.data);
                        // determine whether Element of Component for
                        // access different API !!
                        if(options.cmp_id instanceof Ext.Element){
                            container = options.cmp_id;
                            container.update('');
                            window.v = view;
                            view.render(container);
                        } else {
                            var container = Ext.getCmp(options.cmp_id)
                            container.removeAll();
                            container.add(view);
                        }
                        break;
                    case 'append':
                        var container = Ext.getCmp(options.cmp_id)
                        var view = new View(options.data);
                        container.add(view);
                        break;
                    case 'dialog':
                        var win = new Ext.Window({ title: "Window", layout: 'fit', modal: true });
                        var view = new View(options.data);
                        win.add(view);
                        win.show();
                        break;
                    case 'prepend':
                        // TODO
                        break;
                    default:
                        break;
                }
            });
        }
    };

    return AppController;
});
