$(document).ready(function () {
    $('.PaywithRazorpay').click(function (e){
        e.preventDefault();

        
        var address = $("[name='address']:checked").val();

         
        var token = $("[name='csrfmiddlewaretoken']").val()
        
        console.log(address,"address")
        var first_name = $("[name='first_name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        // var Address1 = $("[name='Address1']").val();
        // var Address2 = $("[name='Address2']").val();
        // var zipcode = $("[name='zipcode']").val();
        // var city = $("[name='city']").val();
        // var country = $("[name='country']").val();
        // var ordernote = $("[name='ordernote']").val();

        // if(first_name == "" || email == "" || phone == "" || Address1 == "" ||  Address2 == "" || zipcode == "" || city == "" || zipcode == "" || country == "" || ordernote == "")
        // {
        //     alert("All fields mandatory")
        //     return false;
        // }
        if(!address)
        {
            swal("Alert!", "Address required!", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url:"/order/proceedtopay/",
                success: function (response) {
                    // console.log(response);

                    var options = {
                        "key": "rzp_test_c4jaB44kt7fHck", // Enter the Key ID generated from the Dashboard
                        "amount": 1*100,//response.grand_total * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "AuraEcom", //your business name
                        "description": "Thank You for buying from us",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data = {
                                "address": address,
                                "payment":"Razorpay",
                                "payment_id":responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                                
                            }
                            $.ajax({
                                method:"POST",
                                url:"/order/placeorder/",
                                data:data,
                                dataType:"dataType",
                                success: function(responsec){
                                    console.log(responsec)
                                    swal("Congratulations!", responsec.status,"success").then((value) => {
                                        window.location.href = '/order/UserOrdersPage/'
                                    });
                                }
                            });
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": first_name, //your customer's name
                            "email": email, 
                            "contact": phone  //Provide the customer's phone number for better conversion rates 
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();


                    
                }
            });
        

            
        }
});

    
});