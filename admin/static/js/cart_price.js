$(document).ready(function(){
    $(".editcartprice").click(function(){
        var id = $(this).val()
        console.log(id)
        $.getJSON('/edit_cart_price/'+id,function(data){
            console.log(data)
            var form = document.getElementById('editform');
            form.innerHTML = `
            <div class="w-full h-full absolute top-0 left-0 bg-opacity-80 bg-black">  </div>
            <section class="flex justify-center z-10">
                <div class="w-2/6 flex text-white z-50 justify-end ml-8 mt-7"><a href="/admin/cartprice">X</a></div>
                <div class="absolute top-1/3 bg-white w-2/6 p-8 shadow-xl rounded-xl -mt-4">
                    <form method='post' action="/admin/cartprice?product_id=${id}" class="space-y-4">
                        <div>
                            <label class="text-gray-700 p-2">Product Name :</label>
                            <label id="productname" class="text-gray-700 p-2 capitalize">${data.name}</label>
                        </div>
                        <div>
                            <label class="text-gray-700 p-2">Cart Price</label>
                            <input type="number" id="cart_price" name="cart_price" value="${data.price}" class="text-sm border border-gray-300 rounded-lg p-2 px-4 w-1/2">
                        </div>
                        <div>
                            <button id="savebutton" class="bg-violet-600 text-white rounded-lg p-2 text-sm">Save</button>
                        </div>
                    </form>
                </div>
            </section>`
        });
       
    });
})