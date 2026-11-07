> **DURUM: CANLI-ŞERHLİ** · bu iskeletin çıktığı kaynak projenin rol haritası · anonim: kişi, firma ve alan adları çıkarıldı · 07.11.2026 ölçümü

# Örnek: kaynak projenin rol haritası

**Kaynak proje:** deterministik bir hesap motoru. Bir canlı web ürününün veri kaynağıdır; ürünün arka uç ve ön yüzü ayrı depolardadır.

**Çalışanlar:**
- bir kullanıcı (teknik yönetici, push ve kapsam kararları);
- bir alan otoritesi (iş tarafında hesap kurallarının sahibi);
- bir ekip (arka uç ve ön yüz geliştiricileri).

Düzen proje sürerken adım adım büyüdü; 07.11.2026'da adres defterinde 13 rol vardı. Rol adları burada anonim; arketipler bu iskeletinkiler.

## Roller

| Rol (anonim) | Arketip | Neden açıldı (ROL_ONERME §2) | Nerede çalıştı | Durum |
|---|---|---|---|---|
| `ANA` | koordinatör | — | proje klasörü, ana dal | açık |
| `KOD-GIRDI` | kod | Bir girdi türünün okuyucuları ayrı bir klasör kümesiydi; kendi test kümesi vardı ve en çok işi o biriktirdi | kendi çalışma ağacı, iş başına dal | açık |
| `KOD-KONTROL` | kod | Kontrol kataloğu ve kontrol kodları ayrı bir yol kümesiydi | kendi çalışma ağacı | kapandı |
| `KOD-RAPOR` | kod | Raporlama katmanı ayrı bir yol kümesiydi | kendi çalışma ağacı | açık |
| `KOD-KAYIT` | kod | Yeni bir ürün dilimi; ilk iş ölçümdü, kod yoktu | kendi çalışma ağacı | açık |
| `KANAL` | kanal | Ekip sohbet kanalındaki trafik ana ajanın bağlamını dolduruyordu | proje klasörü ve yönlendirici; dosyaları kendi klasöründe | açık |
| `ONYUZ-TAKIP` | gözlemci | Ekibin iş takip sayfasının tek yazarı | proje klasörü ve yönlendirici | durduruldu |
| `GOZLEMCI-PLATFORM` | gözlemci | Ürünün bütün depoları ve iş listesi sürekli ölçülüyordu | proje klasörü ve yönlendirici | durduruldu |
| `YAZAR-BASVURU` | yazar | Ayrı takvimli bir hibe başvurusu | proje klasörü ve yönlendirici | açık |
| `ALT-YAZAR-1`, `ALT-YAZAR-2` | alt yazar | Başvurunun paralel bölümleri; okuma alanı kilitle kendi klasörüne kapatıldı | kendi klasörü, kilit | açık |
| `ARSIVCI` | arşivci | Toplantı kayıtlarının konuşmacıya göre ayrılmış dökümü | depo dışında arşiv klasörü | açık |
| `DIS-PROJE` | yazar | Kullanıcının başka bir işi; kilitle bu projeden ayrıldı | kendi klasörü, kilit | açık |

## Kaynak projede ne işe yaradı

- **Tek koordinatör.** Birleştirmeyi, canlı belgeleri ve hafızayı tek oturum yazdı. Roller yalnız öneri yaptı. Aynı dosyaya iki yazar düşmedi.
- **İş başına dal ve ayrı çalışma ağacı.** Bunlardan önce bütün oturumlar tek bir çalışma ağacını paylaşıyordu ve bir commit başka oturumun yarım işini de içine alabiliyordu.
- **Örneklemeyle onay.** Ana ajan rolün planındaki iddiaları kendisi ölçtü. Bir planda canlı ürünün hangi belgeyi ana belge saydığı varsayılmıştı; ölçüm bu varsayımın her durumda tutmadığını gösterdi.
- **Tam kapı.** Bir birleşmede dar test kümesi geçti; tam süit, değişikliğin dokunduğu dosyayı da denetleyen bir çıktı bekçisini düşürdü.
- **"Fark yok"a şüphe.** Sürüm karşılaştırma aracının bir belge türünü hiç beslemediği ortaya çıktı. Araç düzeltildi ve o türdeki eski değişikliklerin farkları beklenen fark olarak kayda girdi.

## İskelette neyi farklı yaptık

| Kaynak projede (07.11.2026 ölçümü) | İskelette |
|---|---|
| Kod dışı roller proje klasöründe açılıyor, kimliklerini ortak bir yönlendirici dosyasından buluyordu | Her rol kendi klasöründe açılır. Kart, üst klasör `CLAUDE.md`'si olarak kendiliğinden yüklenir |
| Kurallar yalnız düzyazıydı, hiç kanca yoktu | Push, zorla push, dal silme ve rolde birleştirme kanca ve izin kuralıyla engellenir |
| Proje talimatı 20 KB, rol kartları 10–21 KB idi | Talimat bütçesi 8 KB. Prosedürler becerilerde |
| Seyir defterlerinde katlama eşiği yoktu; üç defter 540–942 KB'a çıktı | 100 KB'da `katla` uyarısı. Sıkıştırmadan sonra kanca "Şimdi" bölümünü bağlama ekler |
| Alt yazar kilidi elle yazılmış, mutlak yollu bir yasak listesiydi | Kilit kayıttan üretilir; her rol açılışında bütün kilitler tazelenir |
| Oturum adları elle veriliyordu (`/rename`) | Açılış komutu adı ve kilidi taşır: `claude -n <ROL> --settings kilit.json` |
| Belgelerde makineye özgü mutlak yollar vardı | Yollar tek bir yerel dosyada (`iskelet.local.json`). Commit edilen belgeler yol taşımaz |
