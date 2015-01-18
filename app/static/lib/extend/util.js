(function(win){

    Util = {};

    Util.form = {};

    Util.form.loadObject = function(f, obj, options) {
        options = options || {};
        Ext.applyIf(options, {
            modify: false
        });

        if(typeof f == "string"){
            var rootNode = document.getElementById(f);
        }
        else{
            // f = f.getForm && f.getForm();
            var rootNode = document.getElementById(f.id);
        } 

        // js2form
        if(!js2form){ throw new Error("must include js2form lib") }

        js2form(rootNode, obj, ".", function(name, value) {
            if(f.getFieldCompByName){
                var field = f.getFieldCompByName(name);
            } else {
                // incase from is stirng
                var qry = "*[name='"+name+"']";
                var el = Ext.query(qry, rootNode)[0];
                // not work in case custom field like
                // currency and numeric field
                if(!!el) var field = Ext.getCmp(el.id);
            } 

            if(field) {
                if(field.getXType() === "datefield" && !Ext.isEmpty(value)){
                    // got 1970-01-01
                    // incase from array store
                    var v = _.isDate(value) ? value : new Date(value);
                    field.setValue(v);
                    if(!options.modify) field.originalValue = field.getValue();
                } else {
                    // fill data to remote combo
                    if(field.getXType() == "combobox" && field.queryMode == "remote"){
                        if(field.store){
                            if(value) field.setValueRemotely(field.queryParam || field.valueField, value, function() {
                                if(!options.modify) field.originalValue = field.getValue();
                            });
                        }
                    } else {
                        field.setValue(value);
                        if(!options.modify) field.originalValue = field.getValue();
                    }
                    // field.setValue(value);
                    // if(!options.modify) field.originalValue = field.getValue();
                }
            } else {
                console.log("field not found");
            }
        });

        // fix radio filler
        // var rads = $.unique($('#'+f.id+' input[type=radio]').map(function(i, o){ return o.name; }));
        // $.each(rads, function(i, name){
        //     $.grep(
        //         $('#'+f.id+' input[name='+name+']'),
        //         function(o){ return o.value == obj[name]; }
        //     )[0].checked = true;
        // });
    }


    Util.form.serializeJson = function (form, options) {
        options = options || {};
        Ext.applyIf(options, { skipEmpty: true });
        var isAnythingUpdate = false;
        if(form2js){
            // form can be id string
            if(typeof form == "string"){
                var f = Ext.getCmp(form);
                var nodeId = form;
            } else{
                var f = form;
                var nodeId = form.id;
            }

            console.log(f)

                console.log("%c start serialize", "color: cyan;");
            // form2js(rootNode, delimiter, skipEmpty, nodeCallback, useIdIfEmptyName)
            var params = form2js(nodeId, '.', options.skipEmpty, function (node) {
                if(node.getAttribute && node.name && !(/(^ext)|\-/.test(node.name))){
                    console.log(f, node.name);
                    if(f && f.query){
                        var field = f.query(".field[name="+node.name+"]")[0];
                        // var field = f.findField(node.id);
                    } else {
                        // incase from is stirng
                        var qry = "[name="+node.name+"]";
                        var field = form.query(qry)[0];
                    }

                    // check dirty if setting
                    if(options.onlyDirty){
                        //var field = Ext.getCmp(node.id);
                        if(field){
                            var o = field.originalValue;
                            var n = field.getValue();
                            //if(!field.isDirty()){
                            // not use isDirty() method for sure in radio
                            var notDirty = (o == n);
                            if(Ext.isDate(o) && Ext.isDate(n)){ notDirty = notDirty | (o.toDateString() == n.toDateString())}
                            if(notDirty){
                                // set value to null to skip
                                // TODO except id # hidden inputs that store record key 
                                if(/id$/i.test(node.name) && node.type == "hidden"){
                                    return { name: node.name, value: parseInt(node.value) || null }
                                }

                                return { name: node.name, value: null };
                            } else {
                                isAnythingUpdate = true;
                            }
                        } else {
                            // in case not found component of this input
                            // ex the field that use plugins that 
                            // store value in the hidden field instead

                            return { name: node.name, value: null};
                        }
                        }

                        if(field){
                            if(node.className.indexOf('combo') != -1 ){
                                return {name: node.name, value: field.getValue()}
                            }
                            if(node.className.indexOf('time') != -1 ){
                                return {name: node.name, value: field.getValue()}
                            }
                            if(node.className.indexOf('checkbox') != -1 ){
                                return {name: node.name, value: field.getValue()}
                            }
                            if(field.getXType() == "hidden"){
                                return { name: node.name, value: field.getValue()}
                            }
                        }

                        // convert to integer if has class name number in the field
                        if(node.className.indexOf('number') != -1 ){
                            var v = parseFloat(node.value);
                            if(Ext.isNumber(v)){
                                return {name: node.name, value: v}
                            }
                        }

                        // date convert to y m d ( ruby like )
                        if(node.className.indexOf('date') != -1 ){
                            var v = node.value; 
                            if(v){
                                var dmY = v.split('/');
                                var d = dmY[2] + '-' + dmY[1] + '-' + dmY[0];
                                return {name: node.name, value: d}
                            }
                        }

                        // TODO checkbox in legend
                        // act as HTML
                        // radio
                    }

                    return false;
                }, false);

                if(options.onlyDirty && !isAnythingUpdate) return {};
                if(!options.skipEmpty){
                    // filter null out of params
                    var tmp = {};
                    Ext.apply(tmp, params);
                    for(var k in tmp){
                        if(!tmp[k] && tmp[k] == null){
                            delete params[k];
                        }
                        // nested field support just 2 recursive
                        if(tmp[k] instanceof Object){
                            for(var j in tmp[k]){
                                if(!tmp[k][j] && tmp[k][j] == null){
                                    delete params[k][j];
                                }
                            }
                        }
                    }
                }

                // remove ext name
                var tmp = {};
                Ext.apply(tmp, params);
                for(var name in tmp){
                    // ext component
                    if(/^ext/i.test(name)){
                        delete params[name];
                    }
                }

                return params || {};
            }

            throw new Error("must include form2js lib");
        }

})(window);
