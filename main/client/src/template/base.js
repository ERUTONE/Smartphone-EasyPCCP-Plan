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

document.addEventListener('DOMContentLoaded', () => {
 
    // 全てのレンジスライダーの要素を取得（必要に応じてセレクタを変更）
    const rangeSliders = document.querySelectorAll('.slider');
    // Track の元の色
    const baseColor = '#eee';
    // Track のつまみの左側の部分の色
    const activeColor = 'var(--accent-color)';
   
    // 取得したレンジスライダーの各要素に対して実行
    rangeSliders.forEach((slider) => {
      // input イベントのリスナーを設定
      slider.addEventListener('input', (e) => {
        // updateSlider を呼び出す
        updateSlider(e.target);
      });
      // updateSlider を実行して現在の値を反映
      updateSlider(slider);
    });
   
    // input イベントで呼び出される関数（トラックの塗りの範囲と色を設定する関数）
    function updateSlider(slider) {
      // max 属性の値が省略されている場合は100を設定
      if(!slider.max) {
        slider.max = 100;
      }
      // 現在の値から割合（%）を取得
      const progress = (slider.value / slider.max) * 100;
      // linear-gradient で Track の色を設定
      slider.style.background = `linear-gradient(to top, ${activeColor} ${progress}%, ${baseColor} ${progress}%)`;
    }
   
});