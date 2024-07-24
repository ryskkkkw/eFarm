# はじめに

このプロジェクトはPython,Djangoを独学したアウトプットとして作成した最初のポートフォリオです。  
次の項目に沿って、ポートフォリオについて説明します。

1. プロジェクトについて
2. ディレクトリ構成
3. 各ディレクトリの詳細

<br>

# 1.　プロジェクトについて

初めてのポートフォリオとして架空の簡易なECサイトを作成しました。ECサイトを作成した理由は、基本的なCRUD操作を実践できること、一般的なWebサービスなので完成形や実装する機能がイメージしやすいためです。また、テーマがある方がより完成形をイメージしやすいため、規格外の廃棄野菜や果物を売買するECサイトを想定し、プロジェクト名を「eFarm」としました。  

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

