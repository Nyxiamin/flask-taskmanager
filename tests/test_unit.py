# tests/test_unit.py
import os
from datetime import date, timedelta

import pytest

from app import _build_postgres_uri
from models import User, Task


def test_user_password_set_and_check():
    u = User(username="alice")
    u.set_password("s3cr3t")
    # password_hash must be set and check_password must validate
    assert hasattr(u, "password_hash")
    assert u.check_password("s3cr3t") is True
    assert u.check_password("wrong") is False


def test_task_is_overdue_false_without_due_date():
    t = Task(title="no due", description=None, user_id=1)
    t.due_date = None
    t.is_completed = False
    assert t.is_overdue() is False


def test_task_is_overdue_false_when_completed():
    t = Task(title="done", description=None, user_id=1)
    t.due_date = date.today() - timedelta(days=2)
    t.is_completed = True
    assert t.is_overdue() is False


def test_task_is_overdue_true_when_past_due_and_not_completed():
    t = Task(title="late", description=None, user_id=1)
    t.due_date = date.today() - timedelta(days=1)
    t.is_completed = False
    assert t.is_overdue() is True


def test__build_postgres_uri_prefers_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pw@host:5432/dbname")
    uri = _build_postgres_uri()
    assert uri == "postgresql://user:pw@host:5432/dbname"
    monkeypatch.delenv("DATABASE_URL", raising=False)


def test__build_postgres_uri_builds_from_parts(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("POSTGRES_USER", "u")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p")
    monkeypatch.setenv("POSTGRES_HOST", "h")
    monkeypatch.setenv("POSTGRES_PORT", "1234")
    monkeypatch.setenv("POSTGRES_DB", "mydb")

    uri = _build_postgres_uri()
    assert uri.startswith("postgresql+psycopg2://u:p@h:1234/mydb")
