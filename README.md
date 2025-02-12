# Türkçe Duygu Analizi (Turkish Sentiment Analysis)

Bu proje, Türkçe metinler üzerinde duygu analizi yapan bir web uygulamasıdır.

## Özellikler

- Metin tabanlı duygu analizi (Pozitif/Negatif)
- Örnek metinlerle test imkanı
- Analiz sonuçlarının görselleştirilmesi
- Geçmiş analizlerin veritabanında saklanması
- Kullanıcı dostu arayüz

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. PostgreSQL veritabanı bağlantısı için çevre değişkenlerini ayarlayın:
- DATABASE_URL
- PGHOST
- PGPORT
- PGUSER
- PGPASSWORD
- PGDATABASE

3. Uygulamayı çalıştırın:
```bash
streamlit run main.py
```

## Kullanım

1. Web arayüzünde metin giriş alanına analiz edilecek metni yazın veya örnek metinlerden birini seçin
2. "Analiz Et" butonuna tıklayın
3. Sonuçları görsel grafikler ve yüzde değerleriyle görüntüleyin
4. Geçmiş analizleri yan menüden takip edin

## Teknik Detaylar

- Frontend: Streamlit
- Backend: Python
- ML Model: Scikit-learn (LogisticRegression)
- Veritabanı: PostgreSQL
- ORM: SQLAlchemy
