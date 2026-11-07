---
name: rol-oner
description: Projeyi ölçüp kanıtıyla rol oturumu önerir (kod, kanal, gözlemci, yazar, alt yazar, arşivci) ya da işi kalmayan rolün kapanmasını önerir. Kurulumda, tur kapanışında ya da kullanıcı "hangi ajanlar gerekli" diye sorduğunda.
---

`${CLAUDE_PLUGIN_ROOT}/roller/ROL_ONERME.md` yöntemini uygula.

1. **Ölç:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/araclar/iskelet.py alanlar --proje .
   ```
   Kuyruk varsa açık işleri sahibe ve alana göre say. Dış kanalları, dış depoları ve teslimleri kullanıcıya ya da belgelere sor.
2. **Arketipleri oku:** `${CLAUDE_PLUGIN_ROOT}/roller/*.md`; her dosyanın başındaki "Ne zaman" satırı yeterli.
3. **Öneri tablosu:** Her satırda kanıt (komut çıktısından sayı) ve maliyet bulunur. Altına önerilmeyen ama düşünülen rolleri karşı göstergesiyle yaz. Başlangıç sınırı: ana ajan ve en çok iki rol.
4. **Kapanış önerisi:** Açık roller (`OTURUMLAR.md`) için iki tur boyunca iş almayan var mı bak.
5. **Dur:** Kullanıcı seçmeden rol açma ve kapatma. Seçimden sonra `rol-ac` ya da `rol-kapat`.
