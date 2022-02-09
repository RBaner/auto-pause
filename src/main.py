import asyncio
import time
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSession as SessionMananger
from winrt.windows.media.control import \
    PlaybackInfoChangedEventArgs as PlaybackEventArgs

#this is a snippet of what other info is available from session instances
#credit to tameTNT (https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python)
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
        sessions = await MediaManager.request_async() #grab session manager instance

        all_sessions = sessions.get_sessions() #grab sequence of current instances
        for current_session in all_sessions: #iterate and grab desired instances
            if "chrome" in current_session.source_app_user_model_id.lower():
                current_state_chrome = current_session.get_playback_info().playback_status
            if "spotify" in current_session.source_app_user_model_id.lower():
                spotify_manager = current_session 
                current_state_spotify = current_session.get_playback_info().playback_status
        # state of 4 is playing, 5 is paused
        if current_state_chrome == previous_state_chrome: #chrome state hasn't changed
            time.sleep(1)
            continue
        elif current_state_chrome == 5 and previous_state_chrome == 4: #chrome just paused
            if previous_state_spotify == 4:
                await spotify_manager.try_toggle_play_pause_async()
            previous_state_chrome = current_state_chrome
            time.sleep(1)
            continue
        elif current_state_chrome == 4 and previous_state_chrome == 5: #chrome just started playing
            if current_state_spotify == 4:
                await spotify_manager.try_toggle_play_pause_async()
                previous_state_spotify = 4
            else:
                previous_state_spotify = 5
            previous_state_chrome = 4
            time.sleep(1)
            continue
        # print(f"chrome playback status: {chrome_info.playback_status}")
        # print(f"chrome playback status: {spotify_info.playback_status}")
        # print("+++++++++++++++++")

if __name__ == '__main__':
    asyncio.run(toggle_spotify())
