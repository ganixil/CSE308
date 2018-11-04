var table = $('#user-table').DataTable();
$(document).ready(function(){    // Instantiate UI tabs vertical
     $( "#tabs-collapsible" ).tabs({
            collapsible: true
        });

     $("#home").click(function(){
        $("#tabs-v-1").show();
        $("#edit").hide(); 
     });

    $("#users").click(function(){
        $("#tabs-v-2").show();
        $("#edit").hide(); 
     });

    $("#edit").click(function(){
        $("#tabs-v-3").show();
        $("#password").prop("type", "password");
        if ($("#toggle-password").hasClass('fa-eye')){
                $("#toggle-password").removeClass("fa-eye");
                $("#toggle-password").addClass("fa-eye-slash");
        }
      $("#confirm-password").prop("type", "password");
        if ($("#toggle-confirm-password").hasClass('fa-eye')){
         $("#toggle-confirm-password").removeClass("fa-eye");
         $("#toggle-confirm-password").addClass("fa-eye-slash");
        }
     });
        
     $("#globalButton").click(function()
    	{
    	var current_day = $("#day_value").text();
    	var choice_day = $("#avgworkday option:selected").val();

    	var current_speed = $("#speed_value").text();
    	var choice_speed = $("#avgmovspeed option:selected").val();

    	if( ((choice_day).trim() == (current_day).trim())  && ((choice_speed).trim()==(current_speed).trim()) ){
            alert("You did not change anything !");
            return false
    	}
    	else{
    		alert("Update The System Settings Successfully!");
    	}

    });

//Work For Tab#2-------------Users Table
    $("#add").click(function(){  //Add One New User
        $("#edit").show();
        $("#edit").trigger('click');
        var url = $('#user-form').attr("action");
        url = "/admin/add";
        $("#user-form").prop("action", url); 
        $("#user-title").text("Add New User");
        $("#reset" ).trigger( "click" );
        $('#password').prop( "disabled", false );
        $('#toggle-password').prop( "disabled", false );
        $('#confirm-password').prop( "disabled", false );
        $('#toggle-confirm-password').prop( "disabled", false );

    });

    $("#edit-btn").click(function(){  //Add One New User
        $("#edit").show();
        $("#edit").trigger('click');
        $("#user-title").text("Edit Selected User");
        var index = this.closest('tr').rowIndex;
        var name = $('#user-table tr:eq('+index+') td:eq(0)').text();
        $('#name').prop("value", name.trim());

        var email = $('#user-table tr:eq('+index+') td:eq(1)').text();
        $('#email').prop("value", email.trim());
        url = "/admin/edit/"+ email;

        $("#user-form").prop("action", url); 
        $('#password').prop('disabled', true);
        $('#confirm-password').prop('disabled', true);
        $('#toggle-password').prop('disabled', true);
        $('#toggle-confirm-password').prop('disabled', true);

        var role_text = $('#user-table tr:eq('+index+') td:eq(2)').text(); 
        var roles = role_text.split(",");
      $('#check-admin').prop('checked', false);
      $('#check-manager').prop('checked', false);
      $('#check-canvasser').prop('checked', false);
      if (roles != null){
         for (i = 0; i < roles.length; i++)  { 
            var role = roles[i].replace(/\s+/g, '');
            if(role == "admin"){
              $('#check-admin').prop('checked', true);
                 }
            else if(role == "manager"){
                 $('#check-manager').prop('checked',true);
              }
            else if(role == "canvasser"){
                $('#check-canvasser').prop('checked',true);
             } 
        } 
    }
     var avatar= $('#user-table tr:eq('+index+') td:eq(3)').text();
     if(avatar.trim() =="None"){
        document.getElementById('avatar').src="/static/image/profile/avatar.png";
     }
    else{
        var im = avatar.trim();
        if (im != null ){
            var s = "/static/image/profile/" + im ;
            $('#avatar').prop('src', s);
        }
      }
    });

 
    $("#cancel").click(function(){  // Go back to user table
        $("#users").trigger('click');
        $("#edit").hide();   
    });
    
//Hide or show password
    $("#toggle-password").click(function() {
        var type = $("#password").attr('type');
        if (type.trim() == "text"){
             $("#password").prop("type", "password");
             if ($("#toggle-password").hasClass('fa-eye')){
                 $("#toggle-password").removeClass("fa-eye");
                 $("#toggle-password").addClass("fa-eye-slash");
           }
        }
        else{
            if ($("#toggle-password").hasClass('fa-eye-slash')){
                 $("#password").prop("type", "text");
                 $("#toggle-password").addClass("fa-eye");
                 $("#toggle-password").removeClass("fa-eye-slash");
            }
        }

    });

    $("#toggle-confirm-password").click(function() {
        var type = $("#confirm-password").attr('type');
        if (type.trim() == "text"){
             $("#confirm-password").prop("type", "password");
            if ($("#toggle-confirm-password").hasClass('fa-eye')){
             $("#toggle-confirm-password").removeClass("fa-eye");
             $("#toggle-confirm-password").addClass("fa-eye-slash");
         }
        }
        else{
             $("#confirm-password").prop("type", "text");
        if ($("#toggle-confirm-password").hasClass('fa-eye-slash')){
             $("#toggle-confirm-password").addClass("fa-eye");
             $("#toggle-confirm-password").removeClass("fa-eye-slash");
        }
    }

    });

//  Dynamic update the image  if there's any file selected.  
    $('#file').change(function(){
         if(this.files && this.files[0]){
              var reader = new FileReader(); 
                reader.onload = function(e){
                    $('#avatar').attr('src', e.target.result);
                }
               reader.readAsDataURL(this.files[0]);
                alert("Upload Successfully");
             }
    });


});
