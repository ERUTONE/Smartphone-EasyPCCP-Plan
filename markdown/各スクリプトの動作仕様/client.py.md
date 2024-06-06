# 動作仕様 | client.py

layoutからjsonを一つ指定

```json
{
    "grid-columns":4,
    "grid-rows":2,
    "placement":[
        {
            "widget":"texttest.1-1",
            "position": [3,2]
        }
    ]
}
```

ここからcssを作る
- grid-template-columnsとか
- positionとwidgetの1-1とかから計算して、「column 開始/終了」「row 開始/終了」
  をforに出てきた順にidとして指定する

できたら、widgetの内容のjsonを検索、呼び出す。
widget.pyに全部作ってもらったwidget-divを、base.htmlにぶち込む

完成したhtmlは、保存しとく

リクエストきたらそのままreturnして表示させる
再生成？別でそういうpostリクエストやりゃいい
URLくるたびに生成してらんないと思う