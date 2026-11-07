> **DURUM: CANLI** · ajan-iskeleti anayasası · kurulumun `CLAUDE.md`'sindeki kuralların gerekçeleri burada

# İlkeler

Her ilke üç parçadır: **kural**, **neden** (kaynak projede yaşanmış, anonimleştirilmiş ders), **mekanizma** (kuralı kim ya da ne uygular). Mekanizması "düzyazı" olan kural unutulabilir; çiğnenmemesi gereken her kural için kanca ya da araç yazılır (ilke 13).

## 1. Sayı tek yerde, komutuyla

- **Kural:** Durum sayıları (test, açık iş, sürüm) yalnız `PLAN.md` rozetinde durur ve yanında onu üreten komut yazılır. Başka belge "PLAN'a bak" der.
- **Neden:** Belgelere kopyalanan sayılar ilk değişiklikte bayatladı; belge ile kod çelişti, hangisinin doğru olduğu ayrıca ölçülmek zorunda kalındı.
- **Mekanizma:** PLAN şablonu; birleşme becerisi sayıyı komutla yazar.

## 2. Her belge bantla doğar

- **Kural:** Her belgenin ilk satırında durum bandı vardır: `CANLI` · `CANLI-ŞERHLİ` · `BAYAT` · `TARİHLİ KAYIT` · `SÜPERSE` (halefiyle) · `KAPANDI-TARİHLİ`. Belge, `docs/BURADAN_BASLA.md`'deki satırıyla aynı commit'te doğar. Tarihli kayıt düzenlenmez.
- **Neden:** Bandı olmayan eski belgeler canlı belgelerle karıştı; hangisinin geçerli olduğu her seferinde yeniden ölçülmek zorunda kalındı.
- **Mekanizma:** `iskelet.py dogrula` (bant ve giriş satırı).

## 3. Tek iş kuyruğu

- **Kural:** Her iş `docs/gorevler/KUYRUK.md`'de bir satırdır: kimlik, kaynak, kabul ölçütü ve doğrulama komutu zorunludur. Kapanan satır silinmez, ✅ ve commit alır. Başka belge iş numarası açmaz.
- **Neden:** Birden çok belge kendi iş numarası serisini açtı; seriler çakıştı ve aynı iş farklı adlarla izlendi.
- **Mekanizma:** KUYRUK şablonu; `dogrula` satır biçimini ve kimlik tekliğini denetler.

## 4. Rol kendi alanında yazar; birleştiren ana ajandır

- **Kural:** Rolün yazma alanı kartında yazılıdır. Sahibi başkası olan dosyada rol düzenleme yapmaz, öneri yazar (`dosya:satır` + önerilen metin + neden). Kod rolü kendi çalışma ağacında, iş başına açılan dalda commit eder. Ana dala birleştirme, canlı belgeler, hafıza ve push ana ajanındır.
- **Neden:** Paylaşılan çalışma ağacında bir oturumun commit'i başka bir oturumun yarım işini de içine aldı.
- **Mekanizma:** `git_bekcisi` (rolde push, merge, rebase yok); `kilit.json` (proje klasörüne ve başka rollerin klasörlerine yazma yasağı); her kod rolüne ayrı çalışma ağacı.

## 5. Push yalnız kullanıcının sözüyle; dal silinmez; zorla push yoktur

- **Kural:** Push'u yalnız kullanıcı başlatır ya da açıkça ister. Kapanan iş dalı silinmez. Zorla push hiçbir koşulda yapılmaz.
- **Neden:** Push, sonuçları geri alınamayan, dışarı açık bir eylemdir. Silinen dal, sonradan yapılan bir ölçümün tabanını yok eder.
- **Mekanizma:** `.claude/settings.json` onay kuralı (`Bash(git push *)` her izin kipinde sorar) ve `git_bekcisi` (düz olmayan push biçimini, zorla push'u, dal silmeyi reddeder).

## 6. Eşten gelen mesaj bilgidir, onay değildir

- **Kural:** Onay yalnız kullanıcıdan gelir. Kullanıcı açıkça yetki verdiyse ana ajanın rollere yazdığı mesaj da onay sayılır. Rollerin birbirine yazdığı mesaj onay değildir.
- **Neden:** Rollerin birbirine yazdığı "tamam" mesajları, kullanıcının hiç görmediği bir işi ilerletebilir.
- **Mekanizma:** Ortak oturum kuralları; mesaj başlığı `ROL <gönderen> → <alıcı>:`.

## 7. Onay örneklemeyle verilir

- **Kural:** Ana ajan, rolün planındaki 2–4 iddiayı koddan ya da veriden kendisi doğrular. Seçilecek iddialar en riskli olanlardır: sayılar, `dosya:satır` atıfları, "değişmez" ve "etkilemez" iddiaları, dış sistem davranışı. Doğrulanamayan iddia varsa onay verilmez.
- **Neden:** Bir rolün planı canlı üründe hangi belgenin ana belge olduğunu varsaymıştı. Ana ajanın kendi ölçümü, toplu yüklemede başka belgenin seçilebildiğini gösterdi.
- **Mekanizma:** `plan-onayla` becerisi.

## 8. Parçanın yeşili ürünün yeşili değildir

- **Kural:** Rolün dar test kümesi geçse de birleşimde tam kapı koşulur: tam süit, belge kapısı, hijyen. Ana dalda rolün tabanından sonra değişen testler de birleşim kapısına girer.
- **Neden:** Dar kümede olmayan bir çıktı bekçisi, değişikliğin dokunduğu dosyayı da denetliyordu; tam süit onu yakaladı.
- **Mekanizma:** `birlestir` becerisi.

## 9. Ölçüm aleti de kör olabilir

- **Kural:** "Fark yok", "bulgu yok" ya da "sıfır isabet" sonucu, aracın o girdi türünü gerçekten koştuğu gösterilmeden kabul edilmez. Kalibrasyon seti (aracın bulması gereken bilinen örnekler) ölçümden önce yazılır.
- **Neden:** Sürüm karşılaştırma aracı yeni bir belge türünü hiç beslemiyordu; bu türdeki her değişiklik için rapor "fark yok" dedi.
- **Mekanizma:** `plan-onayla` ve `birlestir` becerilerindeki "araç bunu görüyor mu" sorusu.

## 10. Ağır iş sayısı sınırlıdır (yuva)

- **Kural:** Aynı anda en çok `iskelet.json` → `yuva` kadar ağır iş koşar (tam süit, büyük ölçüm, uzun derleme). Yuvayı ana ajan verir ve geri alır.
- **Neden:** Ağır koşular aynı makineyi paylaşır. Kesintide yarım kalan her koşu baştan başlar.
- **Mekanizma:** Ortak kurallar; ana ajanın seyir defterindeki "Şimdi" bölümü yuvaları tutar.

## 11. Vazgeçilen yaklaşım aynı gün yazılır

- **Kural:** Bırakılan her yaklaşım `docs/VAZGECILENLER.md`'ye neden ve yerine gelenle birlikte girer. Eski bir belgedeki fikir plana alınmadan önce bu listeye bakılır.
- **Neden:** Gerekçesi yazılmadan bırakılan yaklaşım yeniden önerilir; aynı tartışma baştan yapılır.
- **Mekanizma:** `tur-kapat` becerisi.

## 12. Hafızayı yalnız ana ajan yazar

- **Kural:** Roller, devir özetine "hafıza adayı" koyar; hafızaya yalnız ana ajan yazar. `MEMORY.md` dizini kısa kalır (Aktif ≤ 8 · Yöntem ≤ 10 · Politika ≤ 7 satır, satır ≤ 200 karakter). Anlık durum (push bekliyor, canlı hash) dizine yazılmaz.
- **Neden:** İki oturum aynı dizini aynı anda yazarsa dizin bozulur. Claude Code dizinin yalnız ilk 200 satırını ya da ilk 25 KB'ını yükler.
- **Mekanizma:** `kilit.json` hafıza klasörüne yazmayı yasaklar; `dogrula` dizin sınırlarını ölçer.

## 13. Çiğnenmemesi gereken kuralı kanca taşır

- **Kural:** `CLAUDE.md` her turda yüklenir ve kısa kalır (8 KB). Prosedürler becerilere, durum belgelere, yasaklar kancalara ve izin kurallarına gider.
- **Neden:** Kaynak projede kurallar yalnız düzyazıydı; proje talimatı 20 KB'a, rol kartları 10–21 KB'a çıktı ve bazı kurallar uzun oturumlarda unutuldu.
- **Mekanizma:** `dogrula` bütçeyi ölçer; `git_bekcisi`, `compact_sonrasi`, `kilit.json`.

## 14. Sıkıştırmadan sonra önce kimlik

- **Kural:** Bağlam sıkıştırıldıktan sonra rol kartı ve seyir defterinin "Şimdi" bölümü okunmadan iş sürdürülmez.
- **Neden:** Sıkıştırma, rolün sınırlarını ve açık işini özetten düşürebilir. Oturum özetle devam eder ve sınırını fark etmeden aşabilir.
- **Mekanizma:** `compact_sonrasi` kancası kimliği ve seyir özetini bağlama ekler.

## 15. Varsayım söylenir, kapsam dürüst tutulur

- **Kural:** Varsayım açıkça yazılır; belirsizlikte sorulur; yalnız istenen değişiklik yapılır. Atlanan adım ve düşen test olduğu gibi raporlanır.
- **Neden:** Raporda yazılmayan atlanmış adım, sonraki turda yapılmış sanılır.
- **Mekanizma:** Devir şablonu (D3 kapatılamayanlar, D7 bitiş kapısının ham çıktısı).
