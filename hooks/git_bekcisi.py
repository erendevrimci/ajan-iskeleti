#!/usr/bin/env python3
"""PreToolUse (Bash) kancası: git kurallarını uygular.

Kurallar (ILKELER 4 ve 5):
- Zorla push, uzakta dal silme ve yerel dal silme: herkese yasak.
- Rol oturumu: push, merge ve rebase yasak.
- Ana ajan: push yalnız düz biçimde (`git push <uzak> <dal>`, tek başına) ve kullanıcı onayıyla.
  Düz biçim, projenin `Bash(git push *)` onay kuralına da takılır. O kural her izin kipinde sorar.

Kanca, kuralın unutulmasını önler; kasıtlı aşmayı önlemez. Örneğin bir betik dosyasının içinden
çağrılan git kancaya görünmez. İskelet kurulu olmayan klasörde hiçbir şey yapmaz.
"""
import json
import os
import re
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baglam  # noqa: E402

KABUKLAR = {"sh", "bash", "zsh", "dash", "ksh"}
ONEKLER = {"env", "command", "builtin", "exec", "nohup", "time", "sudo", "nice", "xargs", "caffeinate", "timeout"}
GIT_ARGLI = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env", "--super-prefix"}
GIT_KOMUTLARI = {
    "add", "am", "apply", "archive", "bisect", "blame", "branch", "bundle", "checkout", "cherry", "cherry-pick",
    "clean", "clone", "commit", "config", "describe", "diff", "difftool", "fetch", "format-patch", "fsck", "gc",
    "grep", "help", "init", "log", "ls-files", "ls-remote", "ls-tree", "merge", "merge-base", "mv", "notes",
    "pull", "push", "range-diff", "rebase", "reflog", "remote", "reset", "restore", "rev-list", "rev-parse",
    "revert", "rm", "shortlog", "show", "show-ref", "stash", "status", "submodule", "switch", "symbolic-ref",
    "tag", "update-ref", "worktree", "cat-file", "for-each-ref", "name-rev", "var", "version",
}
SUPHELI = re.compile(r"\bgit\b.*\b(push|branch|merge|rebase|update-ref)\b", re.S)
AGIRLIK = {None: 0, "ask": 1, "deny": 2}


def _jetonlar(metin):
    lx = shlex.shlex(metin, posix=True, punctuation_chars=";&|()")
    lx.whitespace_split = True
    return list(lx)


def parcala(komut, derinlik=0):
    """Komutu basit komutlara böler. $(...), `...`, `sh -c` ve eval içlerini de açar. Ayrıştıramazsa None döner."""
    if derinlik > 4:
        return []
    parcalar = []
    for ic in re.findall(r"\$\(([^()]*)\)", komut) + re.findall(r"`([^`]*)`", komut):
        alt = parcala(ic, derinlik + 1)
        if alt is None:
            return None
        parcalar += alt
    try:
        jetonlar = _jetonlar(komut.replace("\n", " ; "))
    except ValueError:
        return None
    simdiki = []
    for j in jetonlar:
        if j and set(j) <= set(";&|()"):
            if simdiki:
                parcalar.append(simdiki)
            simdiki = []
        else:
            simdiki.append(j)
    if simdiki:
        parcalar.append(simdiki)
    ek = []
    for p in list(parcalar):
        govde = _govde(p)
        if not govde:
            continue
        ad = os.path.basename(govde[0])
        if ad in KABUKLAR:
            for i, t in enumerate(govde[1:], 1):
                if re.match(r"^-[a-zA-Z]*c[a-zA-Z]*$", t) and i + 1 < len(govde):
                    alt = parcala(govde[i + 1], derinlik + 1)
                    if alt is None:
                        return None
                    ek += alt
                    break
        elif ad == "eval":
            alt = parcala(" ".join(govde[1:]), derinlik + 1)
            if alt is None:
                return None
            ek += alt
    return parcalar + ek


def _govde(p):
    """Ortam atamalarını atlar. Komut bir önek komutuysa (env, sudo, xargs...) içindeki git'i bulur."""
    i = 0
    while i < len(p) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", p[i]):
        i += 1
    p = p[i:]
    if p and os.path.basename(p[0]) in ONEKLER:
        for k, t in enumerate(p[1:], 1):
            if os.path.basename(t) in ({"git", "eval"} | KABUKLAR):
                return p[k:]
        return []
    return p


def _alias(ad, cwd):
    try:
        r = subprocess.run(["git", "config", "--get", "alias." + ad], cwd=cwd, capture_output=True,
                           text=True, timeout=3)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() or None


def git_cagrilari(komut, cwd, derinlik=0):
    """Komuttaki her git çağrısı için (alt komut, argümanlar, düz mü) döner. Ayrıştıramazsa None döner."""
    parcalar = parcala(komut)
    if parcalar is None:
        return None
    tek = len(parcalar) == 1
    sonuc = []
    for ham in parcalar:
        govde = _govde(ham)
        if not govde or os.path.basename(govde[0]) != "git":
            continue
        i, globalli = 1, False
        while i < len(govde) and govde[i].startswith("-"):
            globalli = True
            i += 2 if govde[i] in GIT_ARGLI else 1
        if i >= len(govde):
            continue
        alt, argumanlar = govde[i], govde[i + 1:]
        if alt not in GIT_KOMUTLARI and derinlik < 3:
            deger = _alias(alt, cwd)
            if deger:
                yeni = (deger[1:] if deger.startswith("!") else "git " + deger) + " " + " ".join(
                    shlex.quote(a) for a in argumanlar)
                ic = git_cagrilari(yeni, cwd, derinlik + 1)
                if ic is None:
                    return None
                sonuc += [(a, g, False) for a, g, _ in ic]
                continue
        duz = tek and ham[0] == "git" and not globalli and derinlik == 0
        sonuc.append((alt, argumanlar, duz))
    return sonuc


def _kisa_bayrak(a, harfler):
    return bool(re.match(r"^-[a-zA-Z]*[" + harfler + "]", a)) and not a.startswith("--")


def karar(alt, args, duz, tur):
    if alt == "push":
        if any(a in ("--force", "--mirror", "--force-if-includes") or a.startswith("--force-with-lease")
               or _kisa_bayrak(a, "f") or (a.startswith("+") and len(a) > 1) for a in args):
            return "deny", "Zorla push yasak (ILKELER 5)."
        if any(a in ("--delete", "--prune") or _kisa_bayrak(a, "d") or (a.startswith(":") and len(a) > 1)
               for a in args):
            return "deny", "Uzakta dal silme yasak; kapanan iş dalı kalır (ILKELER 5)."
        if tur == "rol":
            return "deny", ("Rol oturumu push etmez. Birleştirme ve push ana ajanın işidir; push da yalnız "
                            "kullanıcının sözüyle olur (ILKELER 4, 5).")
        if not duz:
            return "deny", ("push'u tek başına ve düz biçimde yaz: `git push <uzak> <dal>`. Başka komutla "
                            "zincirleme, -C ya da takma ad kullanma. Düz biçim kullanıcı onayı ister.")
        return "ask", "Push yalnız kullanıcının sözüyle (ILKELER 5). Kullanıcı açıkça istediyse onaylayın."
    if alt == "branch" and any(a == "--delete" or _kisa_bayrak(a, "dD") for a in args):
        return "deny", "Dal silme yasak; kapanan iş dalı kalır (ILKELER 5)."
    if alt == "update-ref" and any(a == "-d" or a == "--stdin" for a in args):
        return "deny", "update-ref ile dal silme yasak (ILKELER 5)."
    if tur == "rol" and alt in ("merge", "rebase"):
        return "deny", (f"Rol oturumu {alt} yapmaz. Yeni iş için ana dalın ucundan yeni dal aç; birleştirmeyi "
                        "ana ajan yapar (ILKELER 4).")
    return None, None


def degerlendir(komut, cwd):
    b = baglam.bul(cwd)
    if not b:
        return None, None
    cagrilar = git_cagrilari(komut, cwd)
    if cagrilar is None:
        if SUPHELI.search(komut):
            return "deny", "Komut ayrıştırılamadı (tırnak dengesiz olabilir). git komutunu düz ve tek başına yaz."
        return None, None
    en, neden = None, None
    for alt, args, duz in cagrilar:
        k, n = karar(alt, args, duz, b["tur"])
        if AGIRLIK[k] > AGIRLIK[en]:
            en, neden = k, n
    return en, neden


def main():
    try:
        girdi = json.load(sys.stdin)
    except ValueError:
        return 0
    if girdi.get("tool_name") != "Bash":
        return 0
    komut = (girdi.get("tool_input") or {}).get("command") or ""
    cwd = girdi.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    k, neden = degerlendir(komut, cwd)
    if k:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": k,
            "permissionDecisionReason": "[ajan-iskeleti] " + neden,
        }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
