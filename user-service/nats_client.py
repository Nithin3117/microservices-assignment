import os
import json
import nats

NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")


async def connect_nats():
    return await nats.connect(NATS_URL)


async def publish_user_created(user_id: int, name: str, email: str):
    nc = await connect_nats()

    message = {
        "event": "user.created",
        "user_id": user_id,
        "name": name,
        "email": email
    }

    await nc.publish(
        "user.created",
        json.dumps(message).encode()
    )

    await nc.flush()

    print(f"NATS: user.created published for user {user_id}")

    await nc.close()