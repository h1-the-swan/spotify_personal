# -*- coding: utf-8 -*-

DESCRIPTION = """Core for spotify_personal"""

import logging
from typing import List

root_logger = logging.getLogger()
logger = root_logger.getChild(__name__)

import spotipy
import pandas as pd
import numpy as np


class SpotifyPersonal:
    """SpotifyPersonal class"""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self.sp = sp

        self._playlists = None  # cached property, see below

    @property
    def playlists(self):
        if self._playlists is None:
            self._playlists = self.get_playlists()
        return self._playlists

    @playlists.setter
    def playlists(self, val):
        self._playlists = val

    @playlists.deleter
    def playlists(self):
        del self._playlists

    def get_full_results(self, fn, *args, **kwargs):
        r = fn(*args, **kwargs)
        items: List = r["items"]
        while r["next"]:
            r = self.sp.next(r)
            items.extend(r["items"])
        return items

    def get_playlists(self):
        # r = self.sp.current_user_playlists()
        # playlists: List = r['items']
        # while r['next']:
        #     r = self.sp.next(r)
        #     playlists.extend(r['items'])
        # return playlists
        return self.get_full_results(self.sp.current_user_playlists)

    def get_tracks_df(self, items: List) -> pd.DataFrame:
        d = []
        for item in items:
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
            ids = df_tracks.uri.iloc[offset : offset + step].dropna()
            if ids.empty:
                break
            r = self.sp.audio_features(ids)
            r = [x for x in r if x is not None]
            d.extend(r)
            offset += step
        df_audio_features = pd.DataFrame(d)
        df_audio_features.drop(
            columns=["type", "id", "track_href", "analysis_url", "duration_ms"],
            inplace=True,
        )
        df_tracks = df_tracks.merge(df_audio_features, how="left", on="uri")
        return df_tracks

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

    def get_playlist_uri_by_name(self, name: str) -> str:
        for p in self.playlists:
            if p["name"].lower() == name.lower():
                return p["uri"]
        raise ValueError(f"Playlist not found: {name}")
