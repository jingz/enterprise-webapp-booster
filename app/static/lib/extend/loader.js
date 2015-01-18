// widget loader helper
// @widgetName: widget folder name
// @cb : callback function where the widget has beed loaded
// 2012-03-09
var WidgetLoader = function (arrWidgetFolderNames, cb) {
    // varify argument
    if(typeof cb != "function") throw new Error("callback must be supplied.");
    if(!Ext.isArray(arrWidgetFolderNames)) throw new Error("first argument must be array.");

    var includeOrders = []
    Ext.each(arrWidgetFolderNames, function  (item, i, all) {
        var splitName = arrWidgetFolderNames[i].split("_"); 
        Ext.each(splitName, function(_name, j, _all) {
          splitName[j] = splitName[j].capitalize()   
        });
        var folderName = arrWidgetFolderNames[i] + '/';
        var jsMainFileName = splitName.join('');
        includeOrders.push( ABOSS_PATH.WIDGET + folderName + jsMainFileName + ".ui.js")
        includeOrders.push( ABOSS_PATH.WIDGET + folderName + jsMainFileName + ".js")
    })
    Ext.load(includeOrders, cb, window, true)
}

Ext.loadWidget = WidgetLoader;

// Store Loader Function
// use to load store script dynamically 
// 2012-02-21
var StoreLoader = function (scriptList, callback, scope, preserveOrder) {
    // prepend the store root path
    Ext.each(scriptList,function (script,i) {
        scriptList[i] = APP_PATH.STORE + script;
    });

    Ext.Loader.load.call(null, scriptList, callback, scope, preserveOrder)
}

// TODO load page ? by mapping folder and incljudeOrder

// load ENV for separate testing by pass login

var LoadEnvForTest =  function (afterLoad) {

    Ext.Loader.load([
        "/javascripts/extjs/adapter/jquery/jquery-1.7.1-min.js",
        "/javascripts/extjs-3.4/adapter/jquery/ext-jquery-adapter.js",
        "/javascripts/extjs-3.4/adapter/ext/ext-base.js",
        "/javascripts/extjs-3.4/ext-all-debug.js",
        "/aboss-ui/common/config.js",
        "/aboss-ui/common/loader.js",
        "/aboss-ui/common/custom.js",
        "/aboss-ui/common/Util.js",
        "/aboss-ui/common/form2js.js"
    ],afterLoad, window, true)
}
