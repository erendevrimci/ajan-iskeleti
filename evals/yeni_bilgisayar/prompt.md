---
runs: 1
max_turns: 90
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, TodoWrite]
expected_outcome: proje/ içinde çekirdek kurulur, oturumlar/ içinde ana ajan ve en çok iki kod rolü açılır, doğrulama HATA 0 verir, commit ya da push yapılmaz.
---

/ajan-iskeleti:kur ana ajan: ŞEF · kullanıcı: Deniz · proje klasörü: ./proje · oturum kökü: ./oturumlar · kanca kipi: yerel (bu ortamda eklenti proje kapsamında kurulamıyor) · sorusuz: amaç "CSV okuyup rapor üreten küçük araç; bitti = testler yeşil"; alan otoritesi yok; kırmızı çizgi: `veri/` klasörü dışarı çıkmaz, push yalnız kullanıcının sözüyle; aynı anda ağır iş: 1. Rol önerisini tabloyla yap, onay verilmiş say ve önerdiğin kod rollerini (en çok iki) `--worktree` olmadan aç. Commit etme. Sonunda doğrulama aracının son satırını göster.
