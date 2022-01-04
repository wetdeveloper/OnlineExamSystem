$(document).ready((function(){
    console.log('send-exam-answer-student-ajax.js')
    $(document.getElementsByClassName('answer-send-submit')).on('click',function(e){
        e.preventDefault();
        var classid=$(this).closest('.answerform').find("input[name='classid']").val()
        var questionid=$(this).closest('.answerform').find("input[name='questionid']").val()
        var answer_order=$(this).closest('.answerform').find("input[name='answer_order']:checked").val()
        $.post({
            type:'post',
            url:'/home/student-dashboard/load-exam/send-answer/', 
            data:{
            classid:classid,
            questionid:questionid,
            answer_order:answer_order,
            crossDomain: true,
            },
            success:function(response)
            {
                alert(response.message)
                
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
    