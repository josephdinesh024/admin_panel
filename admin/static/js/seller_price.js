$(document).ready(function(){    
    $("#category_id").change(function(){
      var id = $(this).val();
      $.getJSON('/get_product/'+id,function(data){
        var $productname = $("#product_name");
        $productname.empty();
        $.each(data,function(id,name){
          $productname.append($('<option></option>').val(id).text(name));
        });
      });
    });

    $("#product_name").change(function(){
      var id = $(this).val();
      $.getJSON('/get_price/'+id,function(data){
        var $price = $("#price");
        //$price.attr("value",data.price)
        $price.val(data.price)
      });
    })

    $("button").click(function(){
      var image_data = $("#image")
      var error_para = $("#p")
      if (image_data.val() ==""){
        error_para.text("Image field should not be empty")
        error_para.addClass("text-red-500")
        $("#labelerror").removeClass("border-green-400")
        $("#labelerror").addClass("border-red-400")
      }
    })
})