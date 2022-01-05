$(document).ready((function(){
    console.log('delete-exam-ajax.js')
    $(document.getElementsByClassName('delete-exam-submit')).on('click',function(e){
        e.preventDefault();
        var examid=$(this).closest('.deleteexamForm').find("select[name='examid']").val()
        $.post({
            type:'post',
            url:'/home/teacher-dashboard/delete-exam/', 
            data:{
            examid:examid,
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
    