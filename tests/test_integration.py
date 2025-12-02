# tests/test_integration.py
import pytest
from app import create_app
from extensions import db as _db
from models import User, Task

@pytest.fixture
def app():
    # create app with testing config and sqlite in-memory DB
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SECRET_KEY="test-secret",
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, username="testuser", password="pass"):
    return client.post("/register", data={
        "username": username,
        "password": password,
        "confirm": password
    }, follow_redirects=True)


def login(client, username="testuser", password="pass"):
    return client.post("/login", data={
        "username": username,
        "password": password
    }, follow_redirects=True)


def test_register_and_login_flow(client, app):
    # register
    rv = register(client)
    assert b"Registration successful" in rv.data or b"Registration successful" in rv.data
    # login
    rv = login(client)
    assert b"Logged in successfully" in rv.data or b"Logged in successfully" in rv.data

    # ensure user exists in DB
    with app.app_context():
        u = _db.session.query(User).filter_by(username="testuser").first()
        assert u is not None


def test_create_task_via_post_and_toggle(client, app):
    register(client)
    login(client)

    # create task
    rv = client.post("/tasks/new", data={
        "title": "My integration task",
        "description": "desc",
        "due_date": ""
    }, follow_redirects=True)
    assert b"Task created" in rv.data

    # find task in DB
    with app.app_context():
        u = User.query.filter_by(username="testuser").first()
        tasks = Task.query.filter_by(user_id=u.id).all()
        assert len(tasks) == 1
        task = tasks[0]
        assert task.title == "My integration task"
        assert not task.is_completed

    # toggle via POST
    rv = client.post(f"/tasks/{task.id}/toggle", follow_redirects=True)
    assert b"Task status updated" in rv.data
    with app.app_context():
        t = _db.session.get(Task, task.id)
        assert t.is_completed is True
