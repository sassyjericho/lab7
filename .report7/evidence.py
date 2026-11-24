import json
import subprocess
import sys
import unittest
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class Evidence:
    @classmethod
    def run(cls):
        exe = ROOT / 'dist' / 'Animale' / 'Animale.exe'
        spec = ROOT / 'Animale.spec'
        requirements = ROOT / 'requirements.txt'

        pyinstaller = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', '--version'],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        stream = StringIO()
        tests = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(tests)
        assert result.wasSuccessful()

        output = {
            'build': (
                f'PyInstaller: {pyinstaller}\n'
                f'Python: {sys.version.split()[0]}\n'
                f'Fisier de configurare: {spec.name}\n'
                f'Punct de intrare: __main__.py\n'
                f'Director distributiv: dist\\\\Animale\n'
                f'Executabil: {exe.name}\n'
                f'Dimensiune executabil: {exe.stat().st_size} octeti\n'
                f'Dependente: {requirements.read_text(encoding="utf-8").strip()}'
            ),
            'dist': cls.tree(exe.parent),
            'tests': stream.getvalue(),
        }
        report_dir = ROOT / '.report7'
        report_dir.mkdir(exist_ok=True)
        (report_dir / 'evidence.json').write_text(
            json.dumps(output, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )

    @classmethod
    def tree(cls, directory):
        top = sorted((p for p in directory.iterdir()), key=lambda p: p.name.lower())
        lines = [f'{directory.name}/']
        for index, path in enumerate(top):
            prefix = '└── ' if index == len(top) - 1 else '├── '
            if path.is_dir():
                lines.append(f'{prefix}{path.name}/')
            else:
                lines.append(f'{prefix}{path.name} ({path.stat().st_size} octeti)')
        return '\n'.join(lines)


if __name__ == '__main__':
    Evidence.run()
