from modules import preprocessing, learning, predicting


def main():
    processing_type = input('データのスクレイピング:s, csvファイルからデータ読み込み:r : ')

    df = preprocessing.main(processing_type)

    processing_type = input('モデル作成:c, txtファイルからモデル読み込み:r : ')

    lgb_model = learning.main(processing_type, df)

    predicting.predict(lgb_model)


if __name__ == '__main__':
    main()
