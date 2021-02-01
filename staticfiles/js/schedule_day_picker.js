$(function(){
    var employee_tr = $('.employee-schedule-table tbody tr')
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    if(employee_tr){
        for(var i = 0; i < employee_tr.length;i++){
            var employee_id = $(employee_tr[i]).attr('id')
            $.ajax({
                method: "GET",
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                async: false,
                url: GET_STAMPS.replace("0", employee_id),
                success: function (data) {
               
                    if(data['stamps'].length > 0){
                        var stamp_arr = data['stamps']  
                        if(stamp_arr[0]['activity_type'] == 1){
                            var clock_in = stamp_arr[0]['timestamp']
                            $('#'+employee_id+' td.clocked-in').html(clock_in.slice(0,5))
                            $('#'+employee_id+' td.clocked-out').html("Clocked In")                            
                        }
                        else{
                            var clock_in  = stamp_arr[1]['timestamp']
                            var clock_out = stamp_arr[0]['timestamp']
                            $('#'+employee_id+' td.clocked-in').html(clock_in.slice(0,5))
                            $('#'+employee_id+' td.clocked-out').html(clock_out.slice(0,5))
                        }
                    }
                    else{
                        $('#'+employee_id+' td.clocked-in').html("Not Clocked In")
                        $('#'+employee_id+' td.clocked-out').html("Not Clocked Out")   
                    }
                }
            })
        }
    }
})


