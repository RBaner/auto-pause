import asyncio
import time
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSession as SessionMananger
from winrt.windows.media.control import \
    PlaybackInfoChangedEventArgs as PlaybackEventArgs


async def get_media_info():
    sessions = await MediaManager.request_async()

    all_sessions = sessions.get_sessions()
    for current_session in all_sessions:
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(
            song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])
        print(current_session.source_app_user_model_id)
        for key in info_dict:
            print(f"{key}: {info_dict[key]}")
        info = current_session.get_playback_info()
        print(info.playback_status)


async def toggle_spotify():
    previous_state_spotify = 5
    previous_state_chrome = 5
    while True:
        start = time.time()
        sessions = await MediaManager.request_async() #grab session manager instance

        all_sessions = sessions.get_sessions() #grab sequence of current instances
        for current_session in all_sessions: #iterate and grab desired instances
            if "chrome" in current_session.source_app_user_model_id.lower():
                chrome_info = current_session.get_playback_info()
            if "spotify" in current_session.source_app_user_model_id.lower():
                spotify_manager = current_session 
                spotify_info = current_session.get_playback_info()
        current_state_spotify = spotify_info.playback_status
        current_state_chrome = chrome_info.playback_status
        if current_state_chrome == 5:
            if previous_state_chrome == 4 and previous_state_spotify == 4:
                await spotify_manager.try_toggle_play_pause_async()
            previous_state_chrome = chrome_info.playback_status
            continue
        elif current_state_chrome == 4: #status of 4 is playing, 5 is paused
            if current_state_spotify == 4:
                await spotify_manager.try_toggle_play_pause_async()
                previous_state_spotify = 4
            elif current_state_spotify == 5 and previous_state_chrome == 5:
                previous_state_spotify = 5
            previous_state_chrome = 4
        previous_state_chrome = chrome_info.playback_status
        end = time.time()
        # previous_state_spotify = spotify_info.playback_status
        time.sleep(1)
        print(end-start)
        # print(f"chrome playback status: {chrome_info.playback_status}")
        # print(f"chrome playback status: {spotify_info.playback_status}")
        # print("+++++++++++++++++")
        # time.sleep(2)


async def test_event():
    sessions = await MediaManager.request_async()
    all_sessions = sessions.get_sessions()
    for current_session in all_sessions:  # there needs to be a media session running
        if "chrome" in current_session.source_app_user_model_id.lower():
            chrome_mananger = current_session
        if "spotify" in current_session.source_app_user_model_id.lower():
            spotify_info = current_session

if __name__ == '__main__':
    #asyncio.run(get_media_info())
    asyncio.run(toggle_spotify())
