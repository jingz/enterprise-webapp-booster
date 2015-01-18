// Jing 2012-09-24
// --------------------------------------------------------
// Multiple Validation plugins
// What :
//   allow every field component apply more than one validation
//   rule 
// How :
//   this plugins will override getErrors method of instance
// Why :
//   The built-in validation configuration does not allow
//   multiple-validation rule 
// Usage:
//   field.vtypes[<rule>] = param
Ext.ux.MultipleValidations = Ext.extend(Ext.util.Observable, {

  constructor: function(config){
    config = config || {}
    Ext.apply(this, config);
    Ext.ux.MultipleValidations.superclass.constructor.call(this);

    // this.addEvents({
    //     addnewrecord: true,
    //     editselectedrecord: true,
    //     deleteselectedrecord: true
    // });
  },

  init: function(field){
      // work only field instance 
      if(field instanceof Ext.form.Field){
        // window.x = field;
        field._getErrors = field.getErrors;
        field.getErrors = this.getErrors(field);
        field.setVtypes = function  (opt) {
          opt = opt || {};
          this.vtypes = this.vtypes || {};
          Ext.apply(this.vtypes, opt)
          this.clearInvalid();
          this.isValid();
        }
      }
  },

  getErrors:function(field) {
    var self = this;
    return function(value) {
      // get errors array
      var errors = field._getErrors(value); 
      var vtypes = field.vtypes || {};
      for(var t in vtypes){
        if(t){
            var params = vtypes[t];
            var vt = Ext.form.VTypes;
            value = field.getValue();
            if(!vt[t](value, field, params)){
                errors.push(vt[t +'Text']);
            }
        }
      }
      return errors;
    }
  }

});

Ext.preg("multiple_validations", Ext.ux.MultipleValidations);
