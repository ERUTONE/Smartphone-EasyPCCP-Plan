function setRootFontSize(){ 
    // .containerの要素を取得する例
    const containerStyles = window.getComputedStyle(document.querySelector('.container'));

    const gridColumnValue = containerStyles.getPropertyValue('grid-template-columns'); // 00px 00px 00px...の形式
    const gridRowValue = containerStyles.getPropertyValue('grid-template-rows');
    const gridCols = gridColumnValue.trim().split(/\s+/).length; //空白文字で分割して配列の長さを取得
    const gridRows = gridRowValue.trim().split(/\s+/).length;

    const window_ratio = window.innerWidth / window.innerHeight;

    var fontSize;
    if( window_ratio < gridCols / gridRows ) {
        // containerの横幅を優先
        fontSize = `${8/gridCols}vw`;
    }else{
        // containerの縦幅を優先
        fontSize = `${8/gridRows}svh`;
    }

    // :rootのfont-sizeに適用する例
    document.documentElement.style.fontSize = fontSize;
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

function updateSliderGradient(slider, direction) {
    // Gradient// max 属性の値が省略されている場合は100を設定
    if(!slider.max) {
        slider.max = 100;
    }
    // 現在の値から割合（%）を取得
    const progress = (slider.value / slider.max) * 100;
    // linear-gradient で Track の色を設定
    const dir = (direction === "horizontal") ? "to right" : "to top";
    slider.style.background = `linear-gradient(${dir}, ${sld_activeColor} ${progress}%, ${sld_baseColor} ${progress}%)`;
}

function initSliders(){

    // visual & sender init
    const updateSliders = (direction) => {
        const sliders = document.querySelectorAll(`.slider_${direction}`);
        sliders.forEach((slider) => {
            
            slider.addEventListener('input', (e) => {
                updateSliderGradient(e.target, direction);
                sendData({preventDefault: () => {}, submitter: {name: slider.name, value: e.target.value}});
            });
            updateSliderGradient(slider, direction);
        });
    }
    updateSliders("horizontal");
    updateSliders("vertical");
}

// get CSS variable
const computedStyle = getComputedStyle(document.documentElement);
const sld_activeColor = computedStyle.getPropertyValue('--accent-color').trim();
const sld_baseColor = computedStyle.getPropertyValue('--base-color').trim();
initSliders();