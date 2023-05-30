import pytest

def test_create_account(client):
    user_data = {"faceit_nickname":"puss9hunter", 
                 "telegram_id":"1"}
    res = client.post(f"/account/{user_data['faceit_nickname']}", json=user_data)
    assert res.status_code == 201

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('puss9hunter', '1', 302),
    ('37567346537645', '1', 404)
])
def failed_account_creation(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.post(f"/account/{faceit_nickname}", json={"faceit_nickname": faceit_nickname, "telegram_id": telegram_id})
    assert res.status_code == status_code
    
@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('H1de__', '1', 204),
])  
def test_update_account(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.put(f"/update_nickname/{telegram_id}/{faceit_nickname}", json={"faceit_nickname": faceit_nickname, "telegram_id": telegram_id})
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('puss9hunter', '1', 302),
    ('37567346537645', '1', 404),
    ('H1de__', '2', 404)
])
def failed_account_update(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.put(f"/update_nickname/{telegram_id}/{faceit_nickname}", json={"faceit_nickname": faceit_nickname, "telegram_id": telegram_id})
    assert res.status_code == status_code
    
def test_delete_account(client, test_user):
    res = client.delete(f"/delete_account/{test_user['telegram_id']}")
    assert res.status_code == 204

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('H1de__', '2', 404)
])
def test_delete_wrong_account(client, faceit_nickname, telegram_id, status_code):
    res = client.delete(f"/delete_account/{telegram_id}")
    assert res.status_code == status_code
    