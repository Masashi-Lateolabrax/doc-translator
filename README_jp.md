# doc-translator

各種ドキュメントファイルを可能な限りフォーマットを崩さないで翻訳するためのプログラムです．

## Support

### Formats

| Format | Details                  | Version | Status  |
|--------|--------------------------|---------|---------|
| docx   | Microsoft Word Documents | -       | Planned |
| md     | Mark Down                | -       | Planned |

### Translator

| Translator | Version | Status  |
|------------|---------|---------|
| ChatGPT    | -       | Planned |

## For Python Developers

### How to install this as a library?

Currently, this library is not registered on PyPI, so you have to install it from the GitHub repository.

**PIP Users**

```commandline
pip install git+https://github.com/Masashi-Lateolabrax/doc-translator
```

### Git Prefix

| Prefix | Description                    |
|--------|--------------------------------|
| add    | ファイルや関数，クラスなどを追加したときに使用        |
| mov    | ファイルや関数，クラスなどを移動したときに使用        |
| rem    | ファイルや関数，クラスなどを消去したときに使用        |
| mod    | インターフェイスの変更を伴わない変更を行ったときに使用    |
| fix    | バグを修正し問題の解決が確認されたときに使用         |
| doc    | ドキュメントファイルやDocStringを変更したときに使用 |

ドキュメントファイルを追加・移動・消去した場合は*add*・*mov*・*rem*ではなく*doc*を優先して使ってください．

破壊的な変更がある場合，*add*や*mod*，*fix*は使用しないでください．

例えば，バグの修正に破壊的な変更が必要であれば，新しい関数を定義しそれを*add*プレフィックスでコミットした後，その新しい関数で置き換えたバージョンを
*fix*プレフィックスでコミットしてください．

このとき*add*プレフィックスのコミット時，もしくは後から*doc*プレフィックスでバグの要因となった関数に非推奨であることがわかるような記載を行ってください．

### Branching Strategy

| Branch  | Description          | Marge Destinations |
|---------|----------------------|--------------------|
| main    | 公開用のブランチ             | -                  |
| root    | 新規ブランチの元となるブランチ      | feat/*, share      |
| feat/*  | 機能ごとに独立して開発するためのブランチ | development        |
| develop | 各機能を統合するためのブランチ      | main               |
| share   | 各機能で共有する部分の開発用ブランチ   | root               |