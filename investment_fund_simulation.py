"""
Türkiye Yatırım Fonu Yatırımcı Simülasyonu
==========================================
Bu script, Türkiye'deki yatırım fonu yatırımcılarının
ne kadar fon tuttuğunu simüle eder ve görselleştirir.

Veriler:
- Yurt İçi Yatırımcı: 5.617.861
- Yurt Dışı Yatırımcı: 50.873
- Toplam: 5.668.734

Fon Türleri (Milyon TL):
- Hisse Senedi Şemsiye Fonu: 169.351
- Para Piyasası Şemsiye Fonu: 1.458.481
- Diğer Fonlar: 6.566.031
- Toplam: 8.193.863
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği için
plt.rcParams['font.family'] = 'DejaVu Sans'

# =============================================================================
# PARAMETRELER
# =============================================================================

# Yatırımcı sayıları
YURT_ICI_YATIRIMCI = 5_617_861
YURT_DISI_YATIRIMCI = 50_873
TOPLAM_YATIRIMCI = 5_668_734

# Fon değerleri (Milyon TL -> TL'ye çevir)
HISSE_SENEDI_FONU = 169_351 * 1_000_000  # TL
PARA_PIYASASI_FONU = 1_458_481 * 1_000_000  # TL
DIGER_FONLAR = 6_566_031 * 1_000_000  # TL
TOPLAM_FON = 8_193_863 * 1_000_000  # TL

# Ortalama yatırım miktarı (TL / yatırımcı)
ORTALAMA_YATIRIM = TOPLAM_FON / TOPLAM_YATIRIMCI

print("=" * 60)
print("TÜRKIYE YATIRIM FONU SİMÜLASYONU")
print("=" * 60)
print(f"\nToplam Yatırımcı Sayısı: {TOPLAM_YATIRIMCI:,}")
print(f"Toplam Fon Değeri: {TOPLAM_FON:,.0f} TL")
print(f"Ortalama Yatırım: {ORTALAMA_YATIRIM:,.2f} TL")

# =============================================================================
# VERİ ÜRETİMİ
# =============================================================================

def generate_investor_data(n_investors, mean, variance, investor_type, seed=42):
    """
    Lognormal dağılım kullanarak yatırımcı verisi üretir.
    Lognormal dağılım, gelir ve servet dağılımını modellemek için idealdir
    çünkü pozitif değerler üretir ve sağa çarpık bir dağılım gösterir.
    
    Parameters:
    -----------
    n_investors : int
        Yatırımcı sayısı
    mean : float
        Ortalama yatırım miktarı (TL)
    variance : float
        Varyans
    investor_type : str
        Yatırımcı tipi ('Yurt İçi' veya 'Yurt Dışı')
    seed : int
        Random seed
    
    Returns:
    --------
    pd.DataFrame
        Yatırımcı verileri
    """
    np.random.seed(seed)
    
    # Lognormal dağılım parametreleri
    # mean = exp(mu + sigma^2/2)
    # variance = (exp(sigma^2) - 1) * exp(2*mu + sigma^2)
    sigma = np.sqrt(np.log(1 + variance / mean**2))
    mu = np.log(mean) - sigma**2 / 2
    
    # Veri üretimi
    investments = np.random.lognormal(mean=mu, sigma=sigma, size=n_investors)
    
    # DataFrame oluştur
    df = pd.DataFrame({
        'yatirimci_id': range(1, n_investors + 1),
        'yatirimci_tipi': investor_type,
        'yatirim_miktari_tl': investments
    })
    
    return df

print("\n📊 Veri üretimi başlıyor...")

# Yurt içi yatırımcılar için varyans (YÜKSEK VARYANSLAG gerçekçi eşitsizlik)
# Gerçek dünyada servet dağılımı çok daha eşitsiz - Pareto prensibi (%20 nüfus, %80 servet)
variance_yurt_ici = (ORTALAMA_YATIRIM * 5) ** 2  # x2 -> x5 (çok daha geniş dağılım)

# Yurt dışı yatırımcılar için varyans (daha yüksek ortalama ve EKSTREM varyans)
mean_yurt_disi = ORTALAMA_YATIRIM * 2.0  # x1.5 -> x2 (yurt dışı yatırımcılar daha zengin)
variance_yurt_disi = (mean_yurt_disi * 6) ** 2  # x2.5 -> x6 (çok daha büyük uçurum)

# Yurt içi yatırımcı verisi
print(f"  → Yurt içi yatırımcı verisi üretiliyor ({YURT_ICI_YATIRIMCI:,} kişi)...")
df_yurt_ici = generate_investor_data(
    YURT_ICI_YATIRIMCI, 
    ORTALAMA_YATIRIM, 
    variance_yurt_ici,
    'Yurt İçi',
    seed=42
)

# Yurt dışı yatırımcı verisi
print(f"  → Yurt dışı yatırımcı verisi üretiliyor ({YURT_DISI_YATIRIMCI:,} kişi)...")
df_yurt_disi = generate_investor_data(
    YURT_DISI_YATIRIMCI, 
    mean_yurt_disi, 
    variance_yurt_disi,
    'Yurt Dışı',
    seed=43
)

# Tüm verileri birleştir
print("  → Veriler birleştiriliyor...")
df = pd.concat([df_yurt_ici, df_yurt_disi], ignore_index=True)
df['yatirimci_id'] = range(1, len(df) + 1)

print(f"\n✅ Toplam {len(df):,} yatırımcı verisi oluşturuldu!")

# =============================================================================
# İSTATİSTİKLER
# =============================================================================

print("\n" + "=" * 60)
print("İSTATİSTİKSEL ANALİZ")
print("=" * 60)

# Genel istatistikler
print("\n📈 GENEL İSTATİSTİKLER:")
print(f"  Ortalama (Mean): {df['yatirim_miktari_tl'].mean():,.2f} TL")
print(f"  Medyan: {df['yatirim_miktari_tl'].median():,.2f} TL")
print(f"  Standart Sapma: {df['yatirim_miktari_tl'].std():,.2f} TL")
print(f"  Varyans: {df['yatirim_miktari_tl'].var():,.2f} TL²")
print(f"  Minimum: {df['yatirim_miktari_tl'].min():,.2f} TL")
print(f"  Maximum: {df['yatirim_miktari_tl'].max():,.2f} TL")
print(f"  Toplam Fon: {df['yatirim_miktari_tl'].sum():,.0f} TL")

# Yatırımcı tipine göre istatistikler
print("\n📊 YATIRIMCI TİPİNE GÖRE İSTATİSTİKLER:")
for tip in ['Yurt İçi', 'Yurt Dışı']:
    subset = df[df['yatirimci_tipi'] == tip]
    print(f"\n  {tip}:")
    print(f"    Sayı: {len(subset):,}")
    print(f"    Ortalama: {subset['yatirim_miktari_tl'].mean():,.2f} TL")
    print(f"    Medyan: {subset['yatirim_miktari_tl'].median():,.2f} TL")
    print(f"    Standart Sapma: {subset['yatirim_miktari_tl'].std():,.2f} TL")
    print(f"    Varyans: {subset['yatirim_miktari_tl'].var():,.2f} TL²")

# Yüzdelik dilimler
print("\n📉 YÜZDELİK DİLİMLER:")
percentiles = [10, 25, 50, 75, 90, 95, 99]
for p in percentiles:
    value = np.percentile(df['yatirim_miktari_tl'], p)
    print(f"  {p}. yüzdelik: {value:,.2f} TL")

# =============================================================================
# GÖRSELLEŞTİRME
# =============================================================================

print("\n" + "=" * 60)
print("GÖRSELLEŞTİRME")
print("=" * 60)
print("\n🎨 Grafikler oluşturuluyor...")

# Renk paleti
colors = {
    'primary': '#1a5276',
    'secondary': '#2ecc71',
    'accent': '#e74c3c',
    'yurt_ici': '#3498db',
    'yurt_disi': '#e67e22',
    'background': '#ecf0f1'
}

# Figure oluştur
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Türkiye Yatırım Fonu Yatırımcı Dağılımı Analizi\n5.668.734 Yatırımcı', 
             fontsize=14, fontweight='bold', y=0.98)

# 1. Histogram - Genel Dağılım
ax1 = fig.add_subplot(2, 3, 1)
# Log ölçeği için veri hazırlığı
data_log = np.log10(df['yatirim_miktari_tl'] + 1)
ax1.hist(data_log, bins=100, color=colors['primary'], alpha=0.7, edgecolor='white', linewidth=0.5)
ax1.set_xlabel('Yatırım Miktarı (log₁₀ TL)', fontsize=8)
ax1.set_ylabel('Yatırımcı Sayısı', fontsize=8)
ax1.set_title('Yatırım Miktarı Dağılımı (Logaritmik)', fontsize=10, fontweight='bold')
ax1.axvline(np.log10(df['yatirim_miktari_tl'].mean()), color=colors['accent'], 
            linestyle='--', linewidth=2, label=f"Ortalama: {df['yatirim_miktari_tl'].mean():,.0f} TL")
ax1.axvline(np.log10(df['yatirim_miktari_tl'].median()), color=colors['secondary'], 
            linestyle='--', linewidth=2, label=f"Medyan: {df['yatirim_miktari_tl'].median():,.0f} TL")
ax1.legend(fontsize=7)
ax1.grid(True, alpha=0.3)

# 2. Yatırımcı Tipi Karşılaştırması - Box Plot
ax2 = fig.add_subplot(2, 3, 2)
box_data = [df[df['yatirimci_tipi'] == 'Yurt İçi']['yatirim_miktari_tl'].values,
            df[df['yatirimci_tipi'] == 'Yurt Dışı']['yatirim_miktari_tl'].values]
bp = ax2.boxplot(box_data, labels=['Yurt İçi', 'Yurt Dışı'], patch_artist=True, showfliers=False)
bp['boxes'][0].set_facecolor(colors['yurt_ici'])
bp['boxes'][1].set_facecolor(colors['yurt_disi'])
ax2.set_ylabel('Yatırım Miktarı (TL)', fontsize=8)
ax2.set_title('Yatırımcı Tipine Göre Dağılım\n(Box Plot)', fontsize=10, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.ticklabel_format(style='scientific', axis='y', scilimits=(6,6))

# 3. Pasta Grafiği - Yatırımcı Sayısı
ax3 = fig.add_subplot(2, 3, 3)
sizes = [YURT_ICI_YATIRIMCI, YURT_DISI_YATIRIMCI]
labels_legend = [f'Yurt İçi: {YURT_ICI_YATIRIMCI:,} (%{100*YURT_ICI_YATIRIMCI/TOPLAM_YATIRIMCI:.1f})',
                 f'Yurt Dışı: {YURT_DISI_YATIRIMCI:,} (%{100*YURT_DISI_YATIRIMCI/TOPLAM_YATIRIMCI:.1f})']
explode = (0, 0.05)
wedges3, texts3 = ax3.pie(sizes, explode=explode, colors=[colors['yurt_ici'], colors['yurt_disi']],
                           startangle=90, shadow=False)
ax3.legend(wedges3, labels_legend, loc='lower center', fontsize=6, bbox_to_anchor=(0.5, -0.15))
ax3.set_title('Yatırımcı Sayısı Dağılımı', fontsize=10, fontweight='bold')

# 4. Fon Türleri Pasta Grafiği
ax4 = fig.add_subplot(2, 3, 4)
fon_sizes = [169_351, 1_458_481, 6_566_031]
fon_labels_legend = ['Hisse Senedi Şemsiye Fonu: 169.351 M TL (%2.1)',
                     'Para Piyasası Şemsiye Fonu: 1.458.481 M TL (%17.8)',
                     'Diğer Fonlar: 6.566.031 M TL (%80.1)']
fon_colors = ['#27ae60', '#3498db', '#9b59b6']
explode_fon = (0.05, 0.02, 0)
wedges4, texts4 = ax4.pie(fon_sizes, explode=explode_fon, colors=fon_colors,
                           startangle=45, shadow=False)
ax4.legend(wedges4, fon_labels_legend, loc='lower center', fontsize=5, bbox_to_anchor=(0.5, -0.2))
ax4.set_title('Fon Türlerine Göre Piyasa Değeri\n(Milyon TL)', fontsize=10, fontweight='bold')

# 5. Kümülatif Dağılım
ax5 = fig.add_subplot(2, 3, 5)
sorted_investments = np.sort(df['yatirim_miktari_tl'])
cumulative = np.arange(1, len(sorted_investments) + 1) / len(sorted_investments) * 100
# Her 1000 veri noktasından birini al (performans için)
step = 1000
ax5.plot(sorted_investments[::step], cumulative[::step], color=colors['primary'], linewidth=2)
ax5.set_xlabel('Yatırım Miktarı (TL)', fontsize=8)
ax5.set_ylabel('Kümülatif Yüzde (%)', fontsize=8)
ax5.set_title('Kümülatif Dağılım (CDF)', fontsize=10, fontweight='bold')
ax5.set_xscale('log')
ax5.grid(True, alpha=0.3)
# Önemli yüzdelikleri işaretle
for p in [50, 90, 99]:
    value = np.percentile(df['yatirim_miktari_tl'], p)
    ax5.axhline(y=p, color=colors['accent'], linestyle=':', alpha=0.5)
    ax5.axvline(x=value, color=colors['accent'], linestyle=':', alpha=0.5)
    ax5.scatter([value], [p], color=colors['accent'], s=50, zorder=5)
    ax5.annotate(f'{p}%: {value:,.0f} TL', xy=(value, p), 
                 xytext=(value*2, p-5), fontsize=7)

# 6. Yatırımcı Tipi Karşılaştırması - KDE
ax6 = fig.add_subplot(2, 3, 6)
# KDE hesapla
data_yurt_ici = np.log10(df[df['yatirimci_tipi'] == 'Yurt İçi']['yatirim_miktari_tl'] + 1)
data_yurt_disi = np.log10(df[df['yatirimci_tipi'] == 'Yurt Dışı']['yatirim_miktari_tl'] + 1)

ax6.hist(data_yurt_ici, bins=100, density=True, alpha=0.5, 
         color=colors['yurt_ici'], label='Yurt İçi', edgecolor='white', linewidth=0.5)
ax6.hist(data_yurt_disi, bins=50, density=True, alpha=0.5, 
         color=colors['yurt_disi'], label='Yurt Dışı', edgecolor='white', linewidth=0.5)

ax6.set_xlabel('Yatırım Miktarı (log₁₀ TL)', fontsize=8)
ax6.set_ylabel('Yoğunluk', fontsize=8)
ax6.set_title('Yatırımcı Tipine Göre\nYatırım Dağılımı Karşılaştırması', fontsize=10, fontweight='bold')
ax6.legend(fontsize=7)
ax6.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Grafikleri kaydet
output_path = '/Users/emirhanyavuz/data_mining_one_million_data_project/investment_distribution.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"\n✅ Grafikler kaydedildi: {output_path}")

plt.show()

# =============================================================================
# VERİ ÇIKTISI
# =============================================================================

print("\n" + "=" * 60)
print("VERİ ÖRNEĞİ (İLK 10 SATIR)")
print("=" * 60)
print(df.head(10).to_string(index=False))

# CSV'ye kaydet (tüm veri)
csv_path = '/Users/emirhanyavuz/data_mining_one_million_data_project/investor_data.csv'
df.to_csv(csv_path, index=False)
print(f"\n📁 Tüm veri ({len(df):,} satır) kaydedildi: {csv_path}")

# Özet istatistikleri CSV'ye kaydet
summary_stats = pd.DataFrame({
    'Metrik': ['Toplam Yatırımcı', 'Yurt İçi Yatırımcı', 'Yurt Dışı Yatırımcı',
               'Ortalama Yatırım (TL)', 'Medyan Yatırım (TL)', 'Standart Sapma (TL)',
               'Varyans (TL²)', 'Minimum (TL)', 'Maximum (TL)', 'Toplam Fon (TL)'],
    'Değer': [f'{TOPLAM_YATIRIMCI:,}', f'{YURT_ICI_YATIRIMCI:,}', f'{YURT_DISI_YATIRIMCI:,}',
              f'{df["yatirim_miktari_tl"].mean():,.2f}',
              f'{df["yatirim_miktari_tl"].median():,.2f}',
              f'{df["yatirim_miktari_tl"].std():,.2f}',
              f'{df["yatirim_miktari_tl"].var():,.2f}',
              f'{df["yatirim_miktari_tl"].min():,.2f}',
              f'{df["yatirim_miktari_tl"].max():,.2f}',
              f'{df["yatirim_miktari_tl"].sum():,.0f}']
})
summary_path = '/Users/emirhanyavuz/data_mining_one_million_data_project/summary_statistics.csv'
summary_stats.to_csv(summary_path, index=False)
print(f"📁 Özet istatistikler kaydedildi: {summary_path}")

print("\n" + "=" * 60)
print("İŞLEM TAMAMLANDI!")
print("=" * 60)
