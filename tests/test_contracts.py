"""Exercise the documented recipes with a local mock CLI; no network or credits."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def bash_blocks(text):
    return [textwrap.dedent(block) for block in re.findall(r"^[ \t]*```bash\n(.*?)^[ \t]*```", text, re.M | re.S)]


@unittest.skipUnless(shutil.which("jq") and shutil.which("bash"), "requires bash and jq")
class RecipeTests(unittest.TestCase):
    def run_recipe(self, script, result, exit_code=0):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cli = root / "pixverse"
            cli.write_text('''#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$MOCK_CALLS"
if [ "$1" = asset ]; then
  printf '{"file":"result.mp4"}\\n'
else
  printf '%s\\n' "$MOCK_RESULT"
  exit "$MOCK_EXIT"
fi
''')
            cli.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"],
                       MOCK_CALLS=str(root / "calls"), MOCK_RESULT=json.dumps(result) if result is not None else "",
                       MOCK_EXIT=str(exit_code))
            response = subprocess.run(["bash", "-c", script], env=env, text=True, capture_output=True)
            calls = (root / "calls").read_text().splitlines()
            return response, calls

    def create_recipe(self, kind):
        name = "create-video.md" if kind == "video" else "create-and-edit-image.md"
        blocks = bash_blocks((SKILLS / "capabilities" / name).read_text())
        matching = [block for block in blocks if "if RESULT=$(pixverse create " + kind in block]
        self.assertEqual(len(matching), 1, "Expected one executable single-create recipe")
        return matching[0] + '\necho "$' + kind.upper() + '_ID"'

    def test_create_and_parse_only_submits_once(self):
        for kind in ("video", "image"):
            with self.subTest(kind=kind):
                result, calls = self.run_recipe(self.create_recipe(kind), {"status": "completed", kind + "_id": 123})
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), "123")
                self.assertEqual(len(calls), 1)
                self.assertTrue(calls[0].startswith("create " + kind + " "))

    def test_failed_creation_does_not_continue(self):
        for kind in ("video", "image"):
            result, calls = self.run_recipe(self.create_recipe(kind) + '\nprintf "SHOULD_NOT_RUN"', None, 7)
            self.assertEqual(result.returncode, 7)
            self.assertNotIn("SHOULD_NOT_RUN", result.stdout)
            self.assertEqual(len(calls), 1)

    def test_missing_id_is_not_success(self):
        for kind in ("video", "image"):
            result, _ = self.run_recipe(self.create_recipe(kind), {"status": "completed"})
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("null", result.stdout)

    def test_shared_recipe_downloads_only_completed_result(self):
        script = bash_blocks((SKILLS / "references/execution-contract.md").read_text())[0]
        result, calls = self.run_recipe(script, {"status": "completed", "video_id": 123})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 2)
        self.assertTrue(calls[1].startswith("asset download 123 "))
        partial = {"status": "partial", "items": [{"video_id": 123, "status": "completed"}], "failed_ids": [124]}
        result, calls = self.run_recipe(script, partial, 5)
        self.assertEqual(result.returncode, 5)
        self.assertEqual(len(calls), 1)
        self.assertIn('"video_id": 123', result.stderr)

    def test_documented_batch_parser_retains_successes(self):
        text = (SKILLS / "references/execution-contract.md").read_text()
        query = re.search(r"Extract completed video IDs with `jq -r '(.*?)'`", text).group(1)
        for value, expected in [
            ({"status": "completed", "video_id": 1}, ["1"]),
            ({"status": "completed", "items": [{"status": "completed", "video_id": 1}, {"status": "completed", "video_id": 2}]}, ["1", "2"]),
            ({"status": "partial", "items": [{"status": "completed", "video_id": 2}], "failed_ids": [1]}, ["2"]),
            ({"status": "partial", "items": [], "failed_ids": [1]}, []),
        ]:
            result = subprocess.run(["jq", "-r", query], input=json.dumps(value), text=True, capture_output=True, check=True)
            self.assertEqual(result.stdout.splitlines(), expected)

    def test_account_recipe_does_not_read_stdin(self):
        text = (SKILLS / "capabilities/auth-and-account.md").read_text().split("Example error handling:", 1)[1]
        result, calls = self.run_recipe(bash_blocks(text)[0], {"credits": {"total": 650}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("650", result.stdout)
        self.assertEqual(len(calls), 1)


class DocumentationTests(unittest.TestCase):
    def test_local_links_resolve(self):
        for path in list(SKILLS.rglob("*.md")) + [ROOT / "README.md"]:
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                target = link.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                self.assertTrue((path.parent / target).exists(), f"{path.relative_to(ROOT)}: {link}")

    def test_release_versions_match(self):
        version = (ROOT / "VERSION").read_text().strip()
        entry = (SKILLS / "SKILL.md").read_text()
        self.assertEqual(re.search(r"^version: (.+)$", entry, re.M).group(1), version)
        self.assertEqual(re.search(r"^## \[(.+?)\]", (ROOT / "CHANGELOG.md").read_text(), re.M).group(1), version)


if __name__ == "__main__":
    unittest.main()
