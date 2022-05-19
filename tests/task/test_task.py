import json
import pytest
from data import tasks

# obtener lista de tareas
def test_get_tasks(client):
    response = client.get("/tareas")
    assert response.status_code == 200

# agregar tarea (y comprobar persistencia)
def test_create_task(client):
    newTask = {"title": "tarea 1", "description": "hacer algo", "status": "Problemas"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    body = response.json()
    assert body.get("title") and body["title"] == "tarea 1"
    assert body.get("description") and body["description"] == "hacer algo"
    assert body.get("status") and body["status"] == "Problemas"
    assert body.get("id")
    response = client.get("/tareas")
    assert response.status_code == 200
    assert body in response.json()

# casos borde: descripcion nula (es opcional), otros campos nulos
def test_create_task2(client):
    newTask = {"title": "tarea 2", "description": None, "status": "Problemas"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    assert response.json()["description"] == None

    newTask = {"title": "tarea 3", "status": "Problemas"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    assert response.json()["description"] == None

    newTask = {"title": None, "status": "Problemas"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code != 200

    newTask = {"title": "tarea 5", "status": None}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code != 200

# casos borde que deben leventar un error
# (notar que todos los campos se convierten a str, así que no hay TypeError)
def test_create_error(client):
    with pytest.raises(ValueError) as error:
        newTask = {"title": "tarea 6", "status": "Retrasado"}
        client.post("/tareas/", json.dumps(newTask))

    with pytest.raises(ValueError) as error:
        newTask = {"title": "tarea 6", "status": 5}
        client.post("/tareas/", json.dumps(newTask))

# modificar y eliminar tarea
def test_update_task(client):
    newTask = {"title": "tarea 6", "description": "Una cosa mas", "status": "Problemas"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    body = response.json()
    id = body["id"]
    response = client.put(f"/tareas/{id}?category=Trabajando")
    assert response.status_code == 200
    assert response.json()["status"] == "Trabajando"

    body["status"] = "Trabajando"
    response = client.delete(f"/tareas/{id}")
    assert response.status_code == 200
    response = client.get("/tareas")
    assert body not in response.json()

# probar filtro de la BBDD
def test_filter(client):
    for t in tasks:
        response = client.post("/tareas/", json.dumps(t))
        assert response.status_code == 200

    response = client.get("/tareas/Problemas")
    for t in response.json():
        assert t["status"] == "Problemas"

    response = client.get("/tareas/Trabajando")
    for t in response.json():
        assert t["status"] == "Trabajando"

    response = client.get("/tareas/Listo")
    for t in response.json():
        assert t["status"] == "Listo"
