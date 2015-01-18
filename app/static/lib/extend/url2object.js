/**
 * @author Jing
 * Date: 11.04.14
 * Time: 16:00
 */

var url2object = function(url){
    'use strict';

    var arr = url.split("&");
    var param = [];
    var o = {};
    var k, v, matches;
    for(var i = 0; i < arr.length; i++){
        param = arr[i].split('=');
        k = param[0]; v = param[1];
        // case key is array
        if(/\[(\w+)\]/.test(k)){ // nested keys
            // x = "key[nest]"
            // ["key", "nest"]
            matches = k.match(/([^\[\]]+)/g);
            var tmp_keys = ["o"];
            for (var j = 0; j < matches.length; j++) {
                var _k = matches[j];
                tmp_keys = tmp_keys.concat(_k);
                var nested_key = tmp_keys.join(".");
                // case "key[nest][]"
                (/\[\]$/.test(k) && j == matches.length - 1) ?
                    eval(nested_key + " = " + nested_key + " || [];") :
                    eval(nested_key + " = " + nested_key + " || {};");
            };

            // case "key[nest][]"
            (/\[\]$/.test(k)) ?
                eval(nested_key + ".push('" + v + "')") :
                eval(nested_key + " = '" + v + "'");

        } else if(/\[\]$/.test(k)){
            // remove blacket
            k = k.substring(0, k.length - 2);
            o[k] = o[k] || [];
            o[k] = o[k].concat(v);
        } else {
            o[k] = v;
        }
    }
    return o;
}
