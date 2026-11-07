---
name: rol-ac
description: Kullanıcının seçtiği bir rolü açar; rol kartı, seyir defteri, kilit, adres defteri satırı ve kod rolünde çalışma ağacıyla birlikte, ardından açılış komutunu verir. Kullanıcı bir rolün açılmasını onayladığında.
argument-hint: "<ROL> <arketip> [alan ...]"
---

Argümanlar: $ARGUMENTS

1. **Ön koşul (kod rolü):** Kurulum dosyaları ana dalda commit edilmiş olmalı (`git status --porcelain`). Edilmemişse rolün çalışma ağacında kurallar ve kancalar olmaz; kullanıcıya söyle ve commit iste.
2. **Aç:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py rol --proje . --ad <ROL> --arketip <arketip> \
     [--alan '<pathspec>' ...] [--okuma '<yol>' ...] [--ust <ÜST>] [--worktree]
   ```
3. **Kartı tamamla:** "Kimsin" (görev, teslim) ve "Kapanış ölçütü" boşluklarını doldur.
4. **Belgeler:**
   - `docs/gorevler/ESGUDUM.md` §1 alan tablosuna satır ekle.
   - `PLAN.md` tur günlüğüne paragraf yaz.
   - Rolün ilk işi varsa kuyruğa satır ve `${CLAUDE_PLUGIN_ROOT}/sablonlar/oturum/IS_BRIFI.md`'den iş brifi yaz. Brif çözüm önermez; ölçüm sorularını ve kapıları verir.
5. **Açılış komutu:** Kullanıcıya ver; rol yeni bir terminalde açılır. İlk mesajı geldiğinde rolün kartı okuduğunu tek soruyla sına (ör. "yazma alanın ne?").
