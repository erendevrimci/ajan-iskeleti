"""Kancaların ortak bağlam bulucusu.

Bir oturumun nerede açıldığına bakar ve üç cevaptan birini döner:
- rol klasöründe ise ("rol"),
- iskelet kurulu bir projede ise ("ana"),
- ikisi de değilse None.
İskelet kurulu olmayan her klasörde kancalar hiçbir şey yapmaz.
"""
import json
from pathlib import Path

OTURUM_KAYDI = "iskelet_oturum.json"
PROJE_KAYDI = "iskelet.json"
PROJE_YEREL = "iskelet.local.json"


def _oku(yol):
    try:
        return json.loads(Path(yol).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def bul(cwd):
    p = Path(cwd).resolve()
    zincir = [p, *p.parents]
    # Önce oturum kökü: kod rolünün çalışma ağacında da iskelet.json bulunur, oturum kökü ondan önce gelmeli.
    for d in zincir:
        kayit = _oku(d / OTURUM_KAYDI) if (d / OTURUM_KAYDI).is_file() else None
        if kayit is None:
            continue
        parcalar = p.relative_to(d).parts
        if not parcalar:
            return None  # oturum kökünün kendisi: bir rol klasörü değil
        klasor = parcalar[0]
        for ad, r in (kayit.get("roller") or {}).items():
            if r.get("klasor_adi") == klasor:
                tur = "ana" if r.get("arketip") == "koordinator" else "rol"
                return {"tur": tur, "rol": ad, "bilgi": r, "oturum_kok": str(d), "kayit": kayit}
        # Kayıtta olmayan klasör: en kısıtlı bağlam
        return {"tur": "rol", "rol": klasor, "bilgi": {}, "oturum_kok": str(d), "kayit": kayit}
    for d in zincir:
        if not (d / PROJE_KAYDI).is_file():
            continue
        proje = _oku(d / PROJE_KAYDI) or {}
        yerel = _oku(d / PROJE_YEREL) or {}
        oturum_kok = yerel.get("oturum_kok")
        kayit = _oku(Path(oturum_kok) / OTURUM_KAYDI) if oturum_kok else None
        ana = proje.get("ana_ajan", "ana ajan")
        bilgi = ((kayit or {}).get("roller") or {}).get(ana, {})
        return {"tur": "ana", "rol": ana, "bilgi": bilgi, "oturum_kok": oturum_kok,
                "kayit": kayit, "proje_kok": str(d), "proje": proje}
    return None
