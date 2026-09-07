"""Update behavior in disposable repositories with local remotes only."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "requires git and bash")
class UpdateTests(unittest.TestCase):
    def git(self, directory, *args):
        return subprocess.run(["git", *args], cwd=directory, text=True, capture_output=True, check=True).stdout.strip()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.seed = self.root / "seed"
        self.seed.mkdir()
        self.git(self.seed, "init", "-q", "-b", "main")
        self.git(self.seed, "config", "user.email", "fixture@example.invalid")
        self.git(self.seed, "config", "user.name", "Fixture")
        (self.seed / "skills/scripts").mkdir(parents=True)
        for name in ("update.sh", "check-update.sh"):
            shutil.copy(ROOT / "skills/scripts" / name, self.seed / "skills/scripts" / name)
        (self.seed / "skills/SKILL.md").write_text("---\nversion: 1.0.0\n---\n")
        (self.seed / "VERSION").write_text("1.0.0\n")
        (self.seed / "content").write_text("original\n")
        self.git(self.seed, "add", ".")
        self.git(self.seed, "commit", "-qm", "initial")
        self.remote = self.root / "origin.git"
        self.git(self.root, "clone", "--bare", str(self.seed), str(self.remote))
        self.git(self.seed, "remote", "add", "origin", str(self.remote))
        self.checkout = self.root / "checkout"
        self.git(self.root, "clone", str(self.remote), str(self.checkout))
        self.git(self.checkout, "config", "user.email", "fixture@example.invalid")
        self.git(self.checkout, "config", "user.name", "Fixture")

    def update(self, answer="y\n", checkout=None):
        return subprocess.run(["bash", "skills/scripts/update.sh"], cwd=checkout or self.checkout,
                              input=answer, text=True, capture_output=True, timeout=10)

    def advance_remote(self):
        (self.seed / "VERSION").write_text("1.1.0\n")
        self.git(self.seed, "commit", "-qam", "new release")
        self.git(self.seed, "push", "origin", "main")

    def test_dirty_checkout_is_preserved_without_stash(self):
        (self.checkout / "content").write_text("user changes\n")
        result = self.update("n\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.checkout / "content").read_text(), "user changes\n")
        self.assertEqual(self.git(self.checkout, "stash", "list"), "")

    def test_untracked_files_are_preserved(self):
        (self.checkout / "draft").write_text("work")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual((self.checkout / "draft").read_text(), "work")

    def test_decline_and_eof_do_not_fetch_or_change_head(self):
        self.advance_remote()
        original = self.git(self.checkout, "rev-parse", "HEAD")
        for answer in ("n\n", ""):
            result = self.update(answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.git(self.checkout, "rev-parse", "HEAD"), original)
            self.assertFalse((self.checkout / ".git/FETCH_HEAD").exists())

    def test_feature_branch_is_not_rebased_or_switched(self):
        self.git(self.checkout, "checkout", "-qb", "feature/local")
        self.advance_remote()
        original = self.git(self.checkout, "rev-parse", "HEAD")
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual(self.git(self.checkout, "branch", "--show-current"), "feature/local")
        self.assertEqual(self.git(self.checkout, "rev-parse", "HEAD"), original)

    def test_fast_forward_succeeds(self):
        self.advance_remote()
        result = self.update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.checkout / "VERSION").read_text().strip(), "1.1.0")
        self.assertEqual(self.git(self.checkout, "status", "--porcelain"), "")

    def test_divergence_is_rejected_without_rebase(self):
        (self.checkout / "content").write_text("local commit\n")
        self.git(self.checkout, "commit", "-qam", "local")
        original = self.git(self.checkout, "rev-parse", "HEAD")
        self.advance_remote()
        self.assertNotEqual(self.update().returncode, 0)
        self.assertEqual(self.git(self.checkout, "rev-parse", "HEAD"), original)
        self.assertEqual(self.git(self.checkout, "status", "--porcelain"), "")

    def test_linked_worktree_is_supported(self):
        self.git(self.checkout, "checkout", "-qb", "parking")
        worktree = self.root / "worktree"
        self.git(self.checkout, "worktree", "add", str(worktree), "main")
        self.advance_remote()
        result = self.update(checkout=worktree)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((worktree / "VERSION").read_text().strip(), "1.1.0")

    def test_manual_check_only_reports_newer_release(self):
        binary = self.root / "bin"
        binary.mkdir()
        curl = binary / "curl"
        curl.write_text('#!/usr/bin/env bash\nprintf "%s" "$TEST_REMOTE_VERSION"\n')
        curl.chmod(0o755)
        # Installed skills may lack the repository-level VERSION file.
        (self.checkout / "VERSION").unlink()
        for version, expected in [("0.9.9", False), ("1.0.0", False), ("1.0.1", True), ("1.10.0", True), ("2.0.0", True), ("", False), ("invalid", False)]:
            env = dict(os.environ, PATH=str(binary) + os.pathsep + os.environ["PATH"], TEST_REMOTE_VERSION=version)
            result = subprocess.run(["bash", "skills/scripts/check-update.sh"], cwd=self.checkout,
                                    env=env, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(bool(result.stdout.strip()), expected, version)


if __name__ == "__main__":
    unittest.main()
