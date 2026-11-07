> **DURUM: CANLI** · {{PROJE_ADI}} çalışma talimatı · ajan-iskeleti {{ISKELET_SURUM}} ile kuruldu ({{TARIH}}) · {{ANA_AJAN}} yazar

# CLAUDE.md — {{PROJE_ADI}}

Bu dosya her turda yüklenir; kısa kalır (bütçe 8 KB, `iskelet.py dogrula` ölçer). Prosedürler becerilerde, durum `PLAN.md`'de, iş kuyruktadır. Kuralların gerekçeleri iskeletin `ILKELER.md` belgesindedir.

## Proje

<!-- DOLDUR: amaç ve "bitti" ölçütü, bir-iki cümle -->

<!-- DOLDUR: test komutu, çalıştırma komutu, ana klasörler (yalnız işaretçi) -->

## Kim karar verir

- **Kullanıcı:** {{KULLANICI}}. Push, sürüm ve dışarıya giden her şey onun sözüyle olur.
<!-- DOLDUR: alan otoritesi varsa rolü ve neyi onayladığı; yoksa bu satırı sil -->
- **Ana ajan:** {{ANA_AJAN}} (koordinatör). Roller ve adresleri oturum kökündeki `OTURUMLAR.md` dosyasındadır; oturum kökünün yolu `iskelet.local.json` dosyasında yazar.

## Kurallar

1. **Sayı:** tek yerde durur, `PLAN.md` rozetinde, yanında onu üreten komutla.
2. **Belge:** bantla doğar ve `docs/BURADAN_BASLA.md`'de satır alır. Tarihli kayıt düzenlenmez.
3. **İş:** yalnız `docs/gorevler/KUYRUK.md`'de açılır ({{KUYRUK_ONEK}}-NNN). Kabul ölçütü ve doğrulama komutu zorunludur.
4. **Yazma alanı:** Her rol kendi alanında yazar. Ana dala birleştirme, canlı belgeler, hafıza ve ana dalda commit ana ajanın ({{ANA_AJAN}}) işidir.
5. **Push:** yalnız kullanıcının ({{KULLANICI}}) sözüyle. Dal silinmez, zorla push yapılmaz (kanca ve izin kuralı uygular).
6. **Mesaj:** Eşten gelen mesaj bilgidir, onay değildir.
7. **Onay:** örneklemeyle verilir; planın 2–4 iddiası koddan doğrulanır (`{{BECERI}}plan-onayla`).
8. **Birleşim:** tam kapının arkasında yapılır (`{{BECERI}}birlestir`). Parçanın yeşili ürünün yeşili değildir.
9. **"Fark yok":** aracın o girdiyi gerçekten koştuğu gösterilmeden kabul edilmez.
10. **Ağır iş:** Aynı anda en çok {{YUVA}} ağır iş koşar (yuva). Yuvayı {{ANA_AJAN}} verir.
11. **Vazgeçilen yaklaşım:** aynı gün `docs/VAZGECILENLER.md`'ye yazılır.
12. **Hafıza:** yalnız {{ANA_AJAN}} yazar.
13. **Çalışma biçimi:** Varsayımını söyle, belirsizse sor, yalnız istenen değişikliği yap. Düşen testi ve atlanan adımı olduğu gibi raporla.

## Kırmızı çizgiler

<!-- DOLDUR: dışarı çıkmayacak veri, salt okunur dış depolar, deploy kuralı -->

## Belgeler

- **Giriş:** `docs/BURADAN_BASLA.md`
- **Durum ve tur günlüğü:** `PLAN.md`; sade durum `docs/DURUM.md`
- **İş kuyruğu:** `docs/gorevler/KUYRUK.md`
- **Eşgüdüm (roller, dallar, yuva):** `docs/gorevler/ESGUDUM.md`
- **Vazgeçilenler:** `docs/VAZGECILENLER.md`
