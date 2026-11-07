"""ajan-iskeleti birim testleri. Koşum: python3 -m unittest discover -s tests -v

Geçici klasörlerde gerçek git depoları kurar; ağ ya da Claude Code gerektirmez.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ARAC = KOK / "araclar" / "iskelet.py"
BEKCI = KOK / "hooks" / "git_bekcisi.py"
KOMPAKT = KOK / "hooks" / "compact_sonrasi.py"
GIT_ORTAM = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                 GIT_COMMITTER_EMAIL="t@t")


def kos(*args, cwd=None, girdi=None):
    return subprocess.run([sys.executable, *map(str, args)], cwd=cwd, input=girdi, capture_output=True,
                          text=True, env=GIT_ORTAM)


def git(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, env=GIT_ORTAM)


def depo_kur(yol, dosyalar=None):
    yol.mkdir(parents=True)
    git("init", "-q", cwd=yol)
    git("symbolic-ref", "HEAD", "refs/heads/main", cwd=yol)
    for ad, metin in (dosyalar or {"README.md": "x\n"}).items():
        (yol / ad).parent.mkdir(parents=True, exist_ok=True)
        (yol / ad).write_text(metin)
    git("add", "-A", cwd=yol)
    git("commit", "-q", "-m", "ilk", cwd=yol)


def kurulum(tmp, kanca="yerel"):
    tmp = Path(tmp).resolve()  # macOS: /var → /private/var; araç çözülmüş yol yazar
    proje = tmp / "proje"
    depo_kur(proje, {"README.md": "x\n", "src/okuyucu/a.py": "a=1\n", "src/rapor/b.py": "b=1\n"})
    oturum = tmp / "oturumlar"
    r = kos(ARAC, "kur", "--proje", proje, "--ana-ajan", "ŞEF", "--kullanici", "Deniz", "--oturum-kok", oturum,
            "--kanca", kanca, "--hafiza", tmp / "hafiza")
    return proje, oturum, r


class BekciTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.proje, cls.oturum, r = kurulum(cls.tmp.name)
        assert r.returncode == 0, r.stdout + r.stderr
        r = kos(ARAC, "rol", "--proje", cls.proje, "--ad", "KANAL", "--arketip", "kanal")
        assert r.returncode == 0, r.stdout + r.stderr
        cls.rol = cls.oturum / "kanal"
        cls.disari = Path(cls.tmp.name) / "baska"
        cls.disari.mkdir()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def karar(self, komut, cwd):
        r = kos(BEKCI, girdi=json.dumps({"tool_name": "Bash", "tool_input": {"command": komut}, "cwd": str(cwd)}))
        self.assertEqual(r.returncode, 0, r.stderr)
        if not r.stdout.strip():
            return None
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]

    def test_ana_ajan(self):
        tablo = {
            "git push origin main": "ask",
            "git push": "ask",
            "git push -u origin is/dal": "ask",
            "git push --force origin main": "deny",
            "git push origin main -f": "deny",
            "git push --force-with-lease": "deny",
            "git push origin +main": "deny",
            "git push origin :eski": "deny",
            "git push --delete origin eski": "deny",
            "git push -d origin eski": "deny",
            "git push --prune origin": "deny",
            "git -C . push origin main": "deny",
            "cd x && git push origin main": "deny",
            "bash -c 'git push origin main'": "deny",
            "FOO=1 git push origin main": "deny",
            "sudo -u kim git push": "deny",
            "echo $(git push)": "deny",
            "git branch -D eski": "deny",
            "git branch -d eski": "deny",
            "git branch --delete eski": "deny",
            "git branch -a": None,
            "git branch -vv": None,
            "git status && git log --oneline -3": None,
            "echo 'git push origin main'": None,
            "grep -rn 'git push' docs": None,
            "git commit -m 'push sonra'": None,
            "git merge --no-ff --no-commit kod/is": None,
            'git push "dengesiz': "deny",
            "ls -la": None,
        }
        for komut, beklenen in tablo.items():
            with self.subTest(komut=komut):
                self.assertEqual(self.karar(komut, self.proje), beklenen)

    def test_rol(self):
        tablo = {"git push origin x": "deny", "git -C /tmp merge main": "deny", "git rebase main": "deny",
                 "git commit -m x": None, "git switch -c kanal/is_20261107 main": None, "git status": None}
        for komut, beklenen in tablo.items():
            with self.subTest(komut=komut):
                self.assertEqual(self.karar(komut, self.rol), beklenen)

    def test_kayitsiz_klasor_en_kisitli(self):
        yabanci = self.oturum / "kayitsiz"
        yabanci.mkdir(exist_ok=True)
        self.assertEqual(self.karar("git push origin main", yabanci), "deny")

    def test_iskelet_disi_sessiz(self):
        self.assertIsNone(self.karar("git push --force origin main", self.disari))

    def test_takma_ad(self):
        git("config", "alias.zp", "push --force", cwd=self.proje)
        git("config", "alias.sil", "!git branch -D", cwd=self.proje)
        self.assertEqual(self.karar("git zp origin main", self.proje), "deny")
        self.assertEqual(self.karar("git sil eski", self.proje), "deny")

    def test_bash_disi_arac(self):
        r = kos(BEKCI, girdi=json.dumps({"tool_name": "Read", "tool_input": {"file_path": "x"},
                                         "cwd": str(self.proje)}))
        self.assertEqual(r.stdout.strip(), "")


class KurulumTesti(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def dogrula(self, proje):
        return kos(ARAC, "dogrula", "--proje", proje)

    def test_kur_rol_dogrula(self):
        proje, oturum, r = kurulum(self.tmp.name)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for yol in ("CLAUDE.md", "CLAUDE.local.md", "PLAN.md", "iskelet.json", "iskelet.local.json",
                    "docs/BURADAN_BASLA.md", "docs/gorevler/KUYRUK.md", ".claude/settings.json",
                    ".claude/hooks/git_bekcisi.py", ".claude/skills/kur/SKILL.md", ".claude/agents/bagimsiz-okuyucu.md"):
            self.assertTrue((proje / yol).exists(), yol)
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", (proje / ".claude/skills/kur/SKILL.md").read_text())
        self.assertTrue((oturum / "sef" / "CLAUDE.md").exists())
        self.assertTrue((Path(self.tmp.name) / "hafiza" / "MEMORY.md").exists())
        self.assertLessEqual((proje / "CLAUDE.md").stat().st_size, 8 * 1024)
        d = self.dogrula(proje)
        self.assertEqual(d.returncode, 0, d.stdout)
        self.assertIn("HATA: 0", d.stdout)

        git("add", "-A", cwd=proje)
        git("commit", "-q", "-m", "kurulum", cwd=proje)
        r = kos(ARAC, "rol", "--proje", proje, "--ad", "GIRDI", "--arketip", "kod", "--alan", "src/okuyucu/**",
                "--worktree")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        agac = oturum / "girdi" / "proje"
        self.assertTrue((agac / ".claude/hooks/git_bekcisi.py").exists(), "çalışma ağacında kanca yok")
        kilit = json.loads((oturum / "girdi" / "kilit.json").read_text())
        self.assertIn(f"Edit(/{proje}/**)", kilit["permissions"]["deny"])
        self.assertNotIn("hooks", kilit, "kod rolü kancayı proje ayarından almalı")
        r = kos(ARAC, "rol", "--proje", proje, "--ad", "YAZAR", "--arketip", "yazar")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = kos(ARAC, "rol", "--proje", proje, "--ad", "ALT", "--arketip", "alt_yazar", "--ust", "YAZAR")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        kilit_girdi = json.loads((oturum / "girdi" / "kilit.json").read_text())
        self.assertIn(f"Edit(/{oturum / 'yazar'}/**)", kilit_girdi["permissions"]["deny"], "kilitler tazelenmedi")
        kilit_alt = json.loads((oturum / "alt" / "kilit.json").read_text())
        self.assertIn(f"Read(/{proje}/**)", kilit_alt["permissions"]["deny"])
        kilit_yazar = json.loads((oturum / "yazar" / "kilit.json").read_text())
        self.assertEqual(kilit_yazar["permissions"]["additionalDirectories"], [str(proje)])
        self.assertIn("compact_sonrasi.py", json.dumps(kilit_yazar["hooks"]))
        adres = (oturum / "OTURUMLAR.md").read_text()
        for ad in ("ŞEF", "GIRDI", "YAZAR", "ALT"):
            self.assertIn(f"| `{ad}` |", adres)
        d = self.dogrula(proje)
        self.assertEqual(d.returncode, 0, d.stdout)

        r = kos(ARAC, "kapat", "--proje", proje, "--ad", "YAZAR")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("KAPANDI-TARİHLİ", (oturum / "yazar" / "CLAUDE.md").read_text().splitlines()[0])
        self.assertTrue((oturum / "yazar").exists())
        self.assertEqual(self.dogrula(proje).returncode, 0)

    def test_dogrula_bozulmayi_yakalar(self):
        proje, oturum, r = kurulum(self.tmp.name)
        self.assertEqual(r.returncode, 0, r.stderr)
        durum = proje / "docs/DURUM.md"
        durum.write_text("\n".join(durum.read_text().splitlines()[1:]))
        (proje / "docs/YENI.md").write_text("> **DURUM: CANLI** · yeni\n")
        kuyruk = proje / "docs/gorevler/KUYRUK.md"
        kuyruk.write_text(kuyruk.read_text() + "| **IS-001** | eksik sütun |\n")
        ayar = json.loads((proje / ".claude/settings.json").read_text())
        ayar["permissions"]["ask"] = []
        (proje / ".claude/settings.json").write_text(json.dumps(ayar))
        d = self.dogrula(proje)
        self.assertEqual(d.returncode, 1)
        for parca in ("docs/DURUM.md: ilk beş satırda DURUM bandı yok", "docs/YENI.md: BURADAN_BASLA",
                      "KUYRUK satırı biçimsiz", "push onay kuralı"):
            self.assertIn(parca, d.stdout)

    def test_var_olan_dosyalar_ezilmez(self):
        proje = Path(self.tmp.name) / "proje"
        depo_kur(proje, {"CLAUDE.md": "eski talimat\n", "PLAN.md": "eski plan\n",
                         ".claude/settings.json": json.dumps({"permissions": {"allow": ["Bash(ls *)"]}})})
        r = kos(ARAC, "kur", "--proje", proje, "--ana-ajan", "GENEL", "--kullanici", "Deniz", "--kanca", "yerel")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((proje / "CLAUDE.md").read_text(), "eski talimat\n")
        self.assertEqual((proje / "PLAN.md").read_text(), "eski plan\n")
        self.assertTrue((proje / "CLAUDE.iskelet.md").exists())
        ayar = json.loads((proje / ".claude/settings.json").read_text())
        self.assertEqual(ayar["permissions"]["allow"], ["Bash(ls *)"])
        self.assertIn("Bash(git push *)", ayar["permissions"]["ask"])
        self.assertTrue((Path(self.tmp.name) / "proje_oturumlar" / "genel" / "CLAUDE.md").exists())
        self.assertIn("BİRLEŞTİR", r.stdout)

    def test_oturum_koku_proje_icinde_olamaz(self):
        proje = Path(self.tmp.name) / "proje"
        depo_kur(proje)
        r = kos(ARAC, "kur", "--proje", proje, "--ana-ajan", "GENEL", "--kullanici", "D", "--oturum-kok",
                proje / "oturumlar")
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((proje / "iskelet.json").exists())

    def test_eklenti_kipi_etkin_degilse_hata(self):
        proje, oturum, r = kurulum(self.tmp.name, kanca="eklenti")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((proje / ".claude/hooks").exists())
        d = kos(ARAC, "dogrula", "--proje", proje)
        self.assertIn("Eklenti etkin değil", d.stdout)
        ayar = json.loads((proje / ".claude/settings.json").read_text())
        ayar["enabledPlugins"] = {"ajan-iskeleti@ajan-iskeleti": True}
        (proje / ".claude/settings.json").write_text(json.dumps(ayar))
        self.assertEqual(kos(ARAC, "dogrula", "--proje", proje).returncode, 0)


class KompaktTesti(unittest.TestCase):
    def test_rol_ve_ana(self):
        with tempfile.TemporaryDirectory() as tmp:
            proje, oturum, r = kurulum(tmp)
            self.assertEqual(r.returncode, 0, r.stderr)
            kos(ARAC, "rol", "--proje", proje, "--ad", "KANAL", "--arketip", "kanal")
            seyir = oturum / "kanal" / "SEYIR.md"
            seyir.write_text(seyir.read_text().replace("- **Açık iş:** yok", "- **Açık iş:** IS-007 cevabı"))
            c = kos(KOMPAKT, girdi=json.dumps({"cwd": str(oturum / "kanal")}))
            self.assertIn("Sen KANAL oturumusun", c.stdout)
            self.assertIn("IS-007 cevabı", c.stdout)
            c = kos(KOMPAKT, girdi=json.dumps({"cwd": str(proje)}))
            self.assertIn("Sen ana ajansın (ŞEF)", c.stdout)
            c = kos(KOMPAKT, girdi=json.dumps({"cwd": tmp}))
            self.assertEqual(c.stdout, "")


class AracTesti(unittest.TestCase):
    def test_alanlar(self):
        with tempfile.TemporaryDirectory() as tmp:
            proje = Path(tmp) / "p"
            depo_kur(proje, {"src/a/x.py": "1", "src/b/y.py": "1", "tests/test_a.py": "1"})
            for i in range(3):
                (proje / "src/a/x.py").write_text(str(i))
                (proje / "tests/test_a.py").write_text(str(i))
                git("commit", "-qam", f"a{i}", cwd=proje)
            r = kos(ARAC, "alanlar", "--proje", proje)
            self.assertEqual(r.returncode, 0, r.stderr)
            satir = next(s for s in r.stdout.splitlines() if s.startswith("| `src/a`"))
            self.assertIn("| 4 |", satir)
            self.assertIn("`tests`", satir)

    def test_katla(self):
        with tempfile.TemporaryDirectory() as tmp:
            seyir = Path(tmp) / "SEYIR.md"
            govde = "".join(f"- 01.11.2026: giriş {i} " + "x" * 200 + "\n" for i in range(1000))
            seyir.write_text("> **DURUM: CANLI** · s\n\n# S\n\n## Şimdi\n\n- **Açık iş:** IS-9\n\n## Günlük\n\n" + govde)
            r = kos(ARAC, "katla", "--dosya", seyir, "--esik", "50000")
            self.assertEqual(r.returncode, 0, r.stderr)
            yeni = seyir.read_text()
            self.assertLess(len(yeni.encode()), 50000)
            self.assertIn("- **Açık iş:** IS-9", yeni)
            self.assertIn("giriş 999", yeni)
            arsiv = list((Path(tmp) / "arsiv").glob("SEYIR_arsiv_*.md"))
            self.assertEqual(len(arsiv), 1)
            self.assertIn("giriş 0 ", arsiv[0].read_text())


class EklentiTesti(unittest.TestCase):
    def test_bicim(self):
        eklenti = json.loads((KOK / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(eklenti["name"], "ajan-iskeleti")
        self.assertEqual(eklenti["version"], (KOK / "SURUM").read_text().strip())
        pazar = json.loads((KOK / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(pazar["plugins"][0]["name"], "ajan-iskeleti")
        for beceri in (KOK / "skills").iterdir():
            metin = (beceri / "SKILL.md").read_text()
            self.assertTrue(metin.startswith("---\n"), beceri.name)
            on = metin.split("---\n")[1]
            self.assertIn(f"name: {beceri.name}\n", on)
            self.assertRegex(on, r"description: .{40,}")
        kancalar = json.loads((KOK / "hooks/hooks.json").read_text())
        for olay in kancalar["hooks"].values():
            for g in olay:
                for h in g["hooks"]:
                    ad = re.search(r"hooks/([a-z_]+\.py)", h["command"]).group(1)
                    self.assertTrue((KOK / "hooks" / ad).exists(), ad)

    def test_arketip_kart_bloklari(self):
        for arketip in ("koordinator", "kod", "kanal", "gozlemci", "yazar", "alt_yazar", "arsivci"):
            metin = (KOK / "roller" / f"{arketip}.md").read_text()
            self.assertEqual(metin.count("<!-- kart:başla -->"), 1, arketip)
            self.assertTrue(metin.startswith("> **DURUM:"), arketip)


if __name__ == "__main__":
    unittest.main()
