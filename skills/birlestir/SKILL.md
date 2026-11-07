---
name: birlestir
description: Bir rol dalını bağımsız okuma ve birleşim kapısından geçirip ana dala birleştirir, canlı belgeleri günceller, commit atar; push etmez. Bir rol "birleşmeye hazır, uç <hash>" dediğinde.
argument-hint: "<dal> <uç hash'i>"
---

Argümanlar: $ARGUMENTS

1. **Uç:** `git rev-parse <dal>` rolün bildirdiği hash'le aynı olmalı. Değilse dur ve sor.
2. **İzin:** `git diff --stat <taban>...<dal>`. Onaydaki dar izin dışında dosya varsa dur. Taban, dalın ana daldan ayrıldığı noktadır: `git merge-base <ana dal> <dal>`.
3. **Bağımsız okuma:** Değişikliği kendin oku.
   - Hesap, sözleşme yüzeyi ya da güvenlik dosyalarını satır satır oku.
   - Rolün iddiası ile kodun yaptığı aynı mı?
   - Test, iddiayı gerçekten sınıyor mu?
4. **Birleşim kapısı:**
   - rolün dar kümesi;
   - değişen dosyaların bekçi testleri;
   - ana dalda rolün tabanından sonra değişen testler (`git diff --name-only <taban> <ana dal> -- '*test*'`).
   Tam süiti rolün son ucunda rol koşmadıysa kendin koş; yuva gerekir. Parçanın yeşili ürünün yeşili değildir.
5. **Birleştir:** `git merge --no-ff --no-commit <dal>`
6. **Belgeler:**
   - kuyruk satırı `✅ GG.AA BİRLEŞTİ (commit)`;
   - `PLAN.md` paragrafı ve sürüm; sayılar komutla;
   - `docs/BURADAN_BASLA.md` satırı (yeni belge varsa);
   - `docs/VAZGECILENLER.md`;
   - `docs/DURUM.md`;
   - sözleşme yüzeyi değiştiyse etki kaydı.
7. **Denetle:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py dogrula --proje .
   ```
   Projenin belge kapısı varsa onu da koş.
8. **Commit:** Mesajda ne değişti, hangi rol, hangi kapılar ve sonuçları bulunur. Yalnız birleşmenin dosyalarını al; çıplak `git commit -a` kullanma.
9. **Bildir:** Role yaz: birleşme commit'i ve sıradaki iş. **Push etme.** Push kullanıcının sözüyle olur.
