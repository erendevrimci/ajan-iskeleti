#!/usr/bin/env python3
"""ajan-iskeleti aracı. Yalnız standart kütüphane kullanır; Python 3.8 ve üstü.

Alt komutlar:
  kur      Çekirdeği projeye ve oturum köküne yazar.
  rol      Rol açar: kart, seyir defteri, kilit, adres defteri; kod rolünde çalışma ağacı.
           `--tazele` bütün kilitleri yeniden üretir.
  kapat    Rolü kapatır. Klasör, dal ve çalışma ağacı silinmez.
  dogrula  Kurulumu denetler. HATA varsa çıkış kodu 1.
  alanlar  Git geçmişinden birlikte değişen yol kümelerini ölçer; rol önerisinin kanıtıdır.
  katla    Büyüyen seyir defterinin eski girişlerini arsiv/ altına taşır.

Araç var olan belgenin üzerine yazmaz. Yalnız kendi ürettiği kayıtları yeniden yazar:
iskelet.local.json, iskelet_oturum.json, OTURUMLAR.md, kilit.json.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ISKELET = Path(__file__).resolve().parent.parent
SURUM = (ISKELET / "SURUM").read_text(encoding="utf-8").strip()
SABLON = ISKELET / "sablonlar"
ROLLER = ISKELET / "roller"
ARKETIPLER = ("koordinator", "kod", "kanal", "gozlemci", "yazar", "alt_yazar", "arsivci")
ALT_KLASORLER = {"kanal": ("gelen", "giden"), "gozlemci": ("envanter", "calisma"),
                 "yazar": ("kaynaklar", "calisma", "teslim"), "alt_yazar": ("calisma",), "arsivci": ()}
BELGELER = [
    ("PLAN.md", "belgeler/PLAN.md"),
    ("docs/DURUM.md", "belgeler/DURUM.md"),
    ("docs/BURADAN_BASLA.md", "belgeler/BURADAN_BASLA.md"),
    ("docs/VAZGECILENLER.md", "belgeler/VAZGECILENLER.md"),
    ("docs/gorevler/KUYRUK.md", "belgeler/KUYRUK.md"),
    ("docs/gorevler/ESGUDUM.md", "belgeler/ESGUDUM.md"),
]
KANCALAR = ("baglam.py", "git_bekcisi.py", "compact_sonrasi.py")
BANT = re.compile(r"DURUM:\**\s*(CANLI|TARİHLİ|SÜPERSE|BAYAT|KAPANDI|İLETİME HAZIR|GÖNDERİLDİ)")
YER_TUTUCU = re.compile(r"\{\{[A-Z_]+\}\}")
DOLDUR = re.compile(r"<!--\s*DOLDUR:")
AD = re.compile(r"^[A-Za-zÇĞİÖŞÜçğıöşü0-9][A-Za-zÇĞİÖŞÜçğıöşü0-9_-]*$")
CLAUDE_BUTCE = 8 * 1024
SEYIR_ESIK = 100 * 1000
KART_BASLIKLARI = ("## Kimsin", "## Nerede çalışırsın", "## Açılış ve sıkıştırma sonrası", "## Kapanış ölçütü")
HAFIZA_SINIRI = (("## Aktif", 8), ("## Yöntem", 10), ("## Kalıcı", 7))
PUSH_ONAY = "Bash(git push *)"
TR = str.maketrans("ÇĞİIÖŞÜçğıöşü", "CGIIOSUcgiosu")


def bugun():
    return datetime.date.today().strftime("%d.%m.%Y")


def slug(ad):
    return re.sub(r"[^a-z0-9_-]", "_", ad.translate(TR).lower())


def git(*args, cwd, kontrol=True):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)
    if kontrol and r.returncode:
        raise SystemExit(f"HATA: git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def json_oku(yol):
    try:
        return json.loads(Path(yol).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def json_yaz(yol, veri):
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    Path(yol).write_text(json.dumps(veri, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sablon(ad):
    return (SABLON / ad).read_text(encoding="utf-8")


def doldur(metin, d):
    for k, v in d.items():
        metin = metin.replace("{{" + k + "}}", str(v))
    kalan = sorted(set(YER_TUTUCU.findall(metin)))
    if kalan:
        raise SystemExit(f"HATA: şablonda doldurulmamış yer tutucu: {kalan}")
    return metin


class Rapor:
    def __init__(self):
        self.satirlar = []

    def ekle(self, durum, yol, aciklama=""):
        self.satirlar.append((durum, str(yol), aciklama))

    def bas(self):
        for durum, yol, aciklama in self.satirlar:
            print(f"{durum:10} {yol}" + (f"  ({aciklama})" if aciklama else ""))


def yeni_dosya(hedef, metin, rapor, birlestir_adi=None):
    hedef = Path(hedef)
    if hedef.exists():
        if not birlestir_adi:
            rapor.ekle("ATLANDI", hedef, "zaten var")
            return
        hedef = hedef.with_name(birlestir_adi)
        if hedef.exists():
            rapor.ekle("ATLANDI", hedef, "zaten var")
            return
        hedef.write_text(metin, encoding="utf-8")
        rapor.ekle("BİRLEŞTİR", hedef, "asıl dosya zaten var; içe aktar ya da birleştir")
        return
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(metin, encoding="utf-8")
    rapor.ekle("YAZILDI", hedef)


def ayar_birlestir(yol, ek, rapor):
    """settings.json'a izin kurallarını ve kancaları ekler; var olan hiçbir anahtarı silmez."""
    yol = Path(yol)
    var = json_oku(yol) if yol.exists() else {}
    if var is None:
        raise SystemExit(f"HATA: {yol} okunamadı (JSON bozuk); elle düzeltin.")
    izin = var.setdefault("permissions", {})
    for anahtar, kurallar in (ek.get("permissions") or {}).items():
        liste = izin.setdefault(anahtar, [])
        liste += [k for k in kurallar if k not in liste]
    for olay, girdiler in (ek.get("hooks") or {}).items():
        mevcut = var.setdefault("hooks", {}).setdefault(olay, [])
        komutlar = {h.get("command") for g in mevcut for h in g.get("hooks", [])}
        for g in girdiler:
            if not any(h.get("command") in komutlar for h in g.get("hooks", [])):
                mevcut.append(g)
    durum = "BİRLEŞTİ" if yol.exists() else "YAZILDI"
    json_yaz(yol, var)
    rapor.ekle(durum, yol)


def gitignore_ekle(proje, satirlar, rapor):
    yol = proje / ".gitignore"
    metin = yol.read_text(encoding="utf-8") if yol.exists() else ""
    eksik = [s for s in satirlar if s not in metin.splitlines()]
    if not eksik:
        return
    if metin and not metin.endswith("\n"):
        metin += "\n"
    yol.write_text(metin + "# ajan-iskeleti: yerel dosyalar\n" + "\n".join(eksik) + "\n", encoding="utf-8")
    rapor.ekle("BİRLEŞTİ" if metin else "YAZILDI", yol, ", ".join(eksik))


def kanca_ayari(kanca_klasoru, ortam_degiskeni=False):
    def komut(ad):
        if ortam_degiskeni:
            return f'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/{ad}"'
        return f'python3 "{kanca_klasoru}/{ad}"'
    return {
        "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": komut("git_bekcisi.py")}]}],
        "SessionStart": [{"matcher": "compact", "hooks": [{"type": "command",
                                                           "command": komut("compact_sonrasi.py")}]}],
    }


def yerel_kur(proje, rapor):
    """Eklentisiz kip: kancaları, becerileri ve alt ajanı projenin .claude/ klasörüne kopyalar."""
    for ad in KANCALAR:
        yeni_dosya(proje / ".claude/hooks" / ad, (ISKELET / "hooks" / ad).read_text(encoding="utf-8"), rapor)
    for beceri in sorted((ISKELET / "skills").iterdir()):
        if (beceri / "SKILL.md").is_file():
            metin = (beceri / "SKILL.md").read_text(encoding="utf-8").replace("${CLAUDE_PLUGIN_ROOT}", str(ISKELET))
            yeni_dosya(proje / ".claude/skills" / beceri.name / "SKILL.md", metin, rapor)
    for ajan in sorted((ISKELET / "agents").glob("*.md")):
        yeni_dosya(proje / ".claude/agents" / ajan.name, ajan.read_text(encoding="utf-8"), rapor)
    ayar_birlestir(proje / ".claude/settings.json", {"hooks": kanca_ayari(None, ortam_degiskeni=True)}, rapor)


def kart_blogu(arketip, d):
    metin = (ROLLER / f"{arketip}.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- kart:başla -->\n(.*?)<!-- kart:bit -->", metin, re.S)
    if not m:
        raise SystemExit(f"HATA: roller/{arketip}.md kart bloğu yok")
    return doldur(m.group(1).strip(), d)


def rol_karti(d, ad, bilgi, yazma, okuma, kilit, proje_import):
    rd = dict(d, ROL=ad, ARKETIP=bilgi["arketip"], DAL_ONEKI=bilgi["klasor_adi"], UST=bilgi.get("ust") or "—")
    rd.update(CALISMA_KLASORU=bilgi["calisma"], YAZMA_ALANI=yazma, OKUMA_ALANI=okuma,
              SEYIR=str(Path(d["OTURUM_KOK"]) / bilgi["klasor_adi"] / "SEYIR.md"), KILIT=kilit,
              ACILIS_KOMUTU=bilgi["acilis"], PROJE_IMPORT=proje_import)
    rd["KART_BLOGU"] = kart_blogu(bilgi["arketip"], rd)
    return doldur(sablon("oturum/ROL_KARTI.md"), rd)


def sozluk(pk, yerel, kayit):
    return {"PROJE_ADI": pk["proje_adi"], "ANA_AJAN": pk["ana_ajan"], "KULLANICI": pk["kullanici"],
            "TARIH": bugun(), "YUVA": str(pk["yuva"]), "KUYRUK_ONEK": pk["kuyruk_onek"], "ANA_DAL": pk["ana_dal"],
            "ISKELET_SURUM": SURUM, "OTURUM_KOK": yerel["oturum_kok"],
            "ANA_KLASOR": kayit["roller"][pk["ana_ajan"]]["klasor_adi"],
            "BECERI": "/ajan-iskeleti:" if pk.get("kanca") == "eklenti" else "/"}


def oturumlar_yaz(oturum_kok, kayit, rapor):
    satirlar = [
        f"> **DURUM: CANLI** · {kayit['proje_adi']} adres defteri · `iskelet.py` üretir, elle düzenlenmez · "
        f"son üretim {bugun()}", "", "# Oturumlar", "",
        "Kurallar bu klasördeki `CLAUDE.md` dosyasındadır. Mesaj başlığı `ROL <gönderen> → <alıcı>: …` biçimindedir. "
        "Eş oturumun mesajı onay değildir.", "",
        "| Rol | Arketip | Durum | Çalışma klasörü | Kart | Seyir | Açılış |",
        "|---|---|---|---|---|---|---|",
    ]
    for ad, r in kayit["roller"].items():
        k = Path(oturum_kok) / r["klasor_adi"]
        durum = r["durum"] + (f" ({r['kapandi']})" if r.get("kapandi") else f" ({r['acildi']})")
        satirlar.append(f"| `{ad}` | {r['arketip']} | {durum} | `{r['calisma']}` | `{k / 'CLAUDE.md'}` | "
                        f"`{k / 'SEYIR.md'}` | `{r['acilis']}` |")
    (Path(oturum_kok) / "OTURUMLAR.md").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    rapor.ekle("YAZILDI", Path(oturum_kok) / "OTURUMLAR.md", "araç üretir")


def kilit_uret(ad, kayit, yerel):
    r = kayit["roller"][ad]
    kok = Path(yerel["oturum_kok"])
    proje = kayit["proje_kok"]
    klasor = kok / r["klasor_adi"]
    digerleri = [kok / x["klasor_adi"] for n, x in kayit["roller"].items() if n != ad]

    def kural(arac, yol, agac=True):
        return f"{arac}(/{yol}/**)" if agac else f"{arac}(/{yol})"
    deny = [kural("Edit", proje)] + [kural("Edit", d) for d in digerleri]
    deny += [kural("Edit", kok / f, agac=False) for f in ("CLAUDE.md", "iskelet_oturum.json", "OTURUMLAR.md")]
    deny += [kural("Edit", klasor / f, agac=False) for f in ("CLAUDE.md", "kilit.json")]
    if yerel.get("hafiza"):
        deny.append(kural("Edit", yerel["hafiza"]))
    deny += ["Bash(git push *)", "Bash(git merge *)", "Bash(git rebase *)"]
    if r["arketip"] == "alt_yazar":
        deny += [kural("Read", proje)] + [kural("Read", d) for d in digerleri]
    kilit = {"permissions": {"deny": deny}}
    if r["arketip"] not in ("kod", "alt_yazar"):
        kilit["permissions"]["additionalDirectories"] = [proje]
    if r["arketip"] != "kod":
        # Kod dışı rol proje klasöründe çalışmaz; projenin kancaları ona kendiliğinden ulaşmaz.
        if kayit.get("kanca") == "yerel":
            kanca_klasoru = Path(proje) / ".claude/hooks"
        else:
            kanca_klasoru = Path(kayit["iskelet_yolu"]) / "hooks"
        kilit["hooks"] = kanca_ayari(kanca_klasoru)
    return kilit


def kilitleri_tazele(kayit, yerel, rapor):
    for ad, r in kayit["roller"].items():
        if r["arketip"] == "koordinator" or r["durum"] != "açık":
            continue
        yol = Path(yerel["oturum_kok"]) / r["klasor_adi"] / "kilit.json"
        json_yaz(yol, kilit_uret(ad, kayit, yerel))
        rapor.ekle("YAZILDI", yol, "kilit")


def yukle(proje_arg):
    proje = Path(git("rev-parse", "--show-toplevel", cwd=proje_arg)).resolve()
    pk = json_oku(proje / "iskelet.json")
    yerel = json_oku(proje / "iskelet.local.json")
    if not pk or not yerel:
        raise SystemExit("HATA: iskelet.json ya da iskelet.local.json yok; önce `iskelet.py kur`.")
    kayit = json_oku(Path(yerel["oturum_kok"]) / "iskelet_oturum.json")
    if not kayit:
        raise SystemExit("HATA: oturum kökünde iskelet_oturum.json yok.")
    return proje, pk, yerel, kayit


def kalan_doldur(yollar):
    kalan = []
    for y in yollar:
        y = Path(y)
        if y.is_file():
            n = len(DOLDUR.findall(y.read_text(encoding="utf-8")))
            if n:
                kalan.append((y, n))
    return kalan


# ---------------------------------------------------------------- kur

def cmd_kur(a):
    proje = Path(git("rev-parse", "--show-toplevel", cwd=a.proje)).resolve()
    oturum_kok = Path(a.oturum_kok).expanduser().resolve() if a.oturum_kok else proje.parent / f"{proje.name}_oturumlar"
    if oturum_kok == proje or proje in oturum_kok.parents:
        raise SystemExit("HATA: oturum kökü proje klasörünün içinde olamaz (çalışma ağaçları projenin içine açılmaz).")
    if (proje / "iskelet.json").exists():
        raise SystemExit("HATA: iskelet.json zaten var; bu proje kurulu. Denetim için `iskelet.py dogrula`.")
    ana = a.ana_ajan
    if not AD.match(ana):
        raise SystemExit(f"HATA: geçersiz ad: {ana!r}")
    ana_dal = a.ana_dal or git("symbolic-ref", "--short", "HEAD", cwd=proje, kontrol=False) or "main"
    tarih = bugun()
    hafiza = Path(a.hafiza).expanduser().resolve() if a.hafiza else None
    r = Rapor()

    pk = {"iskelet_surum": SURUM, "proje_adi": a.proje_adi or proje.name, "ana_ajan": ana, "kullanici": a.kullanici,
          "yuva": a.yuva, "kuyruk_onek": a.kuyruk_onek, "ana_dal": ana_dal, "kanca": a.kanca, "kuruldu": tarih}
    yerel = {"oturum_kok": str(oturum_kok), "iskelet_yolu": str(ISKELET), "hafiza": str(hafiza) if hafiza else None}
    json_yaz(proje / "iskelet.local.json", yerel)
    r.ekle("YAZILDI", proje / "iskelet.local.json", "makineye özgü, git'e girmez")
    gitignore_ekle(proje, ["CLAUDE.local.md", "iskelet.local.json"], r)

    oturum_kok.mkdir(parents=True, exist_ok=True)
    kayit = {"proje_adi": pk["proje_adi"], "ana_ajan": ana, "kullanici": a.kullanici, "proje_kok": str(proje),
             "iskelet_yolu": str(ISKELET), "kanca": a.kanca, "roller": {}}
    kayit["roller"][ana] = {"arketip": "koordinator", "klasor_adi": slug(ana), "durum": "açık", "acildi": tarih,
                            "calisma": str(proje), "acilis": f'cd "{proje}" && claude -n {ana}'}
    d = sozluk(pk, yerel, kayit)

    yeni_dosya(proje / "CLAUDE.md", doldur(sablon("proje/CLAUDE.md"), d), r, birlestir_adi="CLAUDE.iskelet.md")
    yeni_dosya(proje / "CLAUDE.local.md", doldur(sablon("proje/CLAUDE.local.md"), d), r,
               birlestir_adi="CLAUDE.local.iskelet.md")
    for hedef, ad in BELGELER:
        yeni_dosya(proje / hedef, doldur(sablon(ad), d), r)
    ayar_birlestir(proje / ".claude/settings.json", json.loads(sablon("proje/settings.json")), r)
    if a.kanca == "yerel":
        yerel_kur(proje, r)

    yeni_dosya(oturum_kok / "CLAUDE.md", doldur(sablon("oturum/ORTAK_CLAUDE.md"), d), r)
    bilgi = kayit["roller"][ana]
    kart = rol_karti(d, ana, bilgi,
                     yazma="ana dal; canlı belgeler (`PLAN.md`, `docs/**`); kurallar (`CLAUDE.md`, `.claude/**`, "
                           "`iskelet.json`); hafıza; oturum kökündeki kayıtlar",
                     okuma="proje, oturum kökü, salt okunur dış depolar",
                     kilit="yok; ana ajan proje ayarlarıyla çalışır", proje_import="")
    klasor = oturum_kok / bilgi["klasor_adi"]
    yeni_dosya(klasor / "CLAUDE.md", kart, r)
    yeni_dosya(klasor / "SEYIR.md", doldur(sablon("oturum/SEYIR.md"), dict(d, ROL=ana)), r)
    json_yaz(oturum_kok / "iskelet_oturum.json", kayit)
    r.ekle("YAZILDI", oturum_kok / "iskelet_oturum.json", "rol kaydı")
    oturumlar_yaz(oturum_kok, kayit, r)
    if hafiza:
        yeni_dosya(hafiza / "MEMORY.md", doldur(sablon("hafiza/MEMORY.md"), d), r)
    json_yaz(proje / "iskelet.json", pk)  # en son: yarım kalan kurulum yeniden koşulabilsin
    r.ekle("YAZILDI", proje / "iskelet.json")

    r.bas()
    kalan = kalan_doldur([proje / "CLAUDE.md", proje / "CLAUDE.iskelet.md", proje / "PLAN.md",
                          proje / "docs/DURUM.md", klasor / "CLAUDE.md"])
    print("\nDoldurulacak boşluklar:" if kalan else "\nDoldurulacak boşluk yok.")
    for y, n in kalan:
        print(f"  {y}: {n}")
    print(f"\nSonraki: boşlukları doldur → rol önerisi (`iskelet.py alanlar --proje {proje}`) → "
          f"`iskelet.py dogrula --proje {proje}`.")
    if a.kanca == "eklenti":
        print("Eklenti kipi: `claude plugin install ajan-iskeleti@ajan-iskeleti --scope project` koşulmuş olmalı.")
    return 0


# ---------------------------------------------------------------- rol

def cmd_rol(a):
    proje, pk, yerel, kayit = yukle(a.proje)
    r = Rapor()
    if a.tazele:
        kayit["iskelet_yolu"] = str(ISKELET)
        json_yaz(Path(yerel["oturum_kok"]) / "iskelet_oturum.json", kayit)
        kilitleri_tazele(kayit, yerel, r)
        r.bas()
        return 0
    if not a.ad or not a.arketip:
        raise SystemExit("HATA: --ad ve --arketip gerekli (ya da --tazele).")
    ad, arketip = a.ad, a.arketip
    if not AD.match(ad):
        raise SystemExit(f"HATA: geçersiz ad: {ad!r}")
    if ad in kayit["roller"]:
        raise SystemExit(f"HATA: {ad} kayıtta zaten var ({kayit['roller'][ad]['durum']}).")
    if arketip == "kod" and not a.alan:
        raise SystemExit("HATA: kod rolü en az bir --alan (pathspec) ister.")
    if arketip == "alt_yazar" and (not a.ust or a.ust not in kayit["roller"]):
        raise SystemExit("HATA: alt yazar, kayıtlı bir üst rol ister (--ust).")
    kok = Path(yerel["oturum_kok"])
    klasor_adi = slug(ad)
    if any(x["klasor_adi"] == klasor_adi for x in kayit["roller"].values()):
        raise SystemExit(f"HATA: {klasor_adi} klasör adı başka bir rolde kullanılıyor.")
    klasor = kok / klasor_adi
    tarih = bugun()
    kilit = klasor / "kilit.json"
    bilgi = {"arketip": arketip, "klasor_adi": klasor_adi, "durum": "açık", "acildi": tarih,
             "alan": a.alan or [], "okuma": a.okuma or [], "ust": a.ust}
    if arketip == "kod":
        calisma = klasor / proje.name
        dal = f"{klasor_adi}/baslangic_{datetime.date.today():%Y%m%d}"
        bilgi["dal"] = dal
        if a.worktree:
            if calisma.exists():
                raise SystemExit(f"HATA: {calisma} zaten var.")
            klasor.mkdir(parents=True, exist_ok=True)
            git("worktree", "add", "-b", dal, str(calisma), pk["ana_dal"], cwd=proje)
            r.ekle("YAZILDI", calisma, f"çalışma ağacı, dal {dal}")
        yazma = ", ".join(f"`{x}`" for x in a.alan) + " (çalışma ağacında, kendi dalında)"
        okuma = "proje (çalışma ağacı)" + "".join(f", `{x}`" for x in a.okuma or [])
        proje_import = ""
    else:
        calisma = klasor
        yazma = f"`{klasor}/**` (kendi klasörün)" + "".join(f", `{x}`" for x in a.alan or [])
        if arketip == "alt_yazar":
            okuma = "yalnız kendi klasörün" + "".join(f", `{x}`" for x in a.okuma or [])
            proje_import = ""
        else:
            okuma = f"proje (`{proje}`, salt okuma)" + "".join(f", `{x}`" for x in a.okuma or [])
            proje_import = f"\nProje kuralları: @{proje}/CLAUDE.md\n"
    bilgi["calisma"] = str(calisma)
    bilgi["acilis"] = (f'cd "{calisma}" && claude -n {ad} --settings "{kilit}" '
                       f'"Rol kartını ve SEYIR.md dosyasını oku; ana ajana ({pk["ana_ajan"]}) hazır olduğunu yaz."')
    kayit["roller"][ad] = bilgi
    d = sozluk(pk, yerel, kayit)

    klasor.mkdir(parents=True, exist_ok=True)
    for alt in ALT_KLASORLER.get(arketip, ()):
        (klasor / alt).mkdir(exist_ok=True)
    yeni_dosya(klasor / "CLAUDE.md", rol_karti(d, ad, bilgi, yazma, okuma, str(kilit), proje_import), r)
    yeni_dosya(klasor / "SEYIR.md", doldur(sablon("oturum/SEYIR.md"), dict(d, ROL=ad)), r)
    json_yaz(kok / "iskelet_oturum.json", kayit)
    r.ekle("YAZILDI", kok / "iskelet_oturum.json", "rol kaydı")
    kilitleri_tazele(kayit, yerel, r)
    oturumlar_yaz(kok, kayit, r)
    r.bas()
    if arketip == "kod" and not a.worktree:
        print(f"\nÇalışma ağacı açılmadı. Kurulum commit edildikten sonra:\n"
              f"  git -C \"{proje}\" worktree add -b {bilgi['dal']} \"{calisma}\" {pk['ana_dal']}")
    print(f"\nKartta doldurulacak boşluklar: {len(DOLDUR.findall((klasor / 'CLAUDE.md').read_text(encoding='utf-8')))}")
    print(f"Açılış komutu (kullanıcı yeni bir terminalde koşar):\n  {bilgi['acilis']}")
    return 0


def cmd_kapat(a):
    proje, pk, yerel, kayit = yukle(a.proje)
    r = Rapor()
    bilgi = kayit["roller"].get(a.ad)
    if not bilgi or bilgi["arketip"] == "koordinator":
        raise SystemExit(f"HATA: {a.ad} kapatılabilir bir rol değil.")
    if bilgi["durum"] != "açık":
        raise SystemExit(f"HATA: {a.ad} zaten {bilgi['durum']}.")
    bilgi["durum"], bilgi["kapandi"] = "kapalı", bugun()
    kart = Path(yerel["oturum_kok"]) / bilgi["klasor_adi"] / "CLAUDE.md"
    if kart.exists():
        satirlar = kart.read_text(encoding="utf-8").split("\n")
        satirlar[0] = satirlar[0].replace("DURUM: CANLI", f"DURUM: KAPANDI-TARİHLİ ({bilgi['kapandi']})", 1)
        kart.write_text("\n".join(satirlar), encoding="utf-8")
        r.ekle("BANT", kart, "KAPANDI-TARİHLİ")
    kok = Path(yerel["oturum_kok"])
    json_yaz(kok / "iskelet_oturum.json", kayit)
    kilitleri_tazele(kayit, yerel, r)
    oturumlar_yaz(kok, kayit, r)
    r.bas()
    print("\nKlasör, dal ve çalışma ağacı yerinde kaldı. Çalışma ağacını kaldırmak kullanıcının kararıdır.")
    return 0


# ---------------------------------------------------------------- dogrula

def _eklenti_etkin(proje):
    for yol in (proje / ".claude/settings.json", proje / ".claude/settings.local.json",
                Path.home() / ".claude/settings.json"):
        ep = (json_oku(yol) or {}).get("enabledPlugins") or {}
        if any(k.split("@")[0] == "ajan-iskeleti" and v for k, v in ep.items()):
            return True
    return False


def cmd_dogrula(a):
    H, U = [], []
    proje = Path(git("rev-parse", "--show-toplevel", cwd=a.proje)).resolve()
    pk = json_oku(proje / "iskelet.json")
    if not pk:
        print("HATA: iskelet.json yok ya da bozuk.\nHATA: 1 · UYARI: 0")
        return 1
    yerel = json_oku(proje / "iskelet.local.json") or {}
    if not yerel:
        H.append("iskelet.local.json yok (makineye özgü yollar).")
    kok = Path(yerel["oturum_kok"]) if yerel.get("oturum_kok") else None

    cm, ci = proje / "CLAUDE.md", proje / "CLAUDE.iskelet.md"
    talimat = ci if ci.exists() else cm
    if not talimat.exists():
        H.append("CLAUDE.md yok.")
    else:
        boyut = talimat.stat().st_size
        if boyut > CLAUDE_BUTCE:
            U.append(f"{talimat.name} {boyut} bayt; bütçe {CLAUDE_BUTCE}. Ayrıntıyı belgeye taşı.")
    if ci.exists() and "@CLAUDE.iskelet.md" not in (cm.read_text(encoding="utf-8") if cm.exists() else ""):
        U.append("CLAUDE.iskelet.md var ama CLAUDE.md onu içe aktarmıyor ve birleştirilmemiş.")
    gi = (proje / ".gitignore").read_text(encoding="utf-8").splitlines() if (proje / ".gitignore").exists() else []
    for s in ("CLAUDE.local.md", "iskelet.local.json"):
        if s not in gi:
            H.append(f".gitignore'da {s} yok.")
    yerel_talimat = proje / "CLAUDE.local.md"
    if not yerel_talimat.exists() or (kok and str(kok) not in yerel_talimat.read_text(encoding="utf-8")):
        H.append("CLAUDE.local.md yok ya da oturum kökündeki kartları içe aktarmıyor.")

    uretilen = [talimat, yerel_talimat, *[proje / h for h, _ in BELGELER]]
    belgeler = [proje / "PLAN.md"] + sorted(p for p in (proje / "docs").rglob("*.md") if "arsiv" not in p.parts) \
        if (proje / "docs").is_dir() else [proje / "PLAN.md"]
    for b in belgeler:
        if not b.exists():
            H.append(f"{b.relative_to(proje)} yok.")
            continue
        bas = "\n".join(b.read_text(encoding="utf-8").splitlines()[:5])
        if not BANT.search(bas):
            H.append(f"{b.relative_to(proje)}: ilk beş satırda DURUM bandı yok.")
    bb = proje / "docs/BURADAN_BASLA.md"
    if bb.exists():
        bbm = bb.read_text(encoding="utf-8")
        for b in belgeler[1:]:
            goreli = b.relative_to(proje / "docs").as_posix()
            if f"`{goreli}`" not in bbm:
                H.append(f"docs/{goreli}: BURADAN_BASLA'da satırı yok.")

    ayar = json_oku(proje / ".claude/settings.json") or {}
    if PUSH_ONAY not in (ayar.get("permissions") or {}).get("ask", []):
        H.append(f".claude/settings.json: push onay kuralı ({PUSH_ONAY}) yok.")
    if pk.get("kanca") == "yerel":
        for ad in KANCALAR:
            if not (proje / ".claude/hooks" / ad).exists():
                H.append(f".claude/hooks/{ad} yok.")
        komutlar = json.dumps(ayar.get("hooks") or {})
        for ad in ("git_bekcisi.py", "compact_sonrasi.py"):
            if ad not in komutlar:
                H.append(f".claude/settings.json: {ad} kancası kayıtlı değil.")
    elif not _eklenti_etkin(proje):
        H.append("Eklenti etkin değil: `claude plugin install ajan-iskeleti@ajan-iskeleti --scope project`.")

    kuyruk = proje / "docs/gorevler/KUYRUK.md"
    if kuyruk.exists():
        onek = re.escape(pk.get("kuyruk_onek", "IS"))
        satirlar = [s for s in kuyruk.read_text(encoding="utf-8").splitlines()
                    if re.match(rf"^\| (✅ )?\*\*{onek}-", s)]
        gorulen = set()
        for s in satirlar:
            m = re.match(rf"^\| (?:✅ )?\*\*({onek}-\d+)\*\* \|", s)
            if not m or len(s.split("|")) != 9:
                H.append(f"KUYRUK satırı biçimsiz: {s[:60]}")
                continue
            if m.group(1) in gorulen:
                H.append(f"KUYRUK: {m.group(1)} iki kez.")
            gorulen.add(m.group(1))

    if kok:
        if kok == proje or proje in kok.parents:
            H.append("Oturum kökü proje klasörünün içinde.")
        for f in ("CLAUDE.md", "iskelet_oturum.json", "OTURUMLAR.md"):
            if not (kok / f).exists():
                H.append(f"oturum kökünde {f} yok.")
        kayit = json_oku(kok / "iskelet_oturum.json") or {"roller": {}}
        adres = (kok / "OTURUMLAR.md").read_text(encoding="utf-8") if (kok / "OTURUMLAR.md").exists() else ""
        if pk["ana_ajan"] not in kayit["roller"]:
            H.append("Ana ajan rol kaydında yok.")
        uretilen.append(kok / "CLAUDE.md")
        for ad, r in kayit["roller"].items():
            if r["durum"] != "açık":
                continue
            k = kok / r["klasor_adi"]
            kart, seyir = k / "CLAUDE.md", k / "SEYIR.md"
            uretilen += [kart, seyir]
            if f"| `{ad}` |" not in adres:
                H.append(f"{ad}: OTURUMLAR.md'de yok.")
            if not kart.exists():
                H.append(f"{ad}: rol kartı yok ({kart}).")
            else:
                metin = kart.read_text(encoding="utf-8")
                for baslik in KART_BASLIKLARI:
                    if baslik not in metin:
                        H.append(f"{ad}: kartta '{baslik}' bölümü yok.")
            if not seyir.exists() or "## Şimdi" not in seyir.read_text(encoding="utf-8"):
                H.append(f"{ad}: SEYIR.md yok ya da '## Şimdi' bölümü yok.")
            elif seyir.stat().st_size > SEYIR_ESIK:
                U.append(f"{ad}: SEYIR.md {seyir.stat().st_size} bayt; `iskelet.py katla`.")
            if r["arketip"] == "koordinator":
                continue
            kilit = json_oku(k / "kilit.json")
            if not kilit:
                H.append(f"{ad}: kilit.json yok ya da bozuk.")
            else:
                for olay in (kilit.get("hooks") or {}).values():
                    for g in olay:
                        for h in g.get("hooks", []):
                            m = re.search(r'"([^"]+\.py)"', h.get("command", ""))
                            if m and not Path(m.group(1)).exists():
                                H.append(f"{ad}: kilitteki kanca yolu yok ({m.group(1)}); `iskelet.py rol --tazele`.")
            if r["arketip"] == "kod" and not Path(r["calisma"]).exists():
                U.append(f"{ad}: çalışma ağacı açılmamış ({r['calisma']}).")

    for y in uretilen:
        if Path(y).is_file():
            kalan = sorted(set(YER_TUTUCU.findall(Path(y).read_text(encoding="utf-8"))))
            if kalan:
                H.append(f"{y}: doldurulmamış yer tutucu {kalan}.")
    for y, n in kalan_doldur(uretilen):
        U.append(f"{y}: {n} DOLDUR boşluğu.")

    if yerel.get("hafiza"):
        mem = Path(yerel["hafiza"]) / "MEMORY.md"
        if mem.exists():
            bolum, sayac = None, {}
            for s in mem.read_text(encoding="utf-8").splitlines():
                if s.startswith("## "):
                    bolum = next((b for b, _ in HAFIZA_SINIRI if s.startswith(b)), None)
                elif bolum and s.startswith("- "):
                    sayac[bolum] = sayac.get(bolum, 0) + 1
                    if len(s) > 200:
                        U.append(f"MEMORY.md satırı 200 karakteri aşıyor: {s[:50]}…")
            for b, sinir in HAFIZA_SINIRI:
                if sayac.get(b, 0) > sinir:
                    U.append(f"MEMORY.md '{b}' bölümü {sayac[b]} satır; sınır {sinir}.")

    for h in H:
        print("HATA:", h)
    for u in U:
        print("UYARI:", u)
    print(f"HATA: {len(H)} · UYARI: {len(U)}")
    return 1 if H else 0


# ---------------------------------------------------------------- alanlar

def _alan(dosya, derinlik):
    parca = dosya.split("/")
    if len(parca) == 1:
        return "(kök)"
    return "/".join(parca[:min(derinlik, len(parca) - 1)])


def cmd_alanlar(a):
    proje = Path(git("rev-parse", "--show-toplevel", cwd=a.proje)).resolve()
    cikti = git("log", f"--since={a.gun} days ago", "--name-only", "--pretty=format:@@", cwd=proje, kontrol=False)
    commitler = [{_alan(f, a.derinlik) for f in blok.splitlines() if f.strip()} for blok in cikti.split("@@")]
    commitler = [c for c in commitler if c]
    dosyalar = {}
    for blok in cikti.split("@@"):
        for f in blok.splitlines():
            if f.strip():
                dosyalar.setdefault(_alan(f, a.derinlik), set()).add(f)
    dokunan = {}
    for i, c in enumerate(commitler):
        for alan in c:
            dokunan.setdefault(alan, set()).add(i)
    testler = [f for fs in dosyalar.values() for f in fs if re.search(r"(^|/)(tests?|spec)/|test_|_test\.", f)]
    sirali = sorted(dokunan, key=lambda x: -len(dokunan[x]))[:a.en]
    print(f"Son {a.gun} gün, {len(commitler)} commit, derinlik {a.derinlik}. Eş-değişim = iki alanın birlikte "
          "değiştiği commit'lerin, herhangi birinin değiştiği commit'lere oranı.\n")
    print("| Alan | Commit | Dosya | En yakın alan (eş-değişim) | Ad eşleşen test dosyası |")
    print("|---|---|---|---|---|")
    for alan in sirali:
        A = dokunan[alan]
        en, oran = "—", 0.0
        for diger, B in dokunan.items():
            if diger != alan:
                j = len(A & B) / len(A | B)
                if j > oran:
                    en, oran = diger, j
        ad = alan.rsplit("/", 1)[-1]
        test = sum(1 for f in testler if ad != "(kök)" and ad in f.rsplit("/", 1)[-1])
        print(f"| `{alan}` | {len(A)} | {len(dosyalar.get(alan, ()))} | `{en}` ({oran:.2f}) | {test} |")
    return 0


# ---------------------------------------------------------------- katla

def cmd_katla(a):
    yol = Path(a.dosya).resolve()
    metin = yol.read_text(encoding="utf-8")
    boyut = len(metin.encode("utf-8"))
    if boyut <= a.esik:
        print(f"Gerek yok: {boyut} bayt ≤ {a.esik}.")
        return 0
    satirlar = metin.splitlines(keepends=True)
    gunluk = next((i for i, s in enumerate(satirlar) if s.startswith("## Günlük")), None)
    if gunluk is None:
        raise SystemExit("HATA: '## Günlük' bölümü yok; dosya yapısı tanınmadı.")
    bas, govde = satirlar[:gunluk + 1], satirlar[gunluk + 1:]
    hedef, toplam, kes = a.esik // 2, 0, len(govde)
    for i in range(len(govde) - 1, -1, -1):
        toplam += len(govde[i].encode("utf-8"))
        if toplam > hedef:
            break
        if govde[i].startswith(("- ", "### ")):
            kes = i
    eski, yeni = govde[:kes], govde[kes:]
    if not "".join(eski).strip():
        print("Katlanacak giriş yok.")
        return 0
    arsiv_klasoru = yol.parent / "arsiv"
    arsiv_klasoru.mkdir(exist_ok=True)
    taban = f"{yol.stem}_arsiv_{datetime.date.today():%Y%m%d}"
    arsiv, n = arsiv_klasoru / f"{taban}.md", 2
    while arsiv.exists():
        arsiv, n = arsiv_klasoru / f"{taban}_{n}.md", n + 1
    arsiv.write_text(f"> **DURUM: TARİHLİ KAYIT** · {yol.name} katlaması · {bugun()} · HALEF: `../{yol.name}`\n\n"
                     + "".join(eski), encoding="utf-8")
    yol.write_text("".join(bas) + f"- ({bugun()}) eski girişler: `arsiv/{arsiv.name}`\n" + "".join(yeni),
                   encoding="utf-8")
    print(f"Katlandı: {boyut} → {yol.stat().st_size} bayt; eski girişler {arsiv}.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="iskelet.py", description=__doc__.split("\n")[0])
    alt = p.add_subparsers(dest="komut", required=True)

    k = alt.add_parser("kur", help="çekirdeği kur")
    k.add_argument("--proje", default=".")
    k.add_argument("--ana-ajan", required=True)
    k.add_argument("--kullanici", required=True)
    k.add_argument("--oturum-kok")
    k.add_argument("--proje-adi")
    k.add_argument("--yuva", type=int, default=2)
    k.add_argument("--kuyruk-onek", default="IS")
    k.add_argument("--ana-dal")
    k.add_argument("--kanca", choices=("eklenti", "yerel"), default="eklenti")
    k.add_argument("--hafiza", help="ana ajanın hafıza klasörü (MEMORY.md tohumu)")
    k.set_defaults(f=cmd_kur)

    r = alt.add_parser("rol", help="rol aç ya da kilitleri tazele")
    r.add_argument("--proje", default=".")
    r.add_argument("--ad")
    r.add_argument("--arketip", choices=[x for x in ARKETIPLER if x != "koordinator"])
    r.add_argument("--alan", action="append", help="yazma alanı (pathspec); tekrarlanabilir")
    r.add_argument("--okuma", action="append", help="ek okuma yolu; tekrarlanabilir")
    r.add_argument("--ust", help="alt yazarın üst rolü")
    r.add_argument("--worktree", action="store_true", help="kod rolü: çalışma ağacını ve dalı aç")
    r.add_argument("--tazele", action="store_true", help="bütün açık rollerin kilitlerini yeniden üret")
    r.set_defaults(f=cmd_rol)

    c = alt.add_parser("kapat", help="rolü kapat")
    c.add_argument("--proje", default=".")
    c.add_argument("--ad", required=True)
    c.set_defaults(f=cmd_kapat)

    d = alt.add_parser("dogrula", help="kurulumu denetle")
    d.add_argument("--proje", default=".")
    d.set_defaults(f=cmd_dogrula)

    al = alt.add_parser("alanlar", help="birlikte değişen yol kümeleri")
    al.add_argument("--proje", default=".")
    al.add_argument("--gun", type=int, default=120)
    al.add_argument("--derinlik", type=int, default=2)
    al.add_argument("--en", type=int, default=15)
    al.set_defaults(f=cmd_alanlar)

    kt = alt.add_parser("katla", help="seyir defterini katla")
    kt.add_argument("--dosya", required=True)
    kt.add_argument("--esik", type=int, default=SEYIR_ESIK)
    kt.set_defaults(f=cmd_katla)

    a = p.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
