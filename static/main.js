var csrftoken = $('meta[name=csrf-token]').attr('content');

$("input[class='main']").inputSpinner();

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

$( document ).ready(function() {
    $("input[name='phone']").mask("+7 (999) 999-99-99");
    for(var i=0, len=localStorage.length; i<len; i++) {
        var key = localStorage.key(i);
        var value = localStorage[key];
        if(key.slice(0, 5) == "input") {
            $(key).val(value)
        } else {
}          $(key).html(value);
     };

    if(localStorage.data==undefined) { localStorage.data=String("{}")}
    if(localStorage.mls_sum==undefined) { localStorage.mls_sum="{}"}

    $("input[class='main']").on('input', function (e) {
    let mls_cnt = JSON.parse(localStorage.data);
    let mls_sum = JSON.parse(localStorage.mls_sum);
    let val = Number($(this).val())
    mls_cnt[this.id] = val;
    let sum_el = this.getAttribute('price') * val;
    $('span.sum'+this.id).html('∑' + sum_el + '₽')
    mls_sum[this.id] = sum_el;
    let cnt = Object.values(mls_cnt).reduce((a, b) => a + b, 0);
    let sum = Object.values(mls_sum).reduce((a, b) => a + b, 0);
    $('#qnt').html(cnt);
    $('#sum').html(sum);
    let cart_text = '🛒';
    if (sum_el != 0) {
        cart_text = '🛒: '+String(sum_el)+'₽';
    }
    if (val == 0) {
        $("tr[id="+this.id+"]").hide()
        $("div.alert.alert-warning[id=1]").fadeIn(500).delay(2000).fadeOut(500);
    }
    $('#b'.concat(this.id)).html(cart_text);
    localStorage.data = JSON.stringify(mls_cnt);
    localStorage.mls_sum = JSON.stringify(mls_sum);
    localStorage.setItem('#qnt', cnt);
    localStorage.setItem('#sum', sum);
    localStorage.setItem('#b'.concat(this.id), cart_text);
    localStorage.setItem("input[type=\'number\'][id=\'"+String(this.id)+"\']", $(this).val());
    $.ajax({
        type: "POST",
        url: "/addtocart/",
        data: JSON.stringify(mls_cnt),
        contentType: "application/json",
        method: 'POST',
    });
});
    $("tbody").on('input', 'input[class=\'spinner\']', function (e) {
        console.log(ok)
    });
});

$(function() {
  $("form[name='cart']").validate({
    rules: {
      name: "required",
      address: "required",
      email: {
        required: true,
        email: true
      },
      phone: "required"
    },
    // Specify validation error messages
    messages: {
      name: "Пожалуйста введите имя",
      address: "Пожалуйста введите адрес",
      email: {
        required: "Пожалуйста введите почту",
      },
      phone: "Пожалуйста введите телефон"
    },
    submitHandler: function(form) {
      localStorage.clear();
      form.submit();
    }
  });
});