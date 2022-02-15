import asyncio
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus,
    SessionsChangedEventArgs,
)

async def update_sessions(manager: SessionManager) -> None:
    for session in manager.get_sessions():
        if "chrome" in session.source_app_user_model_id.lower():
            chrome_info = session.get_playback_info()
            if chrome_info.playback_status == PlaybackStatus.PLAYING:
                ...


def handle_sessions_changed(manager: SessionManager, args: SessionsChangedEventArgs) -> None:
    asyncio.create_task(update_sessions(manager))


async def main():
    manager = await SessionManager.request_async()

    # add callback to handle any future changes
    sessions_changed_token = manager.add_sessions_changed(handle_sessions_changed)

    try:
        # handle current state
        asyncio.create_task(update_sessions(manager))

        event = asyncio.Event()
        # wait forever - a real app would call event.set() to end the app
        await event.wait()
    finally:
        # remove the callback
        manager.remove_sessions_changed(sessions_changed_token)

if __name__ == '__main__':
    asyncio.run(main())
