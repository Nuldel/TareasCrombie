import json
import pytest

# casos borde del registro/inicio de sesion (lo demas se hace en test_task.py)
def test_user(client):
    # formato de email
    newUser = {"name": "FranMa", "email": "franMa26outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code != 200

    # campos faltantes
    newUser = {"name": None, "email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code != 200

    newUser = {"email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code != 200

    newUser = {"name": "FranMa", "email": "franMa26@outlook.com"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code != 200

    newUser = {"name": "FranMa", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code != 200

    # registro con el mismo mail
    newUser = {"name": "FranMa", "email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code == 200

    newUser = {"name": "Franco", "email": "franMa26@outlook.com", "password": "Franquito47"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code != 200

    # registro con token previo valido
    user = {"email": "franMa26@outlook.com", "password": "FranMa1234X"}
    response = client.post("/usuarios/entrar", json.dumps(user))
    assert response.status_code == 200

    newUser = {"name": "FranMa", "email": "franMa27@outlook.com", "password": "Franquito47"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code != 200

    # dejamos una tarea privada con el owner actual
    newTask = {"title": "tarea 1",
               "description": "hacer algo",
               "status": "Problemas",
               "visibility": "Privado"}
    response = client.post("/tareas/", json.dumps(newTask))
    assert response.status_code == 200
    task = response.json()

    # registro con mismo nombre
    response = client.post("/usuarios/salir")
    assert response.status_code == 200

    newUser = {"name": "FranMa", "email": "franMa27@outlook.com", "password": "Franquito47"}
    response = client.post("/usuarios/registrar/", json.dumps(newUser))
    assert response.status_code == 200

    del newUser["name"]
    response = client.post("/usuarios/entrar", json.dumps(newUser))
    assert response.status_code == 200

    # la tarea anterior no deberia verse (el dueño es distinto)
    response = client.get("/tareas")
    assert response.status_code == 200
    assert task not in response.json()

    # tampoco se puede modificar ni eliminar la tarea
    task_id = task["id"]
    response = client.put(f"/tareas/{task_id}?category=Trabajando&visibility=Público")
    assert response.status_code != 200

    response = client.delete(f"/tareas/{task_id}")
    assert response.status_code != 200

    response = client.post("/usuarios/salir")
    assert response.status_code == 200
