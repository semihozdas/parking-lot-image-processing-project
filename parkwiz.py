import cv2
import pickle  #park alanlarının kordinatlarını bu kaydedecek
import cvzone
import numpy as np  #hewsaplama için kullandım

video = cv2.VideoCapture('carPark.mp4') #Video Tanımladım

with open('AracParkPozisyonu', 'rb') as f:  #ikili modda 'AracParkPozisyonu' dosyasını f ndosya nesnesine veriyi yükledim liste de tuttum
    posList = pickle.load(f)

width, height = 107, 48


#bu blokta park alanının dolu olup olmadığını anlayacağız
def ParkAlaniKontrolu(imgPro): #park alanlarını kontrol etmek için fonksiyon tanımlar
    spaceCounter = 0 #Boş park alanlarını saymai için boş sayaç başlatır

    for x, y in posList:  #park alanımızın kordinatları için döngü
        imgCrop = imgPro[y:y + height, x:x + width]   #görüntüden pkarkın alanını alıyor
        count = cv2.countNonZero(imgCrop) # Kırpılan görüntüdeki alanın piksellerin sayısı sayılır.
        print(count)
        color = (0, 255, 0) if count < 900 else (0, 0, 255)
        thickness = 4 if count < 900 else 2

        cv2.rectangle(img, (x, y), (x + width, y + height), color, thickness) #Belirlenen boyutta ve kalınlıkta dikdörtgen çiziyor
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color) #Park alanı piksel ölçer

        spaceCounter += 1 if count < 900 else 0 #Park Alanı boşsa, boş alan sayacını 1 artırır

    cvzone.putTextRect(img, f'Bos Alan: {spaceCounter}/{len(posList)}', (20, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 0, 0))  #Görüntü üzerine, boş alan sayısını ve toplam park alanı sayısını gösteren metin

    cv2.putText(img, "Semih Ozdas", (865, 710), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)


while True:
    success, img = video.read()     #video kaynağını okur
    if not success:                 #okuma başarısız ise döngüden çıkar
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     #Görüntüyü gri tonlamaya dönüştürür.
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)  #Gauss bulanıklaştırma uygulayarak gürültüyü azaltır.

    #UYGULANABİLİR EŞİKLEME İLE NETLİĞİ ARTIRDUM
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)       #Medyan filtreleme ile kalan gürültüyü daha da azaltır.
    kernel = np.ones((3, 3), np.uint8)                #3x3'lük bir genişletme çekirdeği oluşturur.
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1) #Nesnelerin kenarlarını genişletir, daha belirgin hale getirir.

    ParkAlaniKontrolu(imgDilate)  #Daha önce tanımlanmış ParkAlaniKontrolu fonksiyonunu kullanarak park alanlarını kontrol eder ve görüntüyü işaretler.

    cv2.imshow("Python Kutuphaneleri Final Sinavi - Semih Ozdas", img)
    cv2.waitKey(10)
