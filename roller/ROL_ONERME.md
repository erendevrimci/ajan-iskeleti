> **DURUM: CANLI** · rol önerme yöntemi · ana ajan kurulumda ve her tur kapanışında uygular

# Rol önerme yöntemi

Rol, uzun ömürlü ayrı bir Claude Code oturumudur. Kendi klasörü, kartı, seyir defteri ve kilidi vardır; ana ajana her gün onay ve birleşme yükü getirir. Bu yüzden rol sezgiyle değil kanıtla önerilir. Kanıt, komut çıktısıdır.

## 1. Ölç

```bash
python3 ISKELET/araclar/iskelet.py alanlar --proje . --gun 120     # birlikte değişen yol kümeleri
git log --since="120 days ago" --format='%an' | sort | uniq -c       # kim yazıyor
ls; ls docs 2>/dev/null                                              # belge akışları
```

Kullanıcıya ya da belgelere şunları sor:
- **Dış kanallar:** sürekli yazışılan sohbet kanalı, e-posta, müşteri.
- **Dış depolar:** izlenmesi gereken, salt okunur başka depolar ya da canlı sistem.
- **Teslimler:** haftalarca süren ayrı işler (başvuru, rapor, belge seti).

Kuyruk varsa açık işleri alana göre say.

## 2. Gerekçe: en az biri, kanıtıyla

| Gerekçe | Kanıt | Arketip |
|---|---|---|
| **Ayrık yazma alanı.** Birlikte değişen ve başka kümelerle az kesişen bir yol kümesi var; kendi test kümesi var; o alanda birden çok açık iş birikiyor | `alanlar` tablosu (commit sayısı, eş-değişim oranı), test dosyaları, kuyruk sayımı | `kod` |
| **Dış kanal.** Sürekli gelen-giden yazışma ana ajanın bağlamını gürültüyle doldurur ve kendi hijyen sınırını ister | kanalın adı, haftalık mesaj hacmi (kullanıcı söyler) | `kanal` |
| **Ayrı teslimli uzun akış.** Kendi belgeleri, muhatabı ve takvimi olan iş | teslim tarihi, belge listesi | `yazar` (gerekirse `alt_yazar`) |
| **Salt okuma izleme.** Başka depoların ya da canlı sistemin sürekli ölçümü | depo listesi, ölçüm sıklığı | `gozlemci` |
| **Kayıt arşivi.** Toplantı ya da görüşme kayıtlarının doğrulanmış dökümü | arşiv yeri, kayıt sıklığı | `arsivci` |

## 3. Karşı gösterge: rol açma

- **Tek seferlik araştırma ya da inceleme:** alt ajan kullan (`agents/` ya da Agent aracı), rol açma.
- **Bir günde biten çok parçalı iş:** kullanıcı isterse workflow, istemezse ana ajanın kendi işi.
- **Aynı dosyalara ikinci yazar gerekecekse:** rol açılmaz, iş kuyrukta sıraya girer.
- **Alan küçükse** (son dönemde birkaç commit, açık iş yok): rol açma; iş geldiğinde yeniden ölç.

## 4. Sınır ve maliyet

- **Başlangıç:** ana ajan artı en çok iki rol. Kuyruk paralel iş gösterdikçe yeni rol açılır.
- **Ağır iş:** kod rolü sayısı yuva sayısını aşabilir, ama aynı anda koşan ağır iş yuva sayısını aşamaz.
- **Maliyet sütunu zorunlu.** Her rol için ana ajanın göreceği iş yazılır: plan onayı, birleşme, mesaj trafiği.
- **Kapanış.** İşi kalmayan rol `rol-kapat` önerisi alır. Klasörü, dalı ve çalışma ağacı silinmez.

## 5. Öneri tablosu

Kullanıcıya bu biçimde sun:

| Rol | Arketip | Yazma alanı | Kendi kapısı | Kimle konuşur | Kanıt | Maliyet |
|---|---|---|---|---|---|---|
| `GIRDI` | kod | `src/okuyucu/**`, `tests/test_okuyucu*` | `pytest tests/test_okuyucu*` | ana ajan | 120 günde 34 commit; en yakın kümeyle eş-değişim 0,08; 5 açık iş | haftada ~3 onay ve birleşme |

Tablonun altına şunları ekle:
- önerilmeyen ama düşünülen roller ve nedenleri (karşı göstergeler);
- açılış sırası.

Kullanıcı seçmeden rol açma.

## 6. Yeniden değerlendirme

Her tur kapanışında (`tur-kapat`) iki soruyu sor:
- Kuyrukta bir alanda iş birikiyor mu? Birikiyorsa yeni rol öner.
- Bir rol iki tur boyunca iş almadı mı? Almadıysa kapanış öner.

Öneri kullanıcıya gider; ana ajan kendi başına rol açmaz ve kapatmaz.
