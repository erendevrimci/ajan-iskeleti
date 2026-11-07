> **DURUM: CANLI** · {{PROJE_ADI}} giriş kapısı · her belge burada bir satırla doğar · {{ANA_AJAN}} yazar

# Buradan başla

**Önem işaretleri:**
- ⭐ her oturumda okunur
- 🟢 canlı kaynak
- 🟠 canlı inceleme ya da karar girdisi
- 🟡 şerhli ya da bayat şüphesi
- 📁 tarihli kayıt

**Kural:** `docs/` altındaki her belge bu tabloda bir satır alır. Yol `docs/`a göre yazılır. `iskelet.py dogrula` eksik satırı hata sayar.

| Belge | Önem | Ne |
|---|---|---|
| `../PLAN.md` | ⭐ | Durum rozeti (tek sayı kaynağı) ve tur günlüğü |
| `BURADAN_BASLA.md` | ⭐ | Bu tablo |
| `DURUM.md` | 🟢 | Sade durum, kullanıcı için |
| `gorevler/KUYRUK.md` | ⭐ | Tek iş kuyruğu ({{KUYRUK_ONEK}}-NNN) |
| `gorevler/ESGUDUM.md` | 🟢 | Roller, dal düzeni, yuva, başlangıç ve bitiş kapıları |
| `VAZGECILENLER.md` | 🟢 | Vazgeçilen yaklaşımlar ve nedenleri |

## Terimler

- **Ana ajan:** koordinatör oturum ({{ANA_AJAN}}).
- **Rol:** uzun ömürlü ayrı oturum; kartı ve seyir defteri oturum kökünde.
- **Yuva:** aynı anda koşabilen ağır iş hakkı (en çok {{YUVA}}).
- **Uç:** bir dalın teslim edilen son commit'i.
- **Birleşim kapısı:** birleşmeden önce koşulan tam kontrol.
