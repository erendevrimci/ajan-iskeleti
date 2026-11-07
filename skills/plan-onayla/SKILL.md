---
name: plan-onayla
description: Bir rolün ölçüm ve plan belgesini örneklemeyle doğrular ve onay ya da ret metni yazar. Bir rol "plan hazır, onay bekliyorum" dediğinde.
argument-hint: "<ROL> <plan belgesinin yolu ya da dal>"
---

Argümanlar: $ARGUMENTS

1. **Oku:** Planı baştan sona oku. İddialarını listele.
2. **Seç:** Doğrulanacak 2–4 iddia seç. En riskliler:
   - sayılar;
   - `dosya:satır` atıfları;
   - "değişmez", "etkilemez", "kullanılmıyor" iddiaları;
   - dış sistem ya da canlı ürün davranışı;
   - ölçüm aracının bu girdiyi gerçekten görüp görmediği (ILKELER 9).
3. **Doğrula:** Her iddiayı kendin, komutla doğrula. Rolün çıktısına yaslanma. Gerekirse `bagimsiz-okuyucu` alt ajanına iddiayı değil kodu ver.
4. **Karar:**
   - **Doğrulanmayan iddia varsa onay yok.** Role hangi iddianın tutmadığını kanıtıyla yaz, düzeltilmiş plan iste.
   - **Hepsi tutarsa onay metni yaz.** Metinde şunlar bulunur:
     - kararlar (seçenekli sorularda hangi seçenek);
     - dar izin (pathspec);
     - kabul ölçütü ve doğrulama komutu;
     - kapılar (dar küme, bekçiler, tam süit);
     - yuva;
     - etki notu (sözleşme yüzeyi varsa);
     - açık kalanlar.
5. **Kullanıcı kararı:** Kullanıcının kararını gerektiren seçenek varsa, onay metnini kullanıcıya sor ve cevabı bekle. Senin yetkin yalnız kullanıcının verdiği kapsamdadır.
6. **Kaydet:**
   - kuyruk satırı `◐ SÜRÜYOR (onay: tarih)`;
   - PLAN paragrafı;
   - vazgeçilen seçenekler `docs/VAZGECILENLER.md`'ye.
