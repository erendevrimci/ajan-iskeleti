---
name: tur-kapat
description: Bir çalışma turunu kapatır; yayılma taraması, arşiv taşımaları, seyir katlama, hafıza, rol değerlendirmesi ve doğrulama yapılır. Kullanıcı turu kapatmayı istediğinde ya da büyük bir iş bloğu bittiğinde.
---

1. **Yayılma taraması:** Turda kapanan ya da vazgeçilen her işin adını projede ara (`grep -rn`). Canlı belgede kalan bayat "yapılacak" cümlesini düzelt. Tarihli kayda dokunma.
2. **Arşiv:**
   - **Atıf kontrolü:** Kapanan iş brifini ya da sonuç belgesini taşımadan önce `grep -rn <dosya adı>` koş. Canlı atıfları güncelle, tarihli atıflara dokunma.
   - **Taşıma:** `git mv` ile `arsiv/<YYYYMMDD>/` altına taşı. Bandı `KAPANDI-TARİHLİ` yap. `docs/BURADAN_BASLA.md` satırını 📁 olarak güncelle.
3. **Katlama:**
   - **PLAN:** 80 KB'ı geçtiyse eski paragraflar `arsiv/plan_arsiv_<YYYYMMDD>.md`'ye gider.
   - **Seyir defterleri:** 100 KB'ı geçen için role `iskelet.py katla` önerilir; ana ajanın kendi defterini sen katla.
4. **Hafıza:**
   - Rollerin devirlerindeki "hafıza adayı" satırlarını süz.
   - Kalıcı dersi konu dosyasına yaz; dizinin bölüm sınırlarını koru.
   - Kapanan konuyu dizinden arşiv dizinine indir.
5. **Roller:** `rol-oner`'in 6. adımı uygulanır: iş birikiyor mu, iş almayan rol var mı. Öneriyi kullanıcıya sun.
6. **Doğrula:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py dogrula --proje .
   ```
   `HATA: 0` olmalı.
7. **Rapor:** Kullanıcıya bir paragraf: ne kapandı, ne açık, ne bekliyor, kimden.
