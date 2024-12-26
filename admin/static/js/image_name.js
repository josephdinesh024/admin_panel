$(document).ready(function(){
    $("#image").change(function(event){
        var p = document.getElementById('p');
        var text = "Files "
        var files = event.target.files;
        for(i=0;i<files.length;i++)
            text += files[i].name+"; "
        p.textContent =text

        var add_button = $("#addimage");
        add_button.removeClass("hidden")
    });
})