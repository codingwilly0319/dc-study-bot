from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from study_bot.database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = Database(Path(self.temp_dir.name) / "test.sqlite3")
        self.db.initialize()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_list_tasks(self) -> None:
        task = self.db.add_task(
            user_id="user-1",
            title="Read linked list notes",
            subject="CS",
            due_date="2026-07-01",
        )

        tasks = self.db.list_tasks(user_id="user-1")

        self.assertEqual(task.id, tasks[0].id)
        self.assertEqual("Read linked list notes", tasks[0].title)
        self.assertEqual("CS", tasks[0].subject)
        self.assertFalse(tasks[0].is_done)

    def test_done_tasks_are_hidden_by_default(self) -> None:
        task = self.db.add_task(user_id="user-1", title="Finish bot README")
        completed = self.db.mark_done(user_id="user-1", task_id=task.id)

        active_tasks = self.db.list_tasks(user_id="user-1")
        all_tasks = self.db.list_tasks(user_id="user-1", include_done=True)

        self.assertIsNotNone(completed)
        self.assertEqual([], active_tasks)
        self.assertEqual(1, len(all_tasks))
        self.assertTrue(all_tasks[0].is_done)

    def test_users_only_see_their_own_tasks(self) -> None:
        self.db.add_task(user_id="user-1", title="User 1 task")
        self.db.add_task(user_id="user-2", title="User 2 task")

        user_1_tasks = self.db.list_tasks(user_id="user-1")

        self.assertEqual(1, len(user_1_tasks))
        self.assertEqual("User 1 task", user_1_tasks[0].title)

    def test_delete_task(self) -> None:
        task = self.db.add_task(user_id="user-1", title="Delete me")

        deleted = self.db.delete_task(user_id="user-1", task_id=task.id)

        self.assertTrue(deleted)
        self.assertEqual([], self.db.list_tasks(user_id="user-1", include_done=True))

    def test_stats(self) -> None:
        first = self.db.add_task(user_id="user-1", title="A")
        self.db.add_task(user_id="user-1", title="B")
        self.db.mark_done(user_id="user-1", task_id=first.id)

        stats = self.db.get_stats(user_id="user-1")

        self.assertEqual(2, stats.total)
        self.assertEqual(1, stats.completed)
        self.assertEqual(50.0, stats.completion_rate)


if __name__ == "__main__":
    unittest.main()
