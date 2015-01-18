Ext.override(Ext.form.FormPanel, {
    // config:
    // prefix_param or root_param: 
    // url: 
    // type: ajax verb usually put or post
    // success: callback
    // failure: callback
    // reset: reset after sending ajax success ?
    oldSubmit: Ext.form.FormPanel.prototype.submit,
        submit: function(config) {
        var self = this;
        var f = this.getForm();
        var serializeOption = Ext.apply({ onlyDirty: true, includeGrid: true }, config.serializeOption);
        // TODO option to inlcude grid records as params

        if(config.type && config.type === "put"){
            Ext.apply(serializeOption, { skipEmpty: false });
            var data = self.serialize(serializeOption); 
            if($.isEmptyObject(data)){
                App.Notify.warn("Nothing changed!");
                return false; 
            }
        } else{
            if(!config.serializeOption){
                Ext.apply(serializeOption, {onlyDirty: false} );
            }
            var data = self.serialize(serializeOption);
        }

        if(config.prefix_param || config.root_param){
            var o = {};
            o[config.prefix_param || config.root_param] = data;
            data = o;
        }

        // cache callback
        var suc = config.success;
        var fail = config.failure;
        var reset = config.reset;
        // function returned params
        var serialized = config.serialized;

        // serialized params
        // modify params before sending
        if(typeof serialized == "function"){
            data = serialized.apply(null, [data]); 
            // do nothing if the function return false
            if(data == false) return false;
        }

        var loadding; // notification element

        var defaults = {
            url: f.url,
            type: "post",
            reset: true, // reset form 
            contentType: "application/json",
            // clientValidation: true,
            dataType: "json",
            data: Ext.encode(data),
            // defer to use global setup
            // beforeSend: function() {
            //   loadding = Ext.Notify.msg({text:"Sending ...", type: "inform"});
            // },
            error: function() {
                // Ext.Notify.close(loadding)
                App.Notify.error("Ajax communication failed");
            },
            success: function (res){
                // return if not login
                if(res && res.response_code == "99"){
                    App.Notify.warn("Please Login");
                    return false;
                }

                if(res.success){
                    //Ext.Notify.msg({text: "Action Complete", type: "success"});
                    if(reset){
                        f.reset();
                        grds = self.query("editorgrid");
                        Ext.each(grds,function(g, index){
                            g.reset(); 
                        });
                    }

                    // success but have warning message
                    if(res.warning_message){
                        Ext.Notify.warning(res.warning_message);
                    }

                    // TODO do more stuff if config.sucess given
                    if(suc) suc(res); 
                } else{
                    var msg = [];
                    Ext.iterate(res.errors, function(k,v){
                        err = {};
                        err['error_field'] = k;
                        err['error_msg'] = v;
                        msg.push(err);
                    });

                    // var err_temp = new Ext.XTemplate(App.Template.form_error);
                    // var err_disp = err_temp.apply(msg);
                    // if(msg.length > 0)
                    //   var err_disp = "There are some invalid fields.<br/> Please see the highlights<hr/>"
                    // else
                    var err_disp = "";

                    self.markInvalids(res.errors);

                    if(err_disp != "")
                        App.Notify.erro(err_disp);
                    else
                        App.Notify.erro('There are some invalid fields \n Please see the highlights');

                    if(fail) fail(res);
                }
            }
        }

        if(config.success) delete config.success
            if(config.failure) delete config.failure

                config = Ext.applyIf(config, defaults);
        // TODO use Ext Ajax 
        $.ajax(config)
    },

    // mark invalid for fields in the form
    // errors format : { field: [ msg1, msg2 ] }
    markInvalids: function(errors) {
        var form = this;
        _.each(errors, function(messages, name) {
            var cmp = form.getFieldCompByName(name);
            cmp.markInvalid(messages.join('\n'));
        });
    },

    getFieldCompByName: function(name) {
        var el = this.query('[name=' + name + ']')[0];
        return !!el ? Ext.getCmp(el.id) : null;
    },

    isValid: function  () {
        if(this.getForm().isValid()){
            return true; 
        } else {
            Ext.Notify.error("The Form is invalid please see the hilights");
            return false;
        }
    },

    /*
     * !! deprecated see serialize
     * options
     * :onlyDirty 
     * :includeGrid
     */
    serializeObject: function(options){
        options = options || {};
        Ext.applyIf(options, { onlyDirty: true });
        var o = Util.form.serializeJson(this, options); 
        if(options.includeGrid){
            // find editorgrid 
            var editorgrids = this.query("editorgrid", true);
            var grids = this.query("grid", true);
            grids = grids.concat(editorgrids);
            Ext.each(grids, function(g, index) {
                // auto convert id to key
                var name = g.id.replace(/\-/g,"_");
                if(/^ext/i.test(name)) return false;
                var recs = g.serializeObject(options);
                if(recs.length > 0){
                    if(Ext.isArray(o[name]))
                o[name] = o[name].concat(recs);
                    else 
                o[name] = recs;
                }
            });
        }
        return o;
    },

    serializeNotBlank: function() {
        return this.serialize({ notBlank: true });
    },

    serializeDirty: function() {
        return this.serialize({ onlyDirty: true });
    },

    serialize: function(options) {
        options = options || {};
        Ext.applyIf(options, {
            onlyDirty: false,
            notBlank: false
        });

        var fields = options.onlyDirty ? this.getDirtyFields() : this.allFields();
        var o = {};

        _.each(fields, function(field) {
            var name = field.name;
            var arr_name = name.split('.');
            var tmp = ['o'];
            for (var i = 0; i < arr_name.length; i++) {
                var _name = arr_name[i];
                tmp.push(_name);
                var _o = tmp.join('.');
                // create object
                eval(_o + ' = ' + _o + ' || ' + ' {};');
            };
            eval(_o + ' = field.getValue();');
        });

        // filter fields that have blank value out
        if(options.notBlank){
          for(var k in o){
            if(o[k] == "" || o[k] == null) delete o[k]
          }
        }

        return o;
    },

    allFields: function  () {
        return this.query('.field');
    },

    // alias
    getAllFields: this.allFields,

    getDirtyFields: function  () {
        return _.filter(this.allFields(), function(f) {
            return f.isDirty();  
        });
    },

    fillData: function (data, options) {
        options = options || {};
        Ext.applyIf(options, {
            modify: false
        });

        Util.form.loadObject(this, data, options)

        // fill data in grid if has an id
        // collect grids in this form
        var gs = this.query("grid", true);
        var egs = this.query("editorgrid");
        var grids = gs.concat(egs);
        _.each(grids, function(g) {
            if(g.id){
                var attr = g.id.replace(/\-/ig, "_"); // association_attributes
                var prefix = attr.split("_")[0];      // association
                var d = data[attr] || data[prefix];
                if(d) g.addRecords(d, true);
            }
        });
        return this;
    },

    reset: function  () {
        this.getForm().reset(); 
    },

    readOnly: function  () {
        this._eachField(function  (el, i) {
            el.setReadOnly(true);
        }); 
        return this;
    },

    // disable all child elements
    disable: function  () {
        this._eachField(function  (el, i) {
            el.disable();
        }); 
        return this;
    },

    enable: function  () {
        this._eachField(function  (el, i) {
            el.setReadOnly(false);
            el.enable();
        }); 
        return this;
    },

    findField: function(id){
        this.getForm().findField(id); 
    },

    _eachField: function(fn) {
        _.each(this.getForm().items.items, fn);
    }
});

Ext.override(Ext.data.Store, {
    dup: function  () {
        // Wed113923
        var randId = Ext.util.Format.date(new Date(), "DHis");
        return new Ext.data.Store({ model: this.model, storeId: randId});
    }
});

Ext.override(Ext.grid.GridPanel, {
    _initComponent: Ext.grid.GridPanel.prototype.initComponent,
    // wrapper
    initComponent: function(){
       this._initComponent(); 
       this._setUpPaginator();
    },

    _setUpPaginator: function() {
        this.paginator = this.getPaginator();    
        // setup page size if given config
        if(this.store && this.paginator && this.paginator.pageSize){
          this.store.pageSize = this.paginator.pageSize;
          delete this.paginator.pageSize;
        }
    },

    changePage: function(page, isLoad){
      isLoad || (isLoad = false);
      if(this.paginator && this.paginator.getPageData().activePage != 1){
         this.store.currentPage = page;
      }

      if(isLoad) this.store.reload();

      return this;
    },

    // return HTML element
    getSelectedRow: function(){
        var sel =  this.getSelectionModel();
        var view = sel.views[0];

        return view.focusedRow;
    },

    // retrun record as JSON
    getSelectedRecord: function(){
        var sel = this.getSelectionModel();
        // TODO incase multi-selection
        return sel.selected.items[0];
    },

    doSimpleEffectOnSelectedRow: function(rowId) {
        var rowEl = this.getSelectedRow();   
        if(rowEl) {
            setTimeout(function(){
                $(rowEl).fadeOut().fadeIn();
            }, 200);
        }
    },

    updateSelectedRow: function(data) {
        var r = this.getSelectedRecord();
        Ext.apply(r.data, data);
        Ext.apply(r.json, data);
        // make a change
        this.doSimpleEffectOnSelectedRow();
        r.commit();
        // but still be modified record
        // this.addModifiedRecord(r);
        // TODO this.fireEvent("datachanged", r);
        return r;
    },

    getAllRecords: function() {
       return this.store.data.items;
    },

    getModifiedRecords: function(){
       return _.filter(this.getAllRecords(), function(rec){ return rec.dirty });
    },

    removeSelectedRecord: function() {
        var row = this.getSelectedRow();
        var rec = this.getSelectedRecord();
        if(row){
            $(row).fadeOut(function(){
                this.store.remove(rec);
            });
        }
    },

    updateRecord: function(id, data) {
        if(id) {
            var record = this.store.findRecord('id', id);
            if(record){
                Ext.extend(record.data, data);
                record.commit();
            } else {
                console.warn("Cannot find record with ID=" + id);
            }
        } else {
            console.error("updateRecord require id");
        }
    },

    addNewRecord: function(data, options){
        options = options || {};
        var st = this.store;
        if(options.append){
            var n = st.getRange().length;
            st.insert(n, data);
            this.getSelectionModel().select(n);
        } else {
            this.store.insert(0, data);
            this.getSelectionModel().select(0);
        }

        this.doSimpleEffectOnSelectedRow();
    },
    
    addRecords: function(data, thenCommit) {
      var thenCommit = thenCommit || false;
      var st = this.store;
      // recs = _.map(data, function(o) {
      //   return new st.recordType(o)
      // });
      st.add(data);
      if(thenCommit) this.getStore().commitChanges();

      // this.fireEvent("datachanged", recs);
      return this;
    },

    // simple remote grid filter
    fetch: function(filter, cb) {
      filter || ( filter = {} );
      // set stating params in order to be resued in pagination
      this.store.proxy.extraParams = {}; // reset cached params
      Ext.apply(this.store.proxy.extraParams, filter);
      this.changePage(1);
      if(typeof cb == 'function')
        this.store.load({ callback: cb }); // args:[ rs, opt, success ]
      else
        this.store.load();

      return this;
    },

    remotelyFilter: function(hash) {
        // clear the filter collection without updating the UI
        this.store.remoteFilter = true;
        this.store.clearFilter(true);
        for(var k in hash){
            this.store.filters.add(new Ext.util.Filter({ property: k, value: hash[k] }));
        }
        this.store.load();
    },

    locallyFilter: function(hash) {
        this.store.remoteFilter = false;  
        this.store.clearFilter(true);
        for(var k in hash){
            this.store.filters.add(new Ext.util.Filter({ property: k, value: hash[k] }));
        }
        this.store.load();
    },

    getPaginator: function() {
       // memo cached to private attributes
       this.paginator = (this.paginator || this.query('pagingtoolbar')[0] )
       return this.paginator;
    }
});

Ext.override(Ext.form.field.ComboBox, {
    setValueRemotely: function(key, v, cb, extraParams) {
        var self = this;
        extraParams = extraParams || {};

        if(!v){
            console.log("is blank ---------", v, this.getName());
            return false;
        }
        if(!key){
            key = this.queryParam;
        }
        if(this.queryMode == "remote" && !this.autoLoad){
            var s = this.getStore();
            // build params
            var params = {};
            params[key] = v;
            var val = v;
            s.load({
                params: Ext.apply(params, extraParams),
                beforeload: function(){
                    self.setRawValue("");
                },
                callback:function(rec) {
                    var rec = rec[0];
                    if(rec){
                        self.setValue(rec.data[self.valueField]);
                        cb && cb.apply(null, [rec]);
                    }
                }
            });
        }
    }
});
