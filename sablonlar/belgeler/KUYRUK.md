> **DURUM: CANLI** · {{PROJE_ADI}} tek iş kuyruğu · satırı {{ANA_AJAN}} açar ve kapatır · kapanan satır silinmez

# İş kuyruğu

Her iş bir satırdır. Başka belge iş numarası açmaz.

**Sütunlar:**
- **Kimlik:** `**{{KUYRUK_ONEK}}-NNN**`; kapanınca başına `✅ ` eklenir.
- **İş:** ne yapılacak, bir-iki cümle.
- **Kaynak:** isteyen, belge ya da konuşma.
- **Sahip:** rol adı.
- **Durum:** aşağıdaki değerlerden biri.
- **Kabul ölçütü · doğrulama komutu:** ikisi de zorunlu.
- **Dosyalar:** iznin dar kapsamı (pathspec).

**Durum değerleri:**
- `☐ AÇIK`
- `◐ SÜRÜYOR (onay: tarih)`
- `⏸ BEKLİYOR (kimden, ne)`
- `✅ GG.AA BİRLEŞTİ (commit)`
- `⛔ DÜŞTÜ (neden)`

| Kimlik | İş | Kaynak | Sahip | Durum | Kabul ölçütü · doğrulama komutu | Dosyalar |
|---|---|---|---|---|---|---|

*Satır sayısı: 0. Komut: `grep -c '^| \(✅ \)\?\*\*{{KUYRUK_ONEK}}-' docs/gorevler/KUYRUK.md`*
