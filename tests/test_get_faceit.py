import pytest

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('puss9hunter', '1', 200),
    ('H1de__', '2', 404)
])
def test_get_player_details(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.get(f"/player_details_by_nickname/{telegram_id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('s1mple', '1', 200),
    ('H1de__', '2', 404)
])
def test_get_player_friends(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.get(f"/player_friendsids_by_nickname/{telegram_id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('puss9hunter', '1', 200),
    ('H1de__', '2', 404)
])
def test_get_player_extended_stats(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.get(f"/player_extended_csgo_stats/{telegram_id}")
    assert res.status_code == status_code
    
@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code, mapname", [
    ('puss9hunter', '1', 200, 'de_dust2'),
    ('H1de__', '2', 404, 'de_dust2')
])
def test_get_player_map_csgo_stats(client, test_user, faceit_nickname, telegram_id, status_code, mapname):
    res = client.get(f"/player_map_csgo_stats/{mapname}/{telegram_id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('puss9hunter', '1', 200),
    ('H1de__', '2', 404)
])
def test_get_last_20_games_stats(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.get(f"/last_20_games_stats/{telegram_id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code, match_id", [
    ('puss9hunter', '1', 200, "1-8332d095-4cc5-4759-a37a-5314008d884a"),
    ('H1de__', '2', 404, "1-8332d095-4cc5-4759-a37a-5314008d884a")
])
def test_get_match_statistic(client, test_user, faceit_nickname, telegram_id, status_code, match_id):
    res = client.get(f"/match_statistic/{telegram_id}/{match_id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('puss9hunter', '1', 200),
    ('H1de__', '2', 404)
])
def test_get_global_position(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.get(f"/global_position/{telegram_id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('puss9hunter', '1', 200),
    ('H1de__', '2', 404)
])
def test_get_country_position(client, test_user, faceit_nickname, telegram_id, status_code):
    res = client.get(f"/country_position/{telegram_id}")
    assert res.status_code == status_code