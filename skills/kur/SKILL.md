---
name: kur
description: ajan-iskeletini bu projeye kurar; mülakat, çekirdek dosyalar, rol önerisi, rol açma, doğrulama adımlarını yürütür. Yalnız kullanıcı iskeletin ya da ajan düzeninin kurulmasını açıkça istediğinde kullanılır.
argument-hint: "ana ajan: <AD> [kullanıcı: <ad>] [sorusuz ...]"
---

Sen bu projenin ana ajanısın. `${CLAUDE_PLUGIN_ROOT}/KUR.md` dosyasını oku ve adımlarını sırayla uygula.

- **ISKELET:** `${CLAUDE_PLUGIN_ROOT}`. Araç: `python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py`.
- **Kanca kipi:** Bu beceri eklentiden çalışıyorsa `--kanca eklenti`. Projenin `.claude/skills/` klasörüne kopyalanmışsa `--kanca yerel`.
- **Kullanıcının argümanları:** $ARGUMENTS
