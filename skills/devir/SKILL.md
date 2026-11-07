---
name: devir
description: Devir özeti yazar; rol işi bitince ya da oturum kapanırken ana ajana, ana ajan oturum değişirken bir sonraki oturuma. Kullanıcı ya da ana ajan devir istediğinde, bağlam dolmak üzereyken.
---

**Rol isen:**

1. Bitiş kapısını koş:
   ```bash
   git status --porcelain
   git diff --stat <taban>..HEAD
   ```
   Çalışma ağacın yoksa yalnız kendi klasörünün dosya listesini al.
2. `${CLAUDE_PLUGIN_ROOT}/sablonlar/oturum/DEVIR.md` şablonuyla `<rol klasörü>/DEVIR_<YYYYMMDD>.md` yaz. Yarım iş varsa D3'e yaz; yapılmış gibi gösterme.
3. Seyir defterinin "Şimdi" bölümünü güncelle.
4. Ana ajana tek mesajla yolu gönder.

**Ana ajan isen:**

1. Oturum kökünde kendi klasörüne `DEVIR_<YYYYMMDD>.md` yaz. Bu bir yeni tarihli belgedir; eski devri yerinde tazeleme. İçeriği:
   - bekleyenler (rol başına: açık iş, beklenen, son uç, yuva);
   - kullanıcının vermediği kararlar;
   - push edilmemiş commit'ler (`git log --oneline origin/<ana dal>..<ana dal> | wc -l`; sayıyı komutla yaz);
   - son birleşmeler.
2. Seyir defterinin "Şimdi" bölümünü bu belgeye işaret edecek biçimde güncelle.
