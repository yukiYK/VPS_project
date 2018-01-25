
$(document).ready(function(){
	$.validator.addMethod("username", function(value, element, param){
	    return new RegExp(/^[a-zA-Z0-9]+$/).test(value);
	}, "只能输入字母和数字！");
	$.validator.addMethod("emailCode", function(value, element, param){//邮箱验证码验证规则
	    return new RegExp(/^\d{6}$/).test(value);
	}, "请输入正确的邮箱验证码！");
	$.validator.addMethod("password", function(value, element, param){//密码验证规则
	    return new RegExp(/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$/).test(value);
	}, "请输入6-20位数字与字母的组合！");
	// $.validator.addMethod("isAgree", function(value, element, param){//复选框验证规则
	//     return this.optional(element) || $(this).attr('checked');
	// }, "请同意UTXO用户服务协议！");
	$.validator.setDefaults({
		onkeyup: null,
		success: function(label){
			label.text('').addClass('valid');
		}
	})
})