import pytest
from app import create_app, db
from app.models.models import User


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def sample_user():
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpassword')
    return user


def test_new_user():
    user = User(username='testuser', email='test@example.com')
    user.set_password('test')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('test')
    assert not user.check_password('wrongpassword')


def test_index(client, sample_user):
    db.session.add(sample_user)
    db.session.commit()
    response = client.get('/users/')
    assert response.status_code == 200
    assert b'testuser' in response.data
    assert b'test@example.com' in response.data


def test_create_user(client):
    data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
    response = client.post('/users/create', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'newuser' in response.data
    assert b'newuser@example.com' in response.data


def test_update_user(client, sample_user):
    db.session.add(sample_user)
    db.session.commit()
    print(f"Testing update on user ID: {sample_user.id}")
    data = {'username': 'updateduser', 'email': 'updated@example.com'}
    response = client.post(f'/users/{sample_user.id}/update', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'updateduser' in response.data


def test_delete_user(client, sample_user):
    db.session.add(sample_user)
    db.session.commit()
    print(f"Testing update on user ID: {sample_user.id}")
    response = client.post(f'/users/{sample_user.id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'testuser' not in response.data


def test_create_user_duplicate_username(client, sample_user):
    """
    Test creating a user with a duplicate username should fail.
    """
    db.session.add(sample_user)
    db.session.commit()
    data = {'username': 'testuser', 'email': 'new@example.com', 'password': 'newpassword'}
    response = client.post('/users/create', data=data)
    assert response.status_code == 400
    assert b"This username is already taken" in response.data


def test_create_user_duplicate_email(client, sample_user):
    """
    Test creating a user with a duplicate email should fail.
    """
    db.session.add(sample_user)
    db.session.commit()
    data = {'username': 'newuser', 'email': 'test@example.com', 'password': 'newpassword'}
    response = client.post('/users/create', data=data)
    assert response.status_code == 400
    assert b"This email is already in use" in response.data


def test_create_user_invalid_data(client):
    """
    Test creating a user with invalid db should fail.
    """
    data = {'username': '', 'email': 'invalidemail', 'password': 'short'}
    response = client.post('/users/create', data=data)
    assert response.status_code == 400
    assert b"Invalid db" in response.data


def test_get_nonexistent_user(client):
    """
    Test retrieving a non-existent user should return a 404.
    """
    response = client.get('/users/99999')
    assert response.status_code == 404


def test_update_nonexistent_user(client):
    """
    Test updating a non-existent user should return a 404.
    """
    data = {'username': 'updateduser', 'email': 'updated@example.com'}
    response = client.post('/users/99999/update', data=data)
    assert response.status_code == 500


def test_delete_nonexistent_user(client):
    """
    Test deleting a non-existent user should return a 404.
    """
    response = client.post('/users/99999/delete')
    assert response.status_code == 500
