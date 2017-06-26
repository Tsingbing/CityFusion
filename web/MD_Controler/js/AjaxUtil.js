AjaxUtil=function(url,data,succ,err,isSync){
	if(!isSync){
		isSync=false;
	}else{
		isSync=true;
	}
	$.ajax({
		url:url,
		dataType:"json",
		async:!isSync,
		data:data,
		success:function(data){
			if(succ){
				succ(data);
			}else{
//				console.log(data);
			}
		},
		error:function(msg){
			if(err){
				err(msg);
			}else{
//				alert(msg);
			}
		}
	});
};