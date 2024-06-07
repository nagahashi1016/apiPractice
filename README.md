### カメラデータAPI

このAPIは、カメラデータに対する基本的なCRUD操作を提供します。SQLiteデータベース「dataAPI.sqlite」とやり取りします。

#### ベースURL
アプリケーションがローカルで実行されている場合、ベースURLは `http://127.0.0.1:8000` になります。

### エンドポイント

#### 1. **カメラデータの取得**
   - **エンドポイント:** `/get/`
   - **メソッド:** `GET`
   - **説明:** 指定されたフィルタに基づいてカメラデータを取得します。
   - **クエリパラメータ:**
     - `id` (int): カメラID
     - `name` (str): カメラ名
     - `type` (str): カメラタイプ
     - `sensorSize` (str): センサーサイズ
     - `pixelNumber` (int): ピクセル数
     - `maker` (str): カメラメーカー
     - `lensMounts` (str): レンズマウント
     - `imageSta` (str): 画像安定化
     - `price` (int): カメラ価格
     - `releaseDate` (str): 発売日
     - `URL` (str): カメラURL

#### 2. **カメラデータの挿入**
   - **エンドポイント:** `/post/`
   - **メソッド:** `POST`
   - **説明:** データベースに新しいカメラデータを挿入します。
   - **クエリパラメータ:**
     - `name` (str): カメラ名
     - `type` (str): カメラタイプ
     - `sensorSize` (str): センサーサイズ
     - `pixelNumber` (int): ピクセル数
     - `maker` (str): カメラメーカー
     - `lensMounts` (str): レンズマウント
     - `imageSta` (str): 画像安定化
     - `price` (int): カメラ価格
     - `releaseDate` (str): 発売日
     - `URL` (str): カメラURL

#### 3. **カメラデータの更新**
   - **エンドポイント:** `/patch/`
   - **メソッド:** `PATCH`
   - **説明:** 指定された条件に基づいて既存のカメラデータを更新します。
   - **クエリパラメータ:**
     - `name` (Optional[str]): 名前の新しい値
     - `type` (Optional[str]): 更新対象レコードを識別するためのカメラタイプ
     - `sensorSize` (Optional[str]): センサーサイズの新しい値
     - `pixelNumber` (Optional[int]): ピクセル数の新しい値
     - `maker` (Optional[str]): メーカーの新しい値
     - `lensMounts` (Optional[str]): レンズマウントの新しい値
     - `imageSta` (Optional[str]): 画像安定化の新しい値
     - `price` (Optional[int]): 価格の新しい値
     - `releaseDate` (Optional[str]): 発売日の新しい値
     - `URL` (Optional[str]): URLの新しい値
     - `where_id` (Optional[int]): IDのWHERE句に追加の条件

#### 4. **カメラデータの削除**
   - **エンドポイント:** `/delete/`
   - **メソッド:** `DELETE`
   - **説明:** 指定された条件に基づいてカメラデータを削除します。
   - **クエリパラメータ:**
     - `id` (Optional[int]): 削除対象レコードを識別するためのカメラID
