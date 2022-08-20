Asana2Excel
=======
AsanaからエクスポートしたデータをExcelのWBSに変換するツールです。

実行には下記のライブラリが必要です。
* openpyxl


Example 
------
1. pip3 install openpyxl
1. python3 python3 src/asana2excel.py test/sample.json test/sample.csv test/out.xlsx
  - test/sample.json: Asanaからexportしたjsonファイル 
  - test/sample.csv: Asanaからexportしたcsvファイル（依存関係を取得するために使用）
  - test/out.xlsx: 出力するファイル

