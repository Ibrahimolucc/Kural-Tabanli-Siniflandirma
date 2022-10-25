# Veri Hazırlama
# persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import numpy as np
import pandas as pd
import seaborn as sns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
df = pd.read_csv("persona.csv")
df.head(5)
df.tail(5)
df.shape
df.info()
df.isnull().sum()
df.describe().T

# Kaç unique SOURCE vardır? &  Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Kaç unique PRICE vardır?
df["PRICE"].nunique()

# Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

# Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE": "sum"})
#  SOURCE türlerine göre göre satış sayıları nedir?
df["SOURCE"].value_counts()

# Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": "mean"})

#  SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"})

# COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

#############################################
# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})

#############################################
#  Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız. &  Çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE","SEX","AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE",ascending=False)
agg_df.head(5)

#############################################
# Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
agg_df.reset_index(inplace=True)

#############################################
# AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]
agg_df["AGE_CAT"]=pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()

#############################################
#  Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
agg_df = agg_df.reset_index()
agg_df["customers_level_based"] = agg_df[["COUNTRY", "SOURCE", "SEX", "AGE_CAT"]].agg("_".join, axis=1)
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.index = agg_df.index.str.upper()
agg_df.head(5)
#############################################
# Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################
agg_df = agg_df.reset_index()
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels = ["D", "C", "B", "A"])
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})
agg_df.loc[agg_df["SEGMENT"] == "A"]

#############################################
#  Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_df = agg_df.copy()
new_df.reset_index(inplace=True)
new_df.head(10)
new_user4 = "TUR_ANDROID_MALE_19_23"
new_df[new_df["customers_level_based"] == new_user4].agg({"PRICE": "mean"})

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
new_user3 = "BRA_IOS_FEMALE_31_40"
new_df[new_df["customers_level_based"] == new_user3].agg({"PRICE": "mean"})