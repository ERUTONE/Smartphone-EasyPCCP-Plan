function sendData(e) {
    // ajaxでデータを送信
    e.preventDefault();
    const submitter = e.submitter.name;
    const value = e.submitter.value;
    // {submitter : value}の形で送信

    $.ajax({
        url: "/action",
        type: 'POST',
        data: JSON.stringify({[submitter]: value}),
        contentType: 'application/json',
        success: function(responce) {
            console.log("Success:",responce);

            console.log(Object.values(responce));
            if (Object.values(responce).includes("reload")) {
                location.reload();
            }
        },
        error: function(xhr, status, error) {
            // リクエストが失敗した場合の処理
            console.error('Error:', status, error);
        }
    });
}

// ------------------------------------------------ //

// sliderの値が変更されたときにSendDataを呼び出す

const sliders = document.getElementsByClassName('slider');
for (let i = 0; i < sliders.length; i++) {
    sliders[i].addEventListener('input', function(event) {
        sendData({preventDefault: () => {}, submitter: {name: sliders[i].name, value: event.target.value}});
    });
}