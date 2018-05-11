function encrypt(src, mykey){
    var key = CryptoJS.enc.Utf8.parse(mykey);
    var srcs = CryptoJS.enc.Utf8.parse(src);
    var encrypted = CryptoJS.AES.encrypt(srcs, key, {mode:CryptoJS.mode.ECB,padding: CryptoJS.pad.Pkcs7});
    return encrypted.toString();
}

function decrypt(src, mykey){
    var key = CryptoJS.enc.Utf8.parse(mykey);
    var decrypt = CryptoJS.AES.decrypt(src, key, {mode:CryptoJS.mode.ECB,padding: CryptoJS.pad.Pkcs7});
    return CryptoJS.enc.Utf8.stringify(decrypt).toString();
}

function link(text){
	return '<a>' + text + '</a>';
}

function replace_spaces(text){
	return text.replace(/  /g,' ').replace('  ',' ');
}

crypt_data = "ir5K4icvTYB59rz57VFFXQ==";
structs = [];
macros = [
	'#define IN ',
	'#define _In_ ',
	'#define OUT ',
	'#define _Out_ ',
]

$(document).ready(function(){
	//var mykey = prompt("mykey", "");
	//$('#content').html(decrypt(crypt_data,mykey));
	
	//add struct to structs array
	$('#STRUCTS tr td:first-child').each(function(index, ele){
		var text = $(ele).text();
		if( structs.indexOf(text) < 0)
			structs.push(text);	
	})
	
	var macro_keys = [];
	//parse define NAME to macro_keys
	macros.forEach(function(elementValue, index, arr){
		var text = replace_spaces(elementValue);
		var name = text.split(' ')[1];
		macro_keys.push(name);
	})	
	
	console.log('structs', structs);
	console.log('macro_keys', macro_keys);
	
	//mark keywords
	$('#CALLS li').each(function(index, ele){
		var text = $(ele).text();
		var words = replace_spaces(text).split(' ');
		var html = '';
		
		words.forEach(function(elementValue, index, arr){
			var count = words.length;
			var find = -1;
			var isMacro = false;

			if( index < count - 2 ){
				console.log('macro', elementValue);
				
				isMacro = true;
				find = macro_keys.indexOf(elementValue);
				if( elementValue[0] == 'P')
					find = macro_keys.indexOf(elementValue.substr(1,elementValue.length-1));
			} else if (index != count-1) {
				console.log('type', elementValue);
				
				find = structs.indexOf(elementValue);
				if( elementValue[0] == 'P')
					find = structs.indexOf(elementValue.substr(1,elementValue.length-1));
			}
			if( find != -1 ){
				var newEle = $( link(elementValue) ).attr('index',find);
				if( isMacro )
					newEle.addClass('macro');
				else
					newEle.addClass('struct');
				
				html += newEle[0].outerHTML + ' ';
			}else
				html += elementValue + ' ';
		});
		$(ele).html(html);
	});
	
	$('.macro').mouseover(function(){
		console.log( macros[$(this).attr('index')] );
	});
	$('.struct').mouseover(function(){
		console.log( macros[$(this).attr('index')] );
	});	
	console.log('MACRO', $('.macro'));
	console.log('STRUCT', $('.struct'));
});