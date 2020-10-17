# _*_ cording: utf-8 _*_
import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import csv

class DatasetCreater():
    '''
    analyze：ダウンロードしたcsvファイルから'いいね'のヒストグラムを保存.
    　　　　　平均以上の'いいね'を獲得したtweetのcsvを作成．
    create：srcとなるcsvファイルから平均以上の'いいね'を獲得したtweetとそうでないものをラベリングし
    　　　　 train, validation, testに分割したcsvファイルを作成
    '''
    def __init__(self, src_path, account='@nikkei.csv'):
        self.account = account
        self.src = pd.read_csv(src_path, encoding="shift-jis")
    
    def create(self, train_rate=0.8, val_rate=0.1, test_rate=0.1):

        if not os.path.isdir('Datasets'):
            os.mkdir('Datasets')

        save_dir = os.path.join('Datasets', self.account[:-4])
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        text = self.src['text']
        like = self.src['like']

        # split to binary category
        mean = like.mean()
        label = like.mask(like < mean, 0)
        label = label.mask(label >= mean, 1)
        
        # remove unneccesary word
        text = self.remove(text, target='\n')
        text = self.remove(text, target='　')

        # join
        COLOMN = 1
        whole = pd.concat([text, label], axis=COLOMN)
        print(whole.head)

        # split
        train_max = math.ceil(len(whole)*train_rate)
        val_max = train_max + math.ceil(len(whole)*val_rate)
        train = whole[0:train_max]
        validation = whole[train_max:val_max]
        test = whole[val_max:]

        # save
        train.to_csv(os.path.join(save_dir, 'train.csv'), encoding='shift-jis')
        validation.to_csv(os.path.join(save_dir, 'validation.csv'), encoding='shift-jis')
        test.to_csv(os.path.join(save_dir, 'test.csv'), encoding='shift-jis')

        print("=====> Created Datasets!")

    def remove(self, src, target='\n'):
        removed = src.apply(lambda d: d.replace(target, ''))
        print(removed.head)
        return(removed)

    def analyze(self, ):
        csv_dir = 'csv'
        img_dir = 'img'
        df = pd.read_csv(self.account, encoding='shift_jis')
        total_tweets = df.shape[0]
        target = ['like', 'retweet']

        if not os.path.isdir(img_dir):
            os.mkdir(img_dir)
        
        try:
            os.path.isdir(csv_dir)
        except FileNotFoundError:
            print("[Error] Not found src directory 'csv'. You need making it using tweet_downloader.py before running this script.")

        for user_action in target:
            mean = self.histgram(df, img_dir, self.account[:-4], user_action, total_tweets)
            self.extract_tweet(df, csv_dir, self.account[:-4], user_action, mean)


    def histgram(self, df, save_dir, name, user_action, total_tweets):
        mean = int(df[user_action].mean())
        std = int(df[user_action].std())
        _max = int(df[user_action].max())
        _min = int(df[user_action].min())

        # draw 'like' histgram
        hist = df[data_type].hist(bins=int(df[user_action].mean()), range=(0, mean+std))

        # drawing setting
        stat = ["Mean: {}".format(mean), "Std: {}".format(std),
                "Max: {}".format(_max), "Min: {}".format(_min)]
        plt.vlines(mean, ymin=0, ymax=150, colors='red', linestyles="dashed", label=stat[0])
        plt.text(mean+std/2, 140, stat[0], color='red')
        plt.text(mean+std/2, 130, stat[1])
        plt.text(mean+std/2, 120, stat[2])
        plt.text(mean+std/2, 110, stat[3])
        plt.title("Histgram of '{}' in {}'s {} tweets".format(user_action, name, total_tweets))
        plt.xlabel(user_action)
        plt.ylabel("frequency")

        # save
        fig = hist.get_figure()
        name = "hist_{}_{}.jpg".format(name, data_type)
        fig.savefig(os.path.join(save_dir, name))
        plt.close()

        return(mean)

    def extract_tweet(self, df, save_dir, account, user_action, criteria, criteria_type="mean"):
        extracted = df.query("{}>{}".format(user_action, criteria))
        fname = "{}_over_{}_{}.csv".format(account, criteria_type, data_type)
        extracted.to_csv(os.path.join(save_dir, fname), 
                        encoding='shift_jis', index=False)


if __name__=="__main__":
    dc = DatasetCreater('./csv/@nikkei.csv')
    # dc.analyze()
    dc.create()
