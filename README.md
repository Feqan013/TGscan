# TGscan
Telegram CTI Tool
2 funksiyaya sahibdir:
1) Infostealer Data Collector
2) Keyword Search - Alert

# Manifest

```bash
  TGscan.py ---- Əsas kod
  TGjsoncreator.py ---- müxtəlif formatlarda olan kombolist sətirlərini(URL:Username:Password) emal edir və json-a dönüşdürür.
  TGSearch.py ---- toplanan hesablar arasında axtarış etmək üçün
  tgleaks.json ---- Bütün hesablar(240.000+) json formatlnda
  tgleaks.txt ---- Bütün hesablar ilkin kombolist formatında
  tgleaks_jun 12.txt ---- Göstərilən tarixdə paylaşılan hesablar
  tgleaks_jun 12.json ---- Göstərilən tarixdə paylaşılan hesablar json formatında
  tgleaks_jun 12_new.txt ---- Göstərilən tarixdə paylaşılan yeni hesablar(tgleaks.json-da olmayan)
  telegram_local_storage.json ---- Axtarış üçün istifadə edilən Telegram hesabının cookie-ləri(şifrəsiz login üçün)
  tgzip_passwords.txt ---- Zip və Rarları extract etmək üçün şifrə siyahısı
```
# 1)Infostealer Data Collector
Telegram Log hesablarında paylaşılan .txt, .zip, .rar formatlı log fayllarını yükləyir, unzip edir, göstərilən domainə(.az) görə hesabları toplayır, uyğun formata salır və diskdə saxlayır.

Windows,pycharm və python 3.12 ilə test edilib.
İstifadəsi üçün chromedriver(https://googlechromelabs.github.io/chrome-for-testing/) 7-zip(https://www.7-zip.org/download.html) və 400 GB+ yer tələb olunur. İki formatda işlədilə bilər:
```bash
python.exe TGscan.py "jun 10" ---- Göstərilən tarixdə paylaşılan hesablar üçün
python.exe TGscan.py ---- Dünənki tarixdə paylaşılan hesablar üçün(Task Scheduler-ə əlavə edilməsi üçün)
```
İşləməsi üçün kodun ilk sətirlərində olan path-lar editlənməlidir. Tarix və fayl adı avtomatik olar hesaba əlavə edilir. Proses bitdikdən sonra yüklənmiş bütün fayllar silinir.
![Diagram1](https://github.com/Feqan013/TGscan/assets/63374185/10bbf34f-6fd6-4d33-a409-cc4b2db0139f)

Yüklənmə prosesi:


https://github.com/Feqan013/TGscan/assets/63374185/45986bf4-3e4a-4d1f-a5cd-48b67f8c870b
# 2)Keyword Search
APT və Hacker qruplarında hədəf keywordlərlə bağlı yeni mesaj paylaşıldığı zaman telegram üzərindən mesaj göndərərək məlumatlandırır. DDOS hücumları və data breachlər haqqında tez məlumat almaq üçün istifadə edilir. Standart olaraq 5 dəqiqə intervalla axtarış edir. 7/24 işləməsi üçün nəzərdə tutlub.
İstifadə etmək üçün -k flagindən istifadə edilir:
```bash
python.exe TGscan.py -k ".az" "Azerbaijani" "test.az" ---- Göstərilən keywordlərlə bağlı hər-hansısa yeni mesaj paylaşılarsa istifadəçi məlumatlandırılacaq.
```
Axtarış prosesi:
![image](https://github.com/Feqan013/TGscan/assets/63374185/1e7690f1-0ac2-443b-899d-192ce32664d3)
Mesaj aşkar edildikdə botun göndərdiyi xəbərdarlıq(mesaj kontenti və ekran görüntüsü)
![image](https://github.com/Feqan013/TGscan/assets/63374185/c6d1e842-0879-4ab6-b373-a2a2286c4194)



