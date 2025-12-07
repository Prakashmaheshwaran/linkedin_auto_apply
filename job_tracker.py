import sqlite3
import csv
import os
import shutil
from datetime import datetime

class JobTracker:
    def __init__(self, db_path="jobs.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Initialize the jobs table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create an index on status for faster reporting
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON jobs(status)')
        self.conn.commit()

    def add_job(self, job_id, status="COLLECTED"):
        """
        Add a new job to the tracker.
        Returns True if added, False if it already exists.
        """
        try:
            self.cursor.execute('INSERT INTO jobs (job_id, status) VALUES (?, ?)', (str(job_id), status))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_job(self, job_id):
        """Returns the status of the job, or None if not found."""
        self.cursor.execute('SELECT status FROM jobs WHERE job_id = ?', (str(job_id),))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_job(self, job_id, status):
        """Updates the status of an existing job."""
        self.cursor.execute('''
            UPDATE jobs 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE job_id = ?
        ''', (status, str(job_id)))
        self.conn.commit()

    def is_processed(self, job_id):
        """
        Checks if the job has already been processed (Applied, Failed, External, or Skipped).
        Returns True if processed, False if it's new or just 'Collected'.
        """
        status = self.check_job(job_id)
        # We consider 'COLLECTED' as not fully processed yet, everything else is processed
        return status in ["APPLIED", "FAILED", "EXTERNAL", "SKIPPED", "LEGACY_PROCESSED"]

    def get_statistics(self):
        """Returns a dictionary with counts of jobs by status."""
        self.cursor.execute('SELECT status, COUNT(*) FROM jobs GROUP BY status')
        return dict(self.cursor.fetchall())

    def backup_db(self):
        """Creates a backup of the database file."""
        backup_path = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(self.db_path, backup_path)
        print(f"Database backed up to {backup_path}")

    def migrate_from_csv(self, processed_csv_path):
        """
        Migrates data from the legacy CSV file.
        Marks all IDs found in the CSV as 'LEGACY_PROCESSED'.
        """
        if not os.path.exists(processed_csv_path):
            print(f"CSV file {processed_csv_path} not found. Skipping migration.")
            return

        print(f"Migrating data from {processed_csv_path}...")
        count = 0
        try:
            with open(processed_csv_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0].strip():
                        job_id = row[0].strip()
                        # Only insert if it doesn't exist
                        if self.add_job(job_id, status="LEGACY_PROCESSED"):
                            count += 1
            print(f"Migration complete. Imported {count} legacy records.")
        except Exception as e:
            print(f"Error during migration: {e}")

    def close(self):
        self.conn.close()

# Example usage/Test
if __name__ == "__main__":
    tracker = JobTracker()
    print("Statistics:", tracker.get_statistics())
    tracker.close()
