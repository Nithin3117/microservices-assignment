import os
import json
import nats

NATS_URL = os.getenv("NATS_URL", "nats://nats:4222")


async def start_nats(app):
    print(f"NATS: connecting to {NATS_URL}")

    try:
        nc = await nats.connect(NATS_URL)

        print("NATS: connection successful")

        async def message_handler(msg):
            data = json.loads(msg.data.decode())

            print(
                f"NATS: user.created received for user {data['user_id']}"
            )

            notification = app.state.db_session()

            try:
                from models import Notification

                new_notification = Notification(
                    user_id=data["user_id"],
                    message=f"Welcome {data['name']}! Your account has been created.",
                    type="WELCOME",
                    status="SENT"
                )

                notification.add(new_notification)
                notification.commit()

                print(
                    f"Notification created for user {data['user_id']}"
                )

            finally:
                notification.close()

        await nc.subscribe(
            "user.created",
            cb=message_handler
        )

        await nc.flush()

        print("NATS: subscribed to user.created")

        app.state.nats = nc

    except Exception as e:
        print(f"NATS ERROR: {e}")
        raise