from http import HTTPStatus

from beeline.event_participiant.models import Registration


class TestEvent:

    def test_success_registration(
            self,
            event,
            app,
            user,
            mocker
    ):
        mocker.patch("flask_jwt._jwt_required", side_effect=lambda x: x)
        mocked_request = mocker.patch("flask_jwt._request_ctx_stack")
        mocked_request.top.current_identity = user
        response = app.post(
            f"/registration/{event.id}/",
        )
        reg = Registration.query.filter_by(user_id=user.id).first()
        assert reg is not None
        assert reg.event_id == event.id
        assert "message" in response.json
        message = "Успешно зарегистрирован"
        assert response.json["message"] == message
        assert response.status_code == HTTPStatus.CREATED

    def test_repeat_registration(self, app, mocker, registration):
        mocker.patch("flask_jwt._jwt_required", side_effect=lambda x: x)
        mocked_request = mocker.patch("flask_jwt._request_ctx_stack")
        reg, user, event = registration
        mocked_request.top.current_identity = user
        response = app.post(
            f"/registration/{event.id}/",
        )
        assert "message" in response.json
        message = "Уже зарегистрирован"
        assert response.json["message"] == message
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_registration_not_existing_event(self, app, user, mocker, event, registration):
        mocker.patch("flask_jwt._jwt_required", side_effect=lambda x: x)
        mocked_request = mocker.patch("flask_jwt._request_ctx_stack")
        mocked_request.top.current_identity = user
        response = app.post(
            f"/registration/2/",
        )
        assert "message" in response.json
        message = "Мероприятие не найдено"
        assert response.json["message"] == message
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_get_event_list(self, app, event_list):
        response = app.get(
            f"/event/",
        )
        json = response.json
        assert json is not None
        assert isinstance(json, list)
        event_1 = json[0]
        event_r1 = event_list[0]
        assert isinstance(event_1, dict)
        assert event_1["has_participants"] is True
        assert event_1["name"] == event_r1.name
        assert event_1["description"] == event_r1.description

    def test_get_single_event(self, app, single_event):
        user, event = single_event
        response = app.get(
            f"/event/{event.id}",
        )
        response_json = response.json
        assert response is not None
        assert isinstance(response_json, dict)
        assert response_json["id"] == event.id
        assert response_json["description"] == event.description
        assert "users" in response_json
        users = response_json["users"]
        assert isinstance(users, list)
        assert len(users) == 1
        user_from_server = users[0]
        assert user_from_server["id"] == user.id
        assert user_from_server["name"] == user.name
