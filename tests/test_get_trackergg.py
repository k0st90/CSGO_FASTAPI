import pytest

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code", [
    ('s1mple', '3', 451),
    ('H1de__', '2', 404),
    ('puss9hunter', '1', 200)
])
def test_get_global_player_csgo_stats_(client, test_user, faceit_nickname, telegram_id, status_code, test_user_with_closed_steam_acc):
    res = client.get(f"/global_player_csgo_stats/{telegram_id}")
    assert res.status_code == status_code

@pytest.mark.parametrize("faceit_nickname, telegram_id, status_code, weapon_name", [
    ('s1mple', '3', 451, "AK"),
    ('H1de__', '2', 404, "AK"),
    ('puss9hunter', '1', 200, "AK")
])
def test_get_player_csgo_stats_weapon(client, test_user, faceit_nickname, telegram_id, status_code, test_user_with_closed_steam_acc, weapon_name):
    res = client.get(f"/player_csgo_stats_weapon/{telegram_id}/{weapon_name}")
    assert res.status_code == status_code