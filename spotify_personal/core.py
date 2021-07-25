# -*- coding: utf-8 -*-

DESCRIPTION = """Core for spotify_personal"""

import logging
root_logger = logging.getLogger()
logger = root_logger.getChild(__name__)

import spotipy
import pandas as pd
import numpy as np


class SpotifyPersonal:
    """SpotifyPersonal class"""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self.sp = sp

    def get_saved_tracks_df(self) -> pd.DataFrame:
        saved_tracks = []
        offset = 0
        while True:
            response = self.sp.current_user_saved_tracks(offset=offset)
            items = response["items"]
            if len(items) == 0:
                break
            saved_tracks.extend(items)
            offset += len(items)
            # print(f"{offset}/{response['total']}")
        # print(f"{len(saved_tracks)} tracks collected")
        d = []
        for item in saved_tracks:
            t = item["track"]
            d.append(
                {
                    "added_at": item["added_at"],
                    "uri": t["uri"],
                    "name": t["name"],
                    "popularity": t["popularity"],
                    "duration_ms": t["duration_ms"],
                    "artist_1_name": t["artists"][0]["name"],
                }
            )
        df_tracks = pd.DataFrame(d)
        d = []
        offset = 0
        step = 100
        while True:
            ids = df_tracks.uri.iloc[offset : offset + step]
            if ids.empty:
                break
            r = self.sp.audio_features(ids)
            d.extend(r)
            offset += step
        df_audio_features = pd.DataFrame(d)
        df_audio_features.drop(
            columns=["type", "id", "track_href", "analysis_url", "duration_ms"],
            inplace=True,
        )
        df_tracks = df_tracks.merge(df_audio_features, how="left", on="uri")
        return df_tracks
