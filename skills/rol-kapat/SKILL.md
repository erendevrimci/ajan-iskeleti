---
name: rol-kapat
description: Kullanıcının kapanmasına karar verdiği rolü kapatır; kart bandı, kayıt, kilitler ve adres defteri güncellenir, klasör, dal ve çalışma ağacı silinmez. Kullanıcı bir rolün kapanmasını onayladığında.
argument-hint: "<ROL>"
---

Argümanlar: $ARGUMENTS

1. **Açık iş:** Rolün açık işi var mı bak (`SEYIR.md` "Şimdi", kuyrukta sahibi o olan ☐ ◐ ⏸ satırlar). Varsa kapatmadan önce kullanıcıya sor: devredilecek mi, düşecek mi.
2. **Devir özeti:** Rolden iste (`DEVIR` şablonu). Rol açık değilse seyir defterinden kendin çıkar.
3. **Kapat:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py kapat --proje . --ad <ROL>
   ```
4. **Belgeler:**
   - `docs/gorevler/ESGUDUM.md` §1 alan tablosunu güncelle.
   - `PLAN.md` paragrafına yaz: neden kapandı, hangi işler kime devredildi.
5. **Silme yok:** Klasör, dal ve çalışma ağacı yerinde kalır. Çalışma ağacının kaldırılması kullanıcının kararıdır.
