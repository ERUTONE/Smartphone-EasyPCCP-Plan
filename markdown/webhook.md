# webhook 仕組みを考える

## 更新されるべきタイミング

- {{format.text()}}の中身が変わった時
- スライドバーの値が変わった時
  - value={{...}}なので実質同じ？

## 更新があるかチェック

- 1秒ごとにfunctionを実行、前回の実行結果と比較。
- 比較した結果が変わっていたらnotify

## 更新チェック用のリストに追加

- 形式？
- 名前？

## 受け取ったらwebエレメントを更新

- addEventListner()のイベント名をcssidに
jsでなんとかして更新できるように...。