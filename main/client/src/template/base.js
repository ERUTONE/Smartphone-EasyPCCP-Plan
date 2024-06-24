function setRootFontSize(){ 
    // .containerの要素を取得する例
    const containerStyles = window.getComputedStyle(document.querySelector('.container'));

    const gridColumnValue = containerStyles.getPropertyValue('grid-template-columns'); // 00px 00px 00px...の形式
    const gridRowValue = containerStyles.getPropertyValue('grid-template-rows');
    const gridCols = gridColumnValue.trim().split(/\s+/).length; //空白文字で分割して配列の長さを取得
    const gridRows = gridRowValue.trim().split(/\s+/).length;
    console.log("gridCols: ",gridCols, ", gridRows: ",gridRows);

    const window_ratio = window.innerWidth / window.innerHeight;
    console.log("window_ratio: ",window_ratio);

    var fontSize;
    if( window_ratio < gridCols / gridRows ) {
        // containerの横幅を優先
        fontSize = `${8/gridCols}vw`;
    }else{
        // containerの縦幅を優先
        fontSize = `${8/gridRows}vh`;
    }

    // :rootのfont-sizeに適用する例
    document.documentElement.style.fontSize = fontSize;
    console.log("fontSize: ",fontSize);
}
window.addEventListener("resize", setRootFontSize);
setRootFontSize();
// ------------------------------------------------ //

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
            // console.log("Success:",responce);

            if (Object.values(responce).includes("reload")) {
                location.reload();
            }
        },
        error: function(xhr, status, error) {
            // リクエストが失敗した場合の処理
            console.error('Error:', status, error);
        }
    }).then(response => {
    }).catch(error => {
    });
}

// ------------------------------------------------ //

const sliders = document.getElementsByClassName('slider');
for (let i = 0; i < sliders.length; i++) {
    sliders[i].addEventListener('input', function(event) {
        // SendData
        sendData({preventDefault: () => {}, submitter: {name: sliders[i].name, value: event.target.value}});
    });
}

function updateSlider(direction) {
    const slider_horizontal = document.getElementsByClassName(`slider_${direction}`);
    // get CSS variable
    const computedStyle = getComputedStyle(document.documentElement);
    const activeColor = computedStyle.getPropertyValue('--accent-color').trim();
    const baseColor = computedStyle.getPropertyValue('--base-color').trim();
    for (let i = 0; i < slider_horizontal.length; i++) {
        slider_horizontal[i].addEventListener('input', function(event) {
            // Gradient
            const value = event.target.value / event.target.max * 100;
            const dir = (direction === "horizontal") ? "to right" : "to top";
            slider_horizontal[i].style.background = `linear-gradient(${dir}, ${activeColor} ${value}%, ${baseColor} ${value}%)`;
        });
    }
}

updateSlider("horizontal");
updateSlider("vertical");

