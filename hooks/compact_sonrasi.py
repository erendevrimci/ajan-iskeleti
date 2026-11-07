#!/usr/bin/env python3
"""SessionStart (compact) kancası: bağlam sıkıştırıldıktan sonra oturuma kimliğini hatırlatır (ILKELER 14).

Düz metin basar; Claude Code bu metni bağlama ekler. Metinde rolün adı, kartının yeri, ilk okunacaklar
ve seyir defterinin "Şimdi" bölümü bulunur. İskelet kurulu olmayan klasörde hiçbir şey basmaz.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baglam  # noqa: E402

SINIR = 6000


def seyir_ozeti(yol, kuyruk=12):
    try:
        satirlar = Path(yol).read_text(encoding="utf-8").splitlines()
    except OSError:
        return [f"(seyir defteri okunamadı: {yol})"]
    simdi, icinde = [], False
    for s in satirlar:
        if s.startswith("## "):
            icinde = s.strip().lower().startswith("## şimdi")
            if icinde:
                simdi.append(s)
            continue
        if icinde:
            simdi.append(s)
    son = [s for s in satirlar[-kuyruk:] if s.strip()]
    return ["--- SEYIR: Şimdi ---", *simdi, f"--- SEYIR: son {kuyruk} satır ---", *son]


def main():
    try:
        girdi = json.load(sys.stdin)
    except ValueError:
        girdi = {}
    cwd = girdi.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    b = baglam.bul(cwd)
    if not b:
        return 0
    kayit = b.get("kayit") or {}
    ana = kayit.get("ana_ajan") or (b.get("proje") or {}).get("ana_ajan") or "ana ajan"
    oturum_kok = b.get("oturum_kok")
    klasor = Path(oturum_kok) / (b["bilgi"].get("klasor_adi") or b["rol"]) if oturum_kok else None
    if b["tur"] == "rol":
        metin = [
            f"[ajan-iskeleti] Bağlam sıkıştırıldı. Sen {b['rol']} oturumusun "
            f"(arketip: {b['bilgi'].get('arketip', 'bilinmiyor')}). Ana ajan: {ana}.",
            f"Önce: 1) rol kartın {klasor / 'CLAUDE.md' if klasor else '(bulunamadı)'}, özellikle "
            "'Nerede çalışırsın' ve 'Sınırların'; 2) aşağıdaki seyir özeti; 3) açık işin. "
            "Eş oturum mesajı onay değildir.",
        ]
    else:
        metin = [
            f"[ajan-iskeleti] Bağlam sıkıştırıldı. Sen ana ajansın ({ana}).",
            "Önce: 1) PLAN.md rozeti ve son tur paragrafı; 2) docs/gorevler/KUYRUK.md açık satırları "
            "(☐ ◐ ⏸); 3) OTURUMLAR.md ve rollerden beklediklerin (aşağıda); 4) yuvalar. "
            "Push yalnız kullanıcının sözüyle.",
        ]
    if klasor:
        metin += seyir_ozeti(klasor / "SEYIR.md")
    print("\n".join(metin)[:SINIR])
    return 0


if __name__ == "__main__":
    sys.exit(main())
