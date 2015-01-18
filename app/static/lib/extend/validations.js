Ext.apply(Ext.form.VTypes, {
    // xxxMask: "",
    // xxxVal: "",
    // xxxText: "",
    ">": function(v, el, param){
   		v = v || 0;
   		param = param || 0; 
   		if(v <= param){
   			Ext.form.VTypes[">Text"] = String.format("Should more than {0}", param);
   			return false;	
   		}
   		return true;	
    },

    "==": function(v, el, param) {
   		v = v || 0;
   		param = param || 0; 
   		if(v != param){
   			Ext.form.VTypes["==Text"] = String.format("Should be equal to {0}", param);
   			return false;	
   		}
   		return true;	
    },

    ">=": function  (v, el, param) {
   		v = v || 0;
   		param = param || 0; 
   		if(v < param){
   			Ext.form.VTypes[">=Text"] = String.format("Should more than or equal to {0}", param);
   			return false;	
   		}
   		return true;	
    },

    "<": function  (v, el, param) {
   		v = v || 0;
   		param = param || 0; 
   		if(v >= param){
   			Ext.form.VTypes["<Text"] = String.format("Should less than {0}", param);
   			return false;	
   		}
   		return true;	
    },

    "<=": function  (v, el, param) {
   		v = v || 0;
   		param = param || 0; 
   		if(v > param){
   			Ext.form.VTypes["<=Text"] = String.format("Should less than or equal to {0}", param);
   			return false;	
   		}
   		return true;	
    },

    len: function  (v, el, param) {
      var t = v + '';
      if(t.length != (+param)){
        Ext.form.VTypes["lenText"] = String.format("Should have length equal to {0}", param);
        return false;
      }
      return true;
    },

    presence: function  (v, el) {
    	if( ((typeof v == "string") && v == "") || 
          ((typeof v == "number") && isNaN(v)) ){
    		Ext.form.VTypes["presenceText"] = String.format("Should not be blank");
    		return false;
    	}
    	return true;
    }

});
