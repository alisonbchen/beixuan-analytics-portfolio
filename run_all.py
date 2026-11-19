"""Run the offline demonstrations and focused checks from any working directory."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
nyc = root / "projects/nyc311"
education = root / "projects/education_outcomes"
retail = root / "projects/retail_growth"
finance = root / "projects/financial_research"
commands = [
    (nyc, ["src/pipeline.py", "--input", "data/synthetic_requests.csv"]),
    (education, ["education.py"]),
    (retail, ["retail.py"]),
    (finance, ["research.py"]),
    (nyc, ["-m", "unittest", "discover", "-s", "tests", "-v"]),
    (education, ["-m", "unittest", "discover", "-s", "tests", "-v"]),
    (retail, ["-m", "unittest", "discover", "-s", "tests", "-v"]),
    (finance, ["-m", "unittest", "discover", "-s", "tests", "-v"]),
]
for cwd, args in commands:
    print("Running:", cwd.name, " ".join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=cwd, check=True)
