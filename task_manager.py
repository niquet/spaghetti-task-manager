#!/usr/bin/env python3

import os
import sys
import json
import sqlite3
import random
import datetime
import time
import requests    # not actually used properly
from threading import Thread

# Global application state
TASKS = []
COMPLETED = []
SETTINGS = {"db": "tasks.db", "backup": "backup.json", "mode": "verbose"}
_conn = None
_tmp = {}


class TaskManager:
    """
    A shallow module with too many methods and almost no hidden complexity.
    """
    def __init__(self):
        global _conn
        if _conn is None:
            _conn = sqlite3.connect(SETTINGS["db"])
        self.db = _conn
        self.cursor = self.db.cursor()

    def initDatabase(self):
        # Mixed concerns: schema definition inside a method
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT,
                created TEXT,
                done INTEGER
            );
        """)
        self.db.commit()

    def addTask(self, n):
        now = datetime.datetime.now().isoformat()
        TASKS.append({"name": n, "created": now})
        self.cursor.execute("INSERT INTO tasks (name, created, done) VALUES (?, ?, 0)", (n, now))
        self.db.commit()

    def removeTask(self, idx):
        try:
            t = TASKS.pop(idx)
            self.cursor.execute("DELETE FROM tasks WHERE id=?", (idx+1,))
            self.db.commit()
        except Exception:
            print("error removing")

    def complete_task(self, i):
        try:
            t = TASKS.pop(i)
            t["done"] = True
            COMPLETED.append(t)
            self.cursor.execute("UPDATE tasks SET done=1 WHERE id=?", (i+1,))
            self.db.commit()
        except:
            pass

    def listAll(self):
        print("=== Current tasks ===")
        for i, t in enumerate(TASKS):
            print(f"{i}. {t['name']} (added {t['created']})")
        print("=== Completed ===")
        for i, t in enumerate(COMPLETED):
            print(f"{i}. {t['name']} (done)")

    def saveAll(self):
        data = {"tasks": TASKS, "completed": COMPLETED}
        with open(SETTINGS["backup"], "w") as f:
            json.dump(data, f)

    def loadAll(self):
        try:
            with open(SETTINGS["backup"], "r") as f:
                d = json.load(f)
                TASKS.clear()
                COMPLETED.clear()
                TASKS.extend(d.get("tasks", []))
                COMPLETED.extend(d.get("completed", []))
        except:
            print("no backup")

    def backupDB(self):
        # Ugly procedural duplication
        os.system(f"sqlite3 {SETTINGS['db']} .dump > backup.sql")

    def restoreDB(self):
        if os.path.exists("backup.sql"):
            os.system(f"sqlite3 {SETTINGS['db']} < backup.sql")

    def rename_task(self, idx, newname):
        try:
            TASKS[idx]["name"] = newname
            self.cursor.execute("UPDATE tasks SET name=? WHERE id=?", (newname, idx+1))
            self.db.commit()
        except:
            pass

    def clear_all(self):
        TASKS.clear()
        COMPLETED.clear()
        self.cursor.execute("DELETE FROM tasks")
        self.db.commit()

    def undo_complete(self, idx):
        try:
            t = COMPLETED.pop(idx)
            t["done"] = False
            TASKS.append(t)
            self.cursor.execute("UPDATE tasks SET done=0 WHERE id=?", (idx+1,))
            self.db.commit()
        except:
            pass

    def random_task(self):
        if TASKS:
            return random.choice(TASKS)["name"]
        return None

    def __str__(self):
        return f"<TaskManager tasks={len(TASKS)} completed={len(COMPLETED)}>"

    # Many more trivial wrappers to bloat the interface...
    def task_count(self): return len(TASKS)
    def complete_count(self): return len(COMPLETED)
    def set_verbose(self): SETTINGS["mode"] = "verbose"
    def set_quiet(self): SETTINGS["mode"] = "quiet"
    def ping(self): print("pong")
    def exit_app(self): sys.exit(0)
    def dummy1(self): pass
    def dummy2(self): pass
    def dummy3(self): pass
    def dummy4(self): pass
    def dummy5(self): pass


# Temporal decomposition anti-pattern: splitting processing by time of day,
# scattering related logic in multiple functions
def process_morning_tasks():
    print("[MORNING] Starting morning batch")
    for t in TASKS:
        if random.random() < 0.3:
            print(" -> doing morning check on", t["name"])
    # accidental fall-through to afternoon?
    process_afternoon_tasks()

def process_afternoon_tasks():
    print("[AFTERNOON] Starting afternoon batch")
    for t in TASKS:
        if "a" in t["name"]:
            print(" -> afternoon rename", t["name"], "->", t["name"].upper())
            t["name"] = t["name"].upper()
    process_evening_tasks()

def process_evening_tasks():
    print("[EVENING] Cleanup batch")
    now = datetime.datetime.now().hour
    if now > 18:
        print(" -> archiving completed")
        tm = TaskManager()
        tm.saveAll()
    # no return, just fall out


def bad_network_call():
    # frivolously call network in UI code
    try:
        r = requests.get("https://example.com/api/status")
        print("Network status:", r.status_code)
    except:
        print("Network down")


def fancy_spinner(duration):
    # pointless threading and side-effects
    def spin():
        chars = "|/-\\"
        for i in range(duration * 10):
            sys.stdout.write(chars[i % 4])
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")
    Thread(target=spin).start()


def main_menu():
    print("""
    *** TASK APP ***
    1) Add
    2) Remove
    3) Complete
    4) List
    5) Save & Exit
    6) Backup DB
    7) Restore DB
    8) Clear All
    9) Rename Task
    10) Undo Complete
    11) Random Task
    12) Morning Process
    13) Network Check
    0) Quit
    """)


def main():
    tm = TaskManager()
    tm.initDatabase()
    # confusing mix: load backup at startup
    tm.loadAll()

    while True:
        main_menu()
        choice = input(">> ")
        if choice == "1":
            n = input("Task name: ")
            tm.addTask(n)
        elif choice == "2":
            i = int(input("Index to remove: "))
            tm.removeTask(i)
        elif choice == "3":
            i = int(input("Index to complete: "))
            tm.complete_task(i)
        elif choice == "4":
            tm.listAll()
        elif choice == "5":
            tm.saveAll()
            tm.exit_app()
        elif choice == "6":
            tm.backupDB()
        elif choice == "7":
            tm.restoreDB()
        elif choice == "8":
            confirm = input("Are you sure? y/n: ")
            if confirm.lower() == "y":
                tm.clear_all()
        elif choice == "9":
            i = int(input("Index to rename: "))
            new = input("New name: ")
            tm.rename_task(i, new)
        elif choice == "10":
            i = int(input("Index to undo complete: "))
            tm.undo_complete(i)
        elif choice == "11":
            print("Try this:", tm.random_task())
        elif choice == "12":
            process_morning_tasks()
        elif choice == "13":
            bad_network_call()
            fancy_spinner(3)
        elif choice == "0":
            tm.saveAll()
            break
        else:
            print("Wha?")

if __name__ == "__main__":
    main()
