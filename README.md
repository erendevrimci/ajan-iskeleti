> **DURUM: CANLI** · ajan-iskeleti giriş belgesi · sürüm `SURUM` dosyasında

# ajan-iskeleti

Claude Code ile çok oturumlu bir çalışma düzeni kurar: bir **ana ajan** (koordinatör; adını siz verirsiniz) ve projeye göre önerilen **rol oturumları**. Kurallar, canlı belgeler, rol kartları ve kancalar bir istemle projeye yerleşir.

## İki parça

- **İskelet** (bu depo) davranışı taşır: beceriler, kancalar, alt ajan, şablonlar, rol kataloğu, araç.
- **Kurulum** (projede üretilen) durumu taşır: `CLAUDE.md`, canlı belgeler, rol kartları, seyir defterleri.

İskelet hiçbir projenin durumunu taşımaz. Kurulum iskeletin kodunu kopyalamaz; yalnız "yerel kanca" kipinde kancalar ve beceriler projeye kopyalanır.

## Yeni bilgisayarda kurulum

Gerekenler: Claude Code 2.1.224 ya da üstü (oturumlar arası mesajlaşma), git, python3 3.8 ya da üstü.

**Eklentiyle (önerilen).** Proje klasöründe:

```
claude plugin marketplace add <bu deponun yolu ya da git adresi>
claude plugin install ajan-iskeleti@ajan-iskeleti --scope project
claude -n GENEL
> /ajan-iskeleti:kur ana ajan: GENEL
```

**Eklentisiz.** Depoyu klonlayın, proje klasöründe `claude -n GENEL` açıp yazın:

```
<iskelet yolu>/KUR.md'yi oku ve bu projeye kur; ana ajanın adı GENEL; kanca kipi yerel.
```

Ana ajan beş soruluk kısa bir mülakat yapar ve çekirdeği kurar. Sonra projeyi tarayıp kanıtıyla rol önerir. Seçtiğiniz rolleri açar ve her rol için tek satırlık açılış komutu verir. Ayrıntı: `KUR.md`.

## Klasör haritası

| Yol | Ne |
|---|---|
| `KUR.md` | Kurulum akışı; `kur` becerisi bunu yürütür |
| `ILKELER.md` | Anayasa: kurallar ve her birinin gerekçesi |
| `roller/` | Rol arketipleri ve `ROL_ONERME.md` (ne zaman hangi rol) |
| `sablonlar/` | Projeye, oturum köküne ve hafızaya yazılan şablonlar |
| `skills/` | `kur` · `rol-oner` · `rol-ac` · `rol-kapat` · `plan-onayla` · `birlestir` · `tur-kapat` · `devir` · `kit-dogrula` |
| `hooks/` | `git_bekcisi.py` (push, zorla push, dal silme, rolde birleştirme) · `compact_sonrasi.py` (sıkıştırmadan sonra kimlik) |
| `agents/` | `bagimsiz-okuyucu` (salt okuma inceleme) |
| `araclar/iskelet.py` | Kurulumu üreten, rol açan/kapatan, doğrulayan, alan ölçen, seyir katlayan araç |
| `ornek/` | Bu düzenin kaynak projede nasıl göründüğü (anonim) |
| `evals/` | "Yeni bilgisayar" kabul testi |
| `tests/` | Araç ve kanca birim testleri |

## Kurulumun ürettiği düzen

```
<proje>/                         git deposu, ana ajanın çalışma klasörü
├── CLAUDE.md                    proje kuralları (bütçe 8 KB)
├── CLAUDE.local.md              git'e girmez: ana ajanın kartını ve ortak kuralları içe aktarır
├── iskelet.json                 ana ajan adı, yuva sayısı, kuyruk öneki (commit edilir)
├── iskelet.local.json           makineye özgü yollar (git'e girmez)
├── .claude/settings.json        push için onay kuralı, zorla push ve dal silme yasağı
├── PLAN.md                      tek sayı kaynağı ve tur günlüğü
└── docs/ BURADAN_BASLA · DURUM · VAZGECILENLER · gorevler/{KUYRUK, ESGUDUM}
<oturum kökü>/                   proje klasörünün dışında
├── CLAUDE.md                    ortak oturum kuralları (her rol üst klasör olarak yükler)
├── iskelet_oturum.json          rol kaydı
├── OTURUMLAR.md                 adres defteri (araç üretir)
└── <rol>/ CLAUDE.md (rol kartı) · SEYIR.md · kilit.json · (kod rolü) <proje> çalışma ağacı
```

Her rol oturumu kendi klasöründe açılır; Claude Code üst klasörlerin `CLAUDE.md` dosyalarını kendiliğinden yüklediği için rol kartı ve ortak kurallar her turda bağlamdadır. Rol kilidi açılış komutundaki `--settings kilit.json` ile verilir. Çalışma ağacındaki `.claude/settings.local.json` ana klasörün dosyasına çözüldüğü için kilit oraya yazılmaz.

## Sınama

```
python3 -m unittest discover -s tests -v
claude plugin validate .
claude plugin eval . --scaffold --trust-plugin --allow-tools Bash Write Edit --runs 1 --ablation none --no-publish
```

`--no-publish` raporu yerelde tutar; varsayılan davranış raporu claude.ai'ye yayımlamaktır. Eval için git 2.31 ya da üstü gerekir. Kabul testi yerel kanca kipini sınar, çünkü eval koşusu proje ayarlarını okumaz. Eklenti kipinin denetimi birim testlerinde.

## Bilinen sınırlar

- Kancalar ve izin kuralları güvenlik sınırı değildir. Bir betik dosyasının içinden çağrılan `git push` ya da Bash ile dosya yazma kancaya görünmez. Kanca, kuralın unutulmasını önler; kasıtlı aşmayı önlemez.
- Eklenti kipinde, kod dışı rollerin kilidi kanca yollarını eklentinin o anki kurulum yolundan alır. Eklenti güncellenince yol değişir; `iskelet.py dogrula` bunu bildirir, `iskelet.py rol --tazele` yeniler.
- v0.1 yalnız Türkçe.

## Sürüm geçmişi

- **0.1.1 (07.11.2026):** kabul testinin ilk koşusundan. Yarıda kalan kurulum yeniden koşulunca aynı içerikli kopya (`CLAUDE.iskelet.md`) üretilmez, dosya `AYNI` geçer. Yazılamayan dosya (yalıtılmış ortamda `.claude/agents`) kurulumu durdurmaz, `YAZILAMADI` olarak raporlanır. `commit_push_yok` denetçisi yalnız gerçek `git commit` ve `git push` çağrısını sayar; önceki biçim metindeki "gitmez … push" sözünü de yakalıyordu.
- **0.1.0 (07.11.2026):** ilk sürüm. İlkeler, kurulum akışı, yedi arketip, rol önerme yöntemi, şablonlar, dokuz beceri, iki kanca, araç, birim testleri, kabul testi, anonim örnek.
