# Türkiye Yatırım Fonu Simülasyonu

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

5.668.734 yatırımcının yatırım fonu tutarlarını simüle eden ve görselleştiren kapsamlı bir veri analizi projesidir.

![Dashboard Preview](investment_distribution.png)

## Proje Hakkında

Bu proje, Türkiye'deki yatırım fonu yatırımcılarının portföy dağılımını simüle eder ve analiz eder. Gerçek istatistiklere dayanan lognormal dağılım modeli kullanılarak, 5.6 milyondan fazla yatırımcı için sentetik veri üretilmiştir.

### Temel Veriler

| Metrik | Değer |
|--------|-------|
| **Toplam Yatırımcı** | 5.668.734 |
| **Yurt İçi Yatırımcı** | 5.617.861 (%99.1) |
| **Yurt Dışı Yatırımcı** | 50.873 (%0.9) |
| **Toplam Fon Değeri** | 8.19 Trilyon TL |
| **Ortalama Yatırım** | 1.451.742 TL |
| **Medyan Yatırım** | 647.488 TL |

### Fon Türleri Dağılımı

| Fon Türü | Değer (Milyon TL) | Oran |
|----------|-------------------|------|
| Hisse Senedi Şemsiye Fonu | 169.351 | %2.1 |
| Para Piyasası Şemsiye Fonu | 1.458.481 | %17.8 |
| Diğer Fonlar | 6.566.031 | %80.1 |

## Kurulum

### Gereksinimler

```bash
pip install numpy pandas matplotlib scipy
```

### Çalıştırma

```bash
python investment_fund_simulation.py
```

## Proje Yapısı

```
fund_data_simulation/
├── investment_fund_simulation.py   # Ana simülasyon scripti
├── dashboard.html                  # İnteraktif web dashboard
├── investment_distribution.png     # Dağılım grafikleri
├── investor_data.csv              # Simülasyon çıktısı (5.6M satır)
├── summary_statistics.csv         # Özet istatistikler
└── README.md                      # Bu dosya
```

## Özellikler

### Veri Simülasyonu
- **Lognormal Dağılım**: Gelir ve servet dağılımını modellemek için ideal dağılım
- **Yurt İçi/Dışı Ayrımı**: Farklı ortalama ve varyans değerleri
- **Tekrarlanabilir Sonuçlar**: Random seed ile tutarlı veri üretimi

### İstatistiksel Analiz
- Temel istatistikler (ortalama, medyan, std, varyans)
- Yüzdelik dilim analizi
- Yatırımcı tipi karşılaştırması

### Görselleştirme
6 farklı grafik içeren kapsamlı analiz:
1. **Histogram** - Logaritmik yatırım dağılımı
2. **Box Plot** - Yatırımcı tipi karşılaştırması
3. **Pasta Grafiği** - Yatırımcı sayısı dağılımı
4. **Fon Türleri** - Piyasa değeri dağılımı
5. **CDF** - Kümülatif dağılım fonksiyonu
6. **KDE** - Yoğunluk karşılaştırması

### İnteraktif Dashboard
- Modern, responsive tasarım
- Tab-based navigasyon
- Arama ve filtreleme
- Veri indirme özelliği

## Örnek Çıktılar

### Yüzdelik Dilimler

| Yüzdelik | Yatırım Miktarı |
|----------|-----------------|
| %10 | 127.146 TL |
| %25 | 274.837 TL |
| %50 (Medyan) | 647.488 TL |
| %75 | 1.525.204 TL |
| %90 | 3.300.162 TL |
| %99 | 12.452.799 TL |

## Metodoloji

Projede **lognormal dağılım** kullanılmıştır:

```python
# Lognormal parametreleri
σ = √(ln(1 + variance/mean²))
μ = ln(mean) - σ²/2

# Veri üretimi
investments = np.random.lognormal(mean=μ, sigma=σ, size=n_investors)
```

Bu dağılım şu nedenlerle tercih edilmiştir:
- Yalnızca pozitif değerler üretir
- Sağa çarpık dağılım (gerçek servet dağılımını yansıtır)
- Az sayıda çok zengin, çok sayıda orta/düşük gelirli yatırımcı

## Lisans

Bu proje MIT lisansı altında sunulmaktadır.

## Geliştirici

**Emirhan Yavuz**

---

<p align="center">
  <sub>📊 Data Mining Project | 2026</sub>
</p>
