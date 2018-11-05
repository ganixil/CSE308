$(document).ready(function(){    // Instantiate UI tabs vertical
 
// Hide or show password
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
             $("#toggle-confirm-password").removeClass("fa-eye");
             $("#toggle-confirm-password").addClass("fa-eye-slash");
        }
        else{
             $("#confirm-password").prop("type", "text");
             $("#toggle-confirm-password").addClass("fa-eye");
             $("#toggle-confirm-password").removeClass("fa-eye-slash");
        }

    });

  // Dynamic update the image  if there's any file selected.  
    $('#file').change(function(){
         if(this.files && this.files[0]){
              var reader = new FileReader();
                reader.onload = function(e){
                    $('#profile-avatar').attr('src', e.target.result);
                }
               reader.readAsDataURL(this.files[0]);
                alert("Upload Successfully");
             }
            
    });

    $("#submit-info").click(function(){
        var ps = $("#password").val();
        var ps1 = $("#confirm-password").val();
        if (ps != ps1){
             alert("The password does not match")
             $( "#reset" ).trigger( "click" );
             return false;
         }
    });


  window.setTimeout(function() {
    $("#error").fadeTo(1000, 0).slideUp(1000, function(){
        $(this).hide(); 
    });
}, 2000);

});