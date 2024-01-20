import cv2
import pickle #park alanlarının kordinatlarını buna kaydettirrecem

width, height = 107, 48

try:
    with open('AracParkPozisyonu', 'rb') as f: #APR dosyasını rb ikili okuma modunda açar ve bu dosyayı 'f'adlı dosya nesnesine atar
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))  #sol tıklamada poslistesine ekliyor
    if events == cv2.EVENT_RBUTTONDOWN:     #ekledikten sonra sağ tık yaptığımızda
        for i, pos in enumerate(posList):   #postlistin içinde dolaşıyor
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height: # dikdörtgen var mı yokmu kontrol ediyor
                posList.pop(i) #eğer dikdörtgen bulursa çıkartıyor

    with open('AracParkPozisyonu', 'wb') as f: #Sonuç neticesinde alınan veriler WB modunda
        pickle.dump(posList, f) #pickle.dump veri yazma yöntemi ile elde edilen veriyi AraçParkPozisyou dosyasına F dosya nesnesine yazar


while True:     #Sürekli Döngü
    img = cv2.imread('carParkImg.png')  #Resim okuma fonksiyonu=imread
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Resim", img)  #resmi görmek için fonksiyon
    cv2.setMouseCallback("Resim", mouseClick)  #farede tıklandığında resmi geri çağırıyor
    cv2.waitKey(1)  #programı 1 milisaniye durdurur ve bir tuşa basılmasını bekler. Bu sayede programı güncel tutar