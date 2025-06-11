$(document).ready(function(){
    $("#addimage").click(function(){
        $("#imagelist").val(image_file)
    })
   
    $(".addimagebutton").click(function(){
        var product = document.getElementById("editproducts");
        if (product.style.display === 'block')
        product.style.display = 'none'
        else
        product.style.display = 'block'
    })

    let image_file = document.getElementById("imagedata").value
    image_file = image_file.split(',')
    var product = $("#productimage");
    
    for(i=0;i<image_file.length;i++){
        if(image_file[i] != ""){
            var image = $("<img/>");
            image.attr({'src':"/static/products/"+image_file[i],
            "class":"m-1 rounded-lg shadow-s w-1/2 hover:shadow-2xl"});
            var svg = document.createElement('a');
        svg.innerHTML = `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M15.8333 2.5H4.16667C3.24619 2.5 2.5 3.24619 2.5 4.16667V15.8333C2.5 16.7538 3.24619 17.5 4.16667 17.5H15.8333C16.7538 17.5 17.5 16.7538 17.5 15.8333V4.16667C17.5 3.24619 16.7538 2.5 15.8333 2.5Z" stroke="black" stroke-width="0.666667" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M7.5 7.5L12.5 12.5" stroke="black" stroke-width="0.666667" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12.5 7.5L7.5 12.5" stroke="black" stroke-width="0.666667" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
            svg.setAttribute('class'," removeimage cursor-pointer bg-gray-50 absolute top-0 right-1/2");
            var div = $("<div></div>").attr("class","relative");
            div.append(image);
            div.append(svg);
            product.append(div);
        }
    }

    $(".removeimage").click(function(){
        var parent_image = $(this).parent();
        var src = parent_image.children('img').attr('src')
        src = src.split('/').pop();
        const index = image_file.indexOf(src);
        if (index > -1) { 
        image_file.splice(index, 1); 
        }
        console.log(image_file)
        parent_image.remove()
    })
});