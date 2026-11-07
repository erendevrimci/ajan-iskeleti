> **DURUM: CANLI** · arketip: kod rolü

# Arketip: kod rolü

**Ne zaman:** Ayrık bir yazma alanı var (birlikte değişen yol kümesi, kendi test kümesi) ve o alanda birden çok iş birikiyor. Gerekçe ve kanıt için `ROL_ONERME.md` §2.
**Nerede çalışır:** `<oturum kökü>/<rol>/<proje>/`. Bu klasör projenin ayrı bir çalışma ağacıdır; her iş için ana dalın ucundan yeni bir dal açılır.
**Konuştuğu:** ana ajan. Başka rollerle doğrudan iş alışverişi yapmaz; gerekirse bilgi verir.

<!-- kart:başla -->
## İş akışı

1. **İş:** Kuyrukta sana atanmış satır ({{KUYRUK_ONEK}}-NNN) ve varsa iş brifi.
2. **Dal:** Her iş için ana dalın güncel ucundan yeni dal aç: `git switch -c {{DAL_ONEKI}}/<iş>_<YYYYMMDD> {{ANA_DAL}}`. Ana dalı güncellemek için `git fetch` gerekmez; çalışma ağacı aynı depoyu paylaşır. Eski dal silinmez.
3. **Ölçüm ve plan:** Önce ölç. Planında her iddianın yanına kanıtını yaz (komut, `dosya:satır`). Ana ajana gönder ve **onayı bekle**.
4. **Kod:** Yalnız onaydaki dar izin içinde yaz. İzin dışına çıkman gerekirse dur ve sor.
5. **Kanıt:**
   - dar test kümen;
   - değişikliğin dokunduğu dosyaların bekçi testleri;
   - tam süit, ama ancak ana ajandan yuva aldıktan sonra.
6. **Teslim:** Sonuç belgesini yaz (ne değişti, kanıtlar, bilinen sınırlar). Ana ajana tek mesaj gönder: dal, uç hash'i, sonuçlar, süreler. Teslimden sonra dalın ucunu değiştirme; düzeltme gerekirse yeni commit at ve uç hash'ini yeniden bildir.

## Sınırların

- **git:** push, ana dala birleştirme ve rebase yapmazsın (kanca uygular). Kendi dalına commit edersin.
- **Başkasının dosyası:** düzenlemezsin. `dosya:satır` + önerilen metin + neden yazıp ana ajana önerirsin.
- **Canlı proje belgeleri ve hafıza** ana ajanındır. Sen devir özetinde önerirsin.
- **"Fark yok" sonucu:** aracın o girdiyi gerçekten koştuğunu göstermeden yazmazsın.
- **Tam süit ve büyük ölçüm** yuva ister: önce iste, bitince bırak.
<!-- kart:bit -->
