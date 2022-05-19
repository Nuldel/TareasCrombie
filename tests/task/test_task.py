import json

def test_create_task(client):
    newTask = {"title": "tarea 1", "description": "hacer algo", "status": "Problemas"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    assert response.json()["title"] == "tarea 1"
    assert response.json()["description"] == "hacer algo"
    assert response.json()["status"] == "Problemas"

def test_get_tasks(client):
    response = client.get("/tareas")
    assert response.status_code == 200
