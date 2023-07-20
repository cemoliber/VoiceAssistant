import random
import time

import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import pyaudio
import os
from selenium import webdriver

import requests
from bs4 import BeautifulSoup

mesaj = "Üzgünüm internet kaynaklı bir hata oluştu.Lütfen internetinizi kontrol ediniz"

r = sr.Recognizer()

class SesliAsistan():
    def seslendirme(self, metin):
        xtts = gTTS(text=metin, lang="tr-TR")
        dosya = "dosya" + str(random.randint(0,3246513216)) + ".mp3"
        xtts.save(dosya)
        playsound(dosya)
        os.remove(dosya)

    def ses_kayit(self):
        with sr.Microphone() as kaynak:
            print("Sizi dinliyorum..")
            listen = r.listen(kaynak)
            voice = " "

            try:
                voice = r.recognize_google(listen, language="tr-TR")
            except sr.UnknownValueError:
                self.seslendirme("Ne söylemek istediğiniz anlayamadım.Lütfen tekrar edin")
            return voice

    def ses_karsilik(self, gelen_ses):
        if "selam" in gelen_ses:
            self.seslendirme("Size de selamlar")
        elif "Merhaba" in gelen_ses:
            self.seslendirme("Size de merhaba")
        elif "Merhaba" in gelen_ses:
            self.seslendirme("İyiyim siz nasılsınız")
        elif "Nasıl gidiyor" in gelen_ses:
            self.seslendirme("İyi gidiyor.Sizin nasıl gidiyor?")
        elif "Nasılsın" in gelen_ses or "Nasılsın palvin" in gelen_ses:
            self.seslendirme("İyiyim teşekkür ederim.Siz nasılsınız?")
        elif "video aç" in gelen_ses or "müzik aç" in gelen_ses or "youtube aç" in gelen_ses:
            try:
                self.seslendirme("Ne açmamı istersiniz")
                veri = self.ses_kayit()
                self.seslendirme("{} açılıyor..".format(veri))
                time.sleep(1)
                url = "https://www.youtube.com/results?search_query={}".format(veri)
                tarayici = webdriver.Chrome()
                tarayici.get(url)
            except:
                self.seslendirme(mesaj)

        elif "google aç" in gelen_ses or "arama yap" in gelen_ses:
            try:
                self.seslendirme("Ne araştırmamı istersiniz?")
                veri = self.ses_kayit()
                self.seslendirme("{} için bulduklarım bunlar".format(veri))
                url = "hhtps://www.google.com/search?q={}"
                tarayci = webdriver.Chrome()
                tarayci.get(url)
            except:
                self.seslendirme(mesaj)

        elif "film aç" in gelen_ses:
            try:
                self.seslendirme("Hangi filmi açmamı istersiniz?")
                veri = self.ses_kayit()
                self.seslendirme("{} filmini açıyorum..".format(veri))
                url = "https://www.google.com/search?q={}+izle".format(veri)
                tarayici = webdriver.Chrome()
                tarayici.get(url)
            except:
                self.seslendirme(mesaj)

        elif "film önerisi yapar mısın?" in gelen_ses or "film izlemek istiyorum" in gelen_ses:
            self.seslendirme("Ne tür film izlemek istersiniz?")
            veri = self.ses_kayit()
            self.seslendirme("{} için bulduklarım bunlar".format(veri))
            url = "https://www.filmmodu13.com/film-ara?term={}".format(veri)
            tarayici = webdriver.Chrome()
            tarayici.get(url)

        elif "hava durumu tahmini" in gelen_ses or "bugün hava kaç derece" in gelen_ses or "hava durumu" in gelen_ses:
            try:
                self.seslendirme("Hangi şehrin hava durumunu istersiniz?")
                sehir = self.ses_kayit()
                url = "https://www.ntv.com.tr/{}-hava-durumu".format(sehir)
                request = requests.get(url)
                html_icerigi = request.content
                soup = BeautifulSoup(html_icerigi, "html.parser")

                gunduz_sicakliklari = soup.find_all("p", {"class": "hava-durumu--detail-data-item-bottom-temp-max"})
                gece_sicakliklari = soup.find_all("p", {"class": "hava-durumu--detail-data-item-bottom-temp-min"})
                hava_durumu = soup.find_all("div", {"class": "container hava-durumu--detail-data-item-bottom-desc"})

                gunduz = []
                gece = []
                hava = []

                for x in gunduz_sicakliklari:
                    x = x.text
                    gunduz.append(x)
                for y in gece_sicakliklari:
                    y = y.text
                    gece.append(y)
                for z in hava_durumu:
                    z = z.text
                    hava.append(z)

                sonuc = "{} için yarınki hava raporları şöyle {} gündüz sıcaklığı {} gece sıcaklığı ise {} derecedir".format(sehir,hava[0],gunduz[0],gece[0])

                self.seslendirme(sonuc)
            except:
                self.seslendirme("Üzgünüm istediğiniz sonuçları getirirken bir hata oluştu.")

asistan = SesliAsistan()

def uyanma_fonk(metin):
    if(metin == "hey palvin" or metin =="palvin"):
        asistan.seslendirme("Sizi diliyorum..")
        cevap = asistan.ses_kayit()
        if(cevap != " "):
            asistan.ses_karsilik(cevap)


while True:
    ses = asistan.ses_kayit()
    if (ses != " "):
        ses = ses.lower()
        print(ses)
        uyanma_fonk(ses)
