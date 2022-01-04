$(document).ready((function(){
    console.log('build-class-ajax')
    function validPassword(password){
        if(password.includes(" ") || password.length==0){
            return false
        }
        return true
    }
    function validClassName(className){
        if (className.includes(" ") || className.length==0){
            return false
        }
        return true
    }
    function validClassKey(classKey){
        if (classKey.includes(" ") || classKey.length==0){
            return false
        }
        return true
    }
    
    $(document.getElementById('build-class-subimt')).on('click',function(e){
        e.preventDefault();
        var className=$(this).closest('#build-class-form').find("input[name='className']").val()
        var classKey=$(this).closest('#build-class-form').find("input[name='classKey']").val()
        var classPassword=$(this).closest('#build-class-form').find("input[name='classPassword']").val()
        var teacherid=$(this).closest('#build-class-form').find("input[name='teacherid']").val()
        if (validPassword(classPassword) && validClassName(className) && validClassKey(classKey)){
            $.post({
                type:'post',
                url:'/home/teacher-dashboard/build-class/', 
                data:{
                className:className,
                classKey:classKey,
                classPassword:classPassword,
                teacherid:teacherid,
                crossDomain: true,
                },
                success:function(response)
                {
                    alert(response.message)
                    location.reload()
                
                },
                error:function(error){
                    console.log('message Error' + JSON.stringify(error));
                }  
            })
            }
        else{
            alert("password or class name or class key is not valid.please dont use any space like 'M 3' or 'Ehsan 12'.the valid shape is 'M3' or 'Ehsan12'")
        }
        });

    ///////////////////////////Config CSRF
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
    })
    //////////////////////////End
}) )
    