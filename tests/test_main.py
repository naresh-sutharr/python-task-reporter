"""Tests for python-task-reporter."""

import json
from pathlib import Path
import unittest
from main import read_input, mock_api, process_tasks, write_output


class TestTaskReporter(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_output_temp")
        self.test_dir.mkdir(exist_ok=True)
        self.sample_data = [
            {"id": 1, "task": "Summarize user feedback for onboarding flow"},
            {"id": 2, "task": "Extract action items from team retrospective meeting"},
            {"id": 3, "task": "Categorize customer support inquiries by urgency level"}
        ]
        self.sample_file = self.test_dir / "sample_temp.json"
        self.sample_file.write_text(json.dumps(self.sample_data), encoding="utf-8")

    def tearDown(self):
        if self.sample_file.exists():
            self.sample_file.unlink()
        report_json = self.test_dir / "report.json"
        report_md = self.test_dir / "report.md"
        if report_json.exists():
            report_json.unlink()
        if report_md.exists():
            report_md.unlink()
        if self.test_dir.exists():
            self.test_dir.rmdir()

    def test_mock_api(self):
        result = mock_api("Summarize customer feedback")
        self.assertEqual(result["word_count"], 3)
        self.assertEqual(result["status"], "mock_api_success")
        self.assertIn("Task contains 3 words", result["summary"])

    def test_read_input(self):
        tasks = read_input(self.sample_file)
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]["task"], "Summarize user feedback for onboarding flow")

    def test_process_tasks(self):
        results = process_tasks(self.sample_data)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["task_id"], 1)
        self.assertEqual(results[0]["result"]["status"], "mock_api_success")

    def test_write_output(self):
        results = process_tasks(self.sample_data)
        write_output(results, self.test_dir)
        self.assertTrue((self.test_dir / "report.json").exists())
        self.assertTrue((self.test_dir / "report.md").exists())

        report_content = json.loads((self.test_dir / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report_content["total_tasks"], 3)
        self.assertEqual(report_content["api_mode"], "mock")


if __name__ == "__main__":
    unittest.main()
