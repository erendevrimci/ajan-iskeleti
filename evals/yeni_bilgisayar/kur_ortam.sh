#!/bin/bash
# İki ayrık alanı olan küçük bir depo: okuyucu ve rapor; her biri kendi testiyle birlikte değişir.
set -euo pipefail
G="git -c user.name=t -c user.email=t@t"
mkdir proje && cd proje && git init -q && git symbolic-ref HEAD refs/heads/main
mkdir -p src/okuyucu src/rapor tests veri
printf '[project]\nname = "oyuncak"\n[tool.pytest.ini_options]\ntestpaths = ["tests"]\n' > pyproject.toml
echo "# oyuncak: CSV okuyup rapor üreten küçük araç" > README.md
echo "def oku(y): return []" > src/okuyucu/csv_okur.py
echo "def yaz(s): return ''" > src/rapor/ozet.py
echo "def test_oku(): assert True" > tests/test_okuyucu.py
echo "def test_yaz(): assert True" > tests/test_rapor.py
echo "ornek" > veri/.gitkeep
git add -A && $G commit -qm ilk
for i in 1 2 3 4 5 6; do
  echo "# $i" >> src/okuyucu/csv_okur.py; echo "# $i" >> tests/test_okuyucu.py
  git add -A && $G commit -qm "okuyucu $i"
done
for i in 1 2 3; do
  echo "# $i" >> src/rapor/ozet.py; echo "# $i" >> tests/test_rapor.py
  git add -A && $G commit -qm "rapor $i"
done
