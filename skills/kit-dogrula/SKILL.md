---
name: kit-dogrula
description: ajan-iskeleti kurulumunu denetler; bantlar, giriş satırları, izin kuralları, kancalar, kuyruk biçimi, rol kartları, kilitler ve hafıza sınırlarına bakar, hataları düzeltir. Kurulumdan sonra, birleşmeden sonra ya da kullanıcı "düzen sağlam mı" diye sorduğunda.
---

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py dogrula --proje .
```

**HATA satırları:** Her birini düzelt ve yeniden koş. Bu dosyalar senin alanındadır: belgeler, bantlar, giriş satırları, kuyruk biçimi.

Şu üç hatayı kendin düzeltme, kullanıcıya sor:
- izin kuralı eksik;
- kanca kayıtlı değil;
- eklenti etkin değil.

**UYARI satırları:** Kullanıcıya listele. `DOLDUR` boşluklarını mülakat bilgisiyle doldurabiliyorsan doldur. Bütçe aşımında ayrıntıyı belgeye taşı ve `CLAUDE.md`'ye işaretçi bırak.

**Rol kilitleri:** Eklenti güncellemesinden sonra kilitlerdeki kanca yolları eskiyebilir. Yenilemek için:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py rol --proje . --tazele
```
