import asyncio
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    #GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus,
    SessionsChangedEventArgs,
)



async def update_sessions(manager: SessionManager) -> None:
    global previous_state_spotify
    for current_session in manager.get_sessions(): #iterate and grab desired instances
        if "chrome" in current_session.source_app_user_model_id.lower():
            current_state_chrome = current_session.get_playback_info().playback_status
        if "spotify" in current_session.source_app_user_model_id.lower():
            spotify_manager = current_session 
            current_state_spotify = current_session.get_playback_info().playback_status
    if current_state_chrome == 4 and current_state_spotify == 4:
        previous_state_spotify = 4
        await spotify_manager.try_pause_async()
    elif current_state_chrome == 5:
        if previous_state_spotify == 4:
            await spotify_manager.try_play_async()
        else:
            await spotify_manager.try_pause_async()

def handle_sessions_changed(manager: SessionManager, args: SessionsChangedEventArgs) -> None:
    asyncio.create_task(update_sessions(manager))


async def main():
    manager = await SessionManager.request_async()


    while True:
        # add callback to handle any future changes
        sessions_changed_token = manager.add_sessions_changed(handle_sessions_changed)
        try:
            # handle current state
            asyncio.create_task(update_sessions(manager))

        finally:
            # remove the callback
            manager.remove_sessions_changed(sessions_changed_token)

if __name__ == '__main__':
    previous_state_spotify = 5
    asyncio.run(main())
