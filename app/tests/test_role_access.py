import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.db import db, connect_to_mongo, close_mongo_connection

pytestmark = pytest.mark.anyio


async def setup_data(client: AsyncClient):
    # Create org
    r = await client.post("/organizations/", json={"name": "Acme"})
    assert r.status_code == 201
    org = r.json()
    org_id = org["id"]

    # Create users
    r = await client.post(f"/organizations/{org_id}/users/", json={"email": "reader@acme.io", "role": "reader"})
    reader = r.json()
    r = await client.post(f"/organizations/{org_id}/users/", json={"email": "writer@acme.io", "role": "writer"})
    writer = r.json()
    r = await client.post(f"/organizations/{org_id}/users/", json={"email": "admin@acme.io", "role": "admin"})
    admin = r.json()
    return org_id, reader, writer, admin


@pytest.fixture(autouse=True, scope="module")
async def _db():
    await connect_to_mongo()
    # isolate DB name for tests if you wish
    yield
    # Cleanup after
    await db.notes.delete_many({})
    await db.users.delete_many({})
    await db.organizations.delete_many({})
    await close_mongo_connection()


def headers(org_id: str, user_id: str):
    return {"X-Org-ID": org_id, "X-User-ID": user_id}


async def create_note(client, org_id, user_id, title="Hello", content="World"):
    return await client.post("/notes/", headers=headers(org_id, user_id),
                             json={"title": title, "content": content})


@pytest.mark.anyio
async def test_rbac():
    async with AsyncClient(app=app, base_url="http://test") as client:
        org_id, reader, writer, admin = await setup_data(client)

        # Reader cannot create
        r = await create_note(client, org_id, reader["id"])
        assert r.status_code == status.HTTP_403_FORBIDDEN

        # Writer can create
        r = await create_note(client, org_id, writer["id"], "T1", "C1")
        assert r.status_code == 201
        note_id = r.json()["id"]

        # All roles can read list & detail
        for user in (reader, writer, admin):
            r = await client.get("/notes/", headers=headers(org_id, user["id"]))
            assert r.status_code == 200
            assert len(r.json()) >= 1

            r = await client.get(f"/notes/{note_id}", headers=headers(org_id, user["id"]))
            assert r.status_code == 200

        # Admin can delete
        r = await client.delete(f"/notes/{note_id}", headers=headers(org_id, admin["id"]))
        assert r.status_code == 204

        # Reader/writer cannot delete
        for user in (reader, writer):
            r = await client.delete(f"/notes/{note_id}", headers=headers(org_id, user["id"]))
            assert r.status_code == 403


@pytest.mark.anyio
async def test_tenant_isolation():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Org A
        r = await client.post("/organizations/", json={"name": "OrgA"});
        orgA = r.json()
        r = await client.post(f"/organizations/{orgA['id']}/users/", json={"email": "w@orga.io", "role": "writer"});
        ua = r.json()
        r = await client.post("/notes/", headers={"X-Org-ID": orgA["id"], "X-User-ID": ua["id"]},
                              json={"title": "A-only", "content": "secret"})

        # Org B + reader
        r = await client.post("/organizations/", json={"name": "OrgB"});
        orgB = r.json()
        r = await client.post(f"/organizations/{orgB['id']}/users/", json={"email": "r@orgb.io", "role": "reader"});
        ub = r.json()

        # Reader from B cannot see A's notes
        r = await client.get("/notes/", headers={"X-Org-ID": orgB["id"], "X-User-ID": ub["id"]})
        assert r.status_code == 200
        titles = [n["title"] for n in r.json()]
        assert "A-only" not in titles
