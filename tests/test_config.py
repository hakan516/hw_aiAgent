import os
import tempfile
import unittest
from pathlib import Path

from ai_study_agent.config import load_env_file


class ConfigTest(unittest.TestCase):
    def test_load_env_file_sets_missing_values(self):
        with tempfile.TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text(
                "GEMINI_API_KEY=test-key\nGEMINI_MODEL='test-model'\n",
                encoding="utf-8",
            )
            old_key = os.environ.pop("GEMINI_API_KEY", None)
            old_model = os.environ.pop("GEMINI_MODEL", None)
            try:
                load_env_file(env_path)

                self.assertEqual(os.environ["GEMINI_API_KEY"], "test-key")
                self.assertEqual(os.environ["GEMINI_MODEL"], "test-model")
            finally:
                os.environ.pop("GEMINI_API_KEY", None)
                os.environ.pop("GEMINI_MODEL", None)
                if old_key is not None:
                    os.environ["GEMINI_API_KEY"] = old_key
                if old_model is not None:
                    os.environ["GEMINI_MODEL"] = old_model

    def test_load_env_file_does_not_override_existing_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text("GEMINI_API_KEY=file-key\n", encoding="utf-8")
            old_key = os.environ.get("GEMINI_API_KEY")
            os.environ["GEMINI_API_KEY"] = "real-env-key"
            try:
                load_env_file(env_path)

                self.assertEqual(os.environ["GEMINI_API_KEY"], "real-env-key")
            finally:
                if old_key is None:
                    os.environ.pop("GEMINI_API_KEY", None)
                else:
                    os.environ["GEMINI_API_KEY"] = old_key


if __name__ == "__main__":
    unittest.main()
