$(document).ready((function(){
    console.log('delete-class-ajax.js')
    $(document.getElementsByClassName('delete-class-submit')).on('click',function(e){
        e.preventDefault();
        var classid=$(this).closest('.deleteclassForm').find("select[name='classid']").val()
        $.post({
            type:'post',
            url:'/home/teacher-dashboard/delete-class/', 
            data:{
            classid:classid,
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
    