> **DURUM: CANLI** · kurulum akışı · `kur` becerisi ve eklentisiz kurulum bu belgeyi yürütür

# Kurulum akışı

Bu belgeyi okuyan sen, kurulacak projenin **ana ajanısın**. Adın kullanıcının isteminde yazar; yazmıyorsa sor. Adımları sırayla uygula ve her adımın sonunda tek satır durum yaz.

**ISKELET** bu belgenin bulunduğu klasördür. Eklenti kipinde bu klasör `${CLAUDE_PLUGIN_ROOT}`, eklentisiz kipte kullanıcının verdiği yoldur. Aşağıdaki komutlarda `ISKELET` yerine gerçek yolu yaz.

## 0. Yoklama (soru sormadan)

```bash
claude --version                      # 2.1.224 ve üstü: oturumlar arası mesajlaşma var
git rev-parse --show-toplevel         # proje bir git deposu olmalı; değilse kullanıcıya sor, kendin git init yapma
git status --porcelain | head
python3 --version                     # 3.8 ve üstü; PATH'teki python3 standart kütüphanesini okuyamıyorsa (yalıtılmış ortam) /usr/bin/python3 dene
ls; ls docs 2>/dev/null | head        # var olan CLAUDE.md, PLAN, docs
```

Ayrıca şunlara bak:
- Test komutu: `pyproject.toml`, `package.json`, `Makefile`, `pytest.ini` vb.
- Hafıza klasörün: sistem isteminde "persistent file-based memory at …" diye yazar. Yoksa boş bırak.

Var olan `CLAUDE.md`'yi oku. Araç onun üzerine yazmaz, yanına `CLAUDE.iskelet.md` koyar (adım 3).

## 1. Mülakat (en çok beş soru, tek mesajda)

İstemde cevaplar ya da `sorusuz` sözü varsa bu adımı atla ve eksikleri varsayılanla doldur; hangi varsayımı kullandığını raporda yaz. Yoksa soruları numaralı, tek mesajda sor:

1. **Amaç:** proje ne yapar, "bitti" ölçütü ne? (bir cümle)
2. **Kim onaylar:** kullanıcının adı; varsa alan otoritesi (iş tarafında kararı veren kişi) ve neyi onayladığı.
3. **Kırmızı çizgiler:** dışarı çıkmaması gereken veri, salt okunur dış depolar, deploy kuralı. Varsayılan: push yalnız kullanıcının sözüyle.
4. **Paralellik:** aynı anda kaç ağır iş koşabilir (tam test, büyük ölçüm)? Varsayılan: 2.
5. **Oturum kökü:** rol klasörleri nerede dursun? Varsayılan: proje klasörünün yanında `<proje>_oturumlar/`. Proje klasörünün içi olamaz.

## 2. Çekirdeği üret

```bash
python3 ISKELET/araclar/iskelet.py kur \
  --proje . --ana-ajan <AD> --kullanici "<kullanıcı>" \
  --oturum-kok <oturum kökü> --yuva <N> \
  --kanca eklenti            # eklentisiz kurulumda: --kanca yerel
  [--hafiza <hafıza klasörü>]
```

Araç var olan dosyanın üzerine yazmaz. Çıktısında her dosya için `YAZILDI`, `AYNI`, `ATLANDI`, `BİRLEŞTİR` ya da `YAZILAMADI` görünür; çıktıyı kullanıcıya özetle. Kurulum yarıda kesildiyse aynı komutu yeniden koşmak güvenlidir: önceki koşunun yazdığı dosyalar `AYNI` geçer. `YAZILAMADI` satırı kurulumu durdurmaz; dosyayı kullanıcıya bildir, engeli aşmaya çalışma.

`--kanca yerel` kancaları `.claude/hooks/`'a, becerileri `.claude/skills/`'e kopyalar ve `.claude/settings.json`'a kanca kaydını ekler. `--kanca eklenti` kipinde bunları eklenti taşır. Bu kipte kullanıcının `claude plugin install ajan-iskeleti@ajan-iskeleti --scope project` komutunu koşmuş olması gerekir; `dogrula` bunu denetler.

## 3. Boşlukları doldur

Üretilen dosyalarda `<!-- DOLDUR: … -->` yorumları var. Yorumların yerine mülakat cevaplarını ve yoklamada bulduklarını yaz:
- `CLAUDE.md` (ya da `CLAUDE.iskelet.md`): amaç, test komutu, ana klasörler, kim onaylar, kırmızı çizgiler. **Bütçe 8 KB.** Ayrıntı belgeye gider, `CLAUDE.md`'ye işaretçi yazılır.
- `PLAN.md` rozeti: her sayı yanındaki komutla birlikte yazılır, örnek `test: 42 (python3 -m pytest --collect-only -q | tail -1)`. Sayıyı komutu koşup yaz, tahmin etme.
- Ana ajanın kartı (`<oturum kökü>/<ad>/CLAUDE.md`): "Kimsin" ve "Kapanış ölçütü".

`CLAUDE.iskelet.md` oluştuysa iki seçenek var: var olan `CLAUDE.md`'nin sonuna `@CLAUDE.iskelet.md` satırını eklemek ya da iki dosyayı birleştirmek. Hangisini yapacağını kullanıcıya sor.

`CLAUDE.local.md` oturum kökündeki iki dosyayı içe aktarır. Claude Code proje dışından içe aktarmayı bir kez onaya sunar; kullanıcıya bunu söyle.

## 4. Rol önerisi

`ISKELET/roller/ROL_ONERME.md`'yi oku ve yöntemini uygula (eklenti kipinde `/ajan-iskeleti:rol-oner`):

```bash
python3 ISKELET/araclar/iskelet.py alanlar --proje .
```

Öneriyi `ROL_ONERME.md` §5 biçimindeki tabloyla sun: yedi sütunun hepsi dolu (Kanıt sütununda komut çıktısından sayı, Maliyet sütununda ana ajanın göreceği iş). Tablonun altına önerilmeyen ama düşünülen rolleri karşı göstergesiyle ve açılış sırasını yaz. Kullanıcı seçmeden rol açma. İstemde "onay verilmiş say" varsa, yöntemin başlangıç sınırı içinde kalan önerileri aç.

## 5. Seçilen rolleri aç

Her rol için:

```bash
python3 ISKELET/araclar/iskelet.py rol --proje . --ad <ROL> --arketip <arketip> \
  [--alan '<pathspec>' ...] [--okuma '<yol>' ...] [--ust <ÜST ROL>] [--worktree]
```

- Kod rolü için `--worktree` çalışma ağacını ve ilk dalı açar. Çalışma ağacı ana dalın ucundan açılır; kurulum dosyaları commit edilmeden açılırsa rolün ağacında kancalar ve kurallar olmaz. Bu yüzden kod rolünü adım 7'deki commit'ten sonra aç ya da kullanıcıya bunu söyle.
- Araç kartı, seyir defterini, `kilit.json`'ı ve adres defteri satırını yazar, açılış komutunu basar.
- Kartın "Kimsin" ve "Kapanış ölçütü" boşluklarını doldur. Rolün ilk işi varsa `ISKELET/sablonlar/oturum/IS_BRIFI.md`'den bir iş brifi yaz ve kuyruğa satırını ekle.

## 6. Doğrula

```bash
python3 ISKELET/araclar/iskelet.py dogrula --proje .
```

`HATA: 0` olmadan kurulum bitmiş sayılmaz. Uyarıları kullanıcıya listele. Kalan `DOLDUR` boşlukları uyarı olarak görünür.

## 7. Rapor ve commit

Kullanıcıya şunları raporla:
- yazılan ve atlanan dosyalar;
- kullanılan varsayımlar;
- rol öneri tablosu, adım 4'teki biçimde (Maliyet sütunu ve önerilmeyen rollerle). Kullanıcı ara mesajları görmemiş olabilir; tablo son raporda yeniden yer alır;
- açılan roller ve her biri için açılış komutu;
- yapılmayan adımlar.

Kurulum dosyalarını commit etmeyi kullanıcıya **sor**; o isterse tek commit'te topla. Push etme.

Son olarak `PLAN.md` tur günlüğüne kurulum paragrafını, hafızaya (varsa) "ajan-iskeleti kuruldu, sürüm, oturum kökü" satırını yaz.
