# はじめに

このプロジェクトはPython,Djangoを独学したアウトプットとして作成した最初のポートフォリオです。  
次の項目に沿って、ポートフォリオについて説明します。

1. プロジェクトについて
2. ディレクトリ構成
3. 主なディレクトリの説明

<br>

# 1.　プロジェクトについて

初めてのポートフォリオとして架空の簡易なECサイトを作成しました。ECサイトを作成した理由は、基本的なCRUD操作を実装できること、一般的なWebサービスなので完成形や機能がイメージしやすいためです。また、テーマがある方がより実践的に取り組めるため、規格外で本来は廃棄となる野菜や果物を売買するECサイトを想定し、プロジェクト名を「eFarm」としました。 

架空のサービスではありますが、一般的なECサイトのマーケットプレイスのように、売り手と買い手が存在し、売り手は商品の登録や変更、削除、買い手は商品の検索、決済、購入履歴の確認といった操作を行えるようにしています。ホスティングもしていますので、実際に[eFarm](https://rkrk.pythonanywhere.com/)を確認することができます。

<br>

# 2.ディレクトリ構成

プロジェクトディレクトリの主な構成は以下のとおりです。


    eFarm
    ├── accounts
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── carts
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── config
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   └── production.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── media
    │   └── uploads
    │       └── product_imgs
    ├── payments
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── products
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── requirements.txt
    ├── static
    │   └── style.css
    ├── templates
    │   ├── accounts
    │   ├── base.html
    │   ├── carts
    │   ├── payments
    │   └── products
    └── tests
        ├── test1.jpg
        ├── test2.jpg
        ├── test_accounts.py
        ├── test_carts.py
        ├── test_payments.py
        └── test_products.py

<br>

# 3.主なディレクトリの説明

## accounts
- ユーザーの認証に関する機能を持つアプリケーションです。
- CustomUser,Buyer,Sellerの3つのモデルを実装しています。
- CustomUserは全ユーザーの識別子としてのemailといくつかのフラグのフィールドのみを持ち、その他のユーザー情報はBuyerまたはSellerモデルで登録します。CustomUserはBuyerまたはSellerオブジェクトと一対一関係になっています。
- ユーザー登録のフローは次のようになっています。
  1. BuyerまたはSellerの登録リンクから始めにCustomUserの登録を行う。登録のurlパスにはそれぞれbuyerまたはsellerのrollパラメータが含まれている。
  2. CustomUserのemail,パスワードの登録をする際に、rollパラメータに基づきCustomUserのis_buyerまたはis_sellerのフラグをFalseからTrueにする。
  3. CustomUserの登録が終わったら完了画面に遷移する。完了画面にはログインのリンクがある。
  4. ログインの際に、CustomUserのis_profileフラグがFalseである場合、is_buyerがTrueであればBuyerの登録、is_sellerがTrueであればSellerの登録に遷移する。is_profileがTrue（BuyerまたはSellerが登録済）の場合は商品一覧画面に遷移する。
  5. BuyerまたはSellerの登録する際は、関連付けられているCustomUserのis_profileフラグをTrueにした上で、登録した内容を表示するプロフィール画面に遷移する。
- パスワードの変更、リセットにはDjangoのPasswordChangeViewやPasswordResetViewなどをそのまま利用しています。
- PasswordResetViewではメールが送信されるので、[mailtrap](https://mailtrap.io/ja/email-sandbox/)を利用してhtmlメールでのパスワードリセットのフローを確認しました。また、コンソールバックエンドを設定し、開発途中の確認として標準出力されるリンクからパスワードリセットを行う方法も試しています。

## products
- 商品の登録や表示、検索などを実行するアプリケーションです。
- 実装しているモデルはProductモデルの1つだけです。
- ProductはSellerオブジェクトと多対一関係になっています。
- Productモデルにはimageフィールドがあるので、商品の画像ファイルも登録できます。
- 画像ファイルはmedia/uploads/producut_imgsにアップロードされます。アップロードの過程で、ファイルをリサイズし、ファイル名はタイムスタンプ（UNIX時間）+ユーザーIDになるようにしています。
- 画像ファイルを更新するときは、新しいファイルの登録後に上記パスにある古いファイルが削除されます。
- 商品一覧の表示は、ユーザーがSellerの場合は自身の登録商品のみが表示されます。ユーザーがBuyerまたは未登録の場合は全商品が表示されます（ユーザー未登録でも商品は表示されます）。
- 商品一覧から特定の商品を検索することもできます。検索フローは次のようになっています。
  1. 商品一覧画面の検索バーに文字を入力、検索ボタンを押下すると、HttpRequestオブジェクトのキーにsearchが含まれる。searchが含まれている場合は商品検索の処理が実行される。
  2. searchの値は検索バーに入力した文字列となっている。複数の単語で検索が行われたときのために、取得した値はスペース区切りのリストにしてwords変数に格納する。
  3. forループでwordsのリスト内にある単語を一つずつ処理する。検索したユーザーがBuyerまたはユーザー未登録者であればProductオブジェクト全件に対して、Sellerであれば自身の登録したProductオブジェクトに対して検索を行う。
  4. 検索はProductオブジェクトの商品名または関連付けられているSellerの農園名に、検索する単語が含まれているProductオブジェクトを抽出する。
  5. 全ての単語の検索が終わり該当する商品があれば、その商品のみユーザーに表示される。該当商品がない場合はNOT Resultと表示される。
- 商品一覧から商品詳細に遷移すると、商品名や商品説明、個数や価格が表示されます。Productモデルのpriceフィールドは税抜価格となっているため、商品詳細画面で価格を表示する際には、同モデル内で定義したprice_with_tax関数から税込価格を表示するようにしています。priceフィールドを税抜価格にし、税込価格は関数で計算するようにしたのは、消費税率の変更を考慮したためです（現在はtax=0.1で設定）。
- 商品詳細から商品を登録したSellerの詳細画面へ遷移することもできます。また、ユーザーがBuyerの場合は商品の購入個数を選択してカートに入れることができます。ユーザー未登録者の場合はカートのフォームは表示されません。

## carts
- 購入予定の商品を決済前に一時保存するアプリケーションです。
- Cart,CartItemの2つのモデルを実装しています。
- CartはBuyerオブジェクトと多対一関係、CartItemはCartオブジェクトと多対一関係になっています。
- カートに商品を登録するフローは次のようになっています。
  1. 商品詳細画面で購入個数を選択し、カートボタンを押下する。
  2. Buyerに関連付けられているCartオブジェクトが既にある場合は、そのCartオブジェクトを取得する。関連付けられているCartオブジェクトが存在しない場合は、新規でCartオブジェクトを作成してBuyerに関連付ける。
  3. カート登録のurlパスにはproduct_idのパラメータがあるため、そこから商品情報を取得する。また、カート登録のHttpRequestオブジェクトにあるamountキーから、購入個数を取得する。
  4. Cartに関連付けられているCartItemオブジェクトに同じ商品がある場合は購入個数と金額を更新する。同じ商品がない場合は新たにCartItemを作成する。
  5. CartやCartItemの登録が終わったら、カート詳細画面に遷移する。
- カート詳細画面ではカートに入れた各商品の個数の更新やカートからの削除ができます。また、Checkoutボタンから決済手続きに進むことができます。
