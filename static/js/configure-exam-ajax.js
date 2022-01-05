$(document).ready((function(){
    console.log('configure-exam-ajax.js')
    $(document.getElementsByClassName('configure-exam-submit')).on('click',function(e){
        e.preventDefault();
        var examclassId=$(this).closest('.configureexamForm').find("select[name='examclassId']").val()
        var examName=$(this).closest('.configureexamForm').find("input[name='examName']").val()
        var examStart=$(this).closest('.configureexamForm').find("input[name='examStart']").val()
        var examEnd=$(this).closest('.configureexamForm').find("input[name='examEnd']").val()
        $.post({
            type:'post',
            url:'/home/teacher-dashboard/configure-exam/', 
            data:{
            examclassId:examclassId,
            examName:examName,
            examStart:examStart,
            examEnd:examEnd,
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
    