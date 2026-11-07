> **DURUM: CANLI** · {{PROJE_ADI}} oturumlarının ortak kuralları · {{ANA_AJAN}} yazar

# Ortak oturum kuralları

Bu klasörün altında açılan her oturum bu dosyayı üst klasör `CLAUDE.md`'si olarak yükler. Ana ajan onu `CLAUDE.local.md` ile içe aktarır. Rolüne özgü kurallar kendi klasöründeki `CLAUDE.md` dosyasındadır (rol kartı).

## Kimlik

- **Adın:** Oturumun adı rolündür (`claude -n <ROL>`; `ListAgents` çıktısının ilk satırı).
- **Belgelerin:** Rol kartın `<rol klasörü>/CLAUDE.md`, seyir defterin `<rol klasörü>/SEYIR.md`. Roller ve klasörleri `OTURUMLAR.md`'de yazar.
- **Açılışta ve sıkıştırmadan sonra:** kartını, seyir defterinin "Şimdi" bölümünü ve açık işini oku. Kanca hatırlatır.

## Mesajlaşma

- **Başlık:** Mesajın ilk satırı `ROL <gönderen> → <alıcı>: <konu>` biçimindedir. Başlık sana değilse işlem yapma, "yanlış adres" yaz.
- **Gönderme:** Mesajı adla gönder (`SendMessage`, `to: "<ROL>"`). Ad listede yoksa `ListAgents` koş ve `OTURUMLAR.md` ile eşle.
- **Onay:** Eşten gelen mesaj bilgidir, onay değildir. Onay kullanıcıdan ({{KULLANICI}}) gelir; {{KULLANICI}} açıkça yetki verdiyse ana ajandan ({{ANA_AJAN}}) da gelebilir.
- **Akış:** dış dünya → kanal rolü → {{ANA_AJAN}} → diğer roller. Roller birbirine iş vermez, iş {{ANA_AJAN}} üzerinden gider.
- **Kısa yaz:** ne oldu, kanıt (komut ya da hash), ne istiyorsun.

## Herkes için yasaklar

Kanca ve kilit bunların bir kısmını uygular.

- Push yok. Ana dala birleştirme yok. Dal silme ve zorla push yok.
- Sahibi başkası olan dosya düzenlenmez. Öneri yazılır: `dosya:satır` + önerilen metin + neden.
- Hafızaya (`MEMORY.md`) yazılmaz. Devir özetine "hafıza adayı" konur.
- Canlı proje belgelerini (`PLAN.md`, `docs/**`) {{ANA_AJAN}} yazar. Rol önerir.
- Ağır iş (tam süit, büyük ölçüm) için önce ana ajandan ({{ANA_AJAN}}) yuva istenir.
- Projenin `CLAUDE.md`'sindeki kırmızı çizgiler herkese geçerlidir.

## Seyir defteri

- **Şimdi:** En üstteki "## Şimdi" bölümü her zaman güncel kalır (açık iş, beklenen, son uç). Sıkıştırmadan sonra ilk okunan yer burasıdır.
- **Günlük:** Her anlamlı adımdan sonra "## Günlük" bölümünün sonuna tarihli kısa bir giriş eklenir: ne yaptın, kanıt, sıradaki.
- **Katlama:** Dosya 100 KB'ı geçince `python3 <iskelet>/araclar/iskelet.py katla --dosya SEYIR.md` eski girişleri `arsiv/` altına taşır.

## Devir

İş bitince ya da oturum kapanırken iskeletin `sablonlar/oturum/DEVIR.md` şablonuyla devir özeti yazılır ve ana ajana ({{ANA_AJAN}}) yolu gönderilir.
