> **DURUM: CANLI** · {{PROJE_ADI}} eşgüdüm protokolü · roller, dallar, yuva, kapılar · {{ANA_AJAN}} yazar

# Eşgüdüm

## 1. Roller ve yazma alanları

Rollerin listesi, klasörleri ve açılış komutları oturum kökündeki `OTURUMLAR.md` dosyasındadır; o dosyayı araç üretir. Her rolün yazma alanı kendi kartında yazar. Bu tablo, alanların kime ait olduğunu tek bakışta gösterir. Rol açılıp kapandıkça {{ANA_AJAN}} günceller.

| Alan (pathspec) | Sahip | Not |
|---|---|---|
| `PLAN.md`, `docs/**`, `CLAUDE.md`, `.claude/**`, `iskelet.json` | {{ANA_AJAN}} | Canlı belgeler ve kurallar |

## 2. Dal düzeni

- **Kod rolü:**
  - kendi çalışma ağacında çalışır (`<oturum kökü>/<rol>/<proje>`);
  - her iş için `{{ANA_DAL}}` ucundan dal açar: `<rol>/<iş>_<YYYYMMDD>`;
  - kendi dalına commit eder.
- **Ana dal:** {{ANA_AJAN}} `git merge --no-ff --no-commit <dal>` ile birleştirir, belgeleri günceller, tek commit atar.
- **Dallar silinmez.** Bir sonraki iş yeni daldır.

## 3. Yuva

- **Sayı:** Aynı anda en çok {{YUVA}} ağır iş (tam süit, büyük ölçüm, uzun derleme) koşar.
- **İsteme:** Rol yuvayı mesajla ister: `ROL <rol> → {{ANA_AJAN}}: yuva istiyorum, <iş>, tahmini süre`.
- **Verme ve geri alma:** {{ANA_AJAN}} yuvayı verir ve seyir defterinin "Şimdi" bölümüne yazar. Rol iş bitince yuvayı bırakır.

## 4. Başlangıç kapısı (rolün bir işteki ilk komutu)

```bash
git status --porcelain
git log --oneline -1
```

Kendi yapmadığın bir değişiklik görürsen dur ve ana ajana ({{ANA_AJAN}}) bildir.

## 5. Bitiş kapısı (teslimden önceki son komut)

```bash
git status --porcelain
git diff --stat <taban>..HEAD
```

Ham çıktı devir özetine (D7) girer. Kendi izin listende olmayan bir yol diff'te görünüyorsa bunu açıkça yaz.

## 6. Kanıt disiplini

- **Komut:** Her iddianın yanında komut ve ham çıktısı ya da `dosya:satır` bulunur.
- **Damga:** Dış depoya ilişkin hükümde tarih, komut ve hash yazılır.
- **"Fark yok":** aracın o girdi türünü gerçekten koştuğu gösterilmeden yazılmaz.
