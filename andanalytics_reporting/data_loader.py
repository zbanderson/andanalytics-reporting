import pandas as pd
import numpy as np
from typing import Optional


def add_core_derived_metrics(df: pd.DataFrame, tz: str = "US/Eastern") -> pd.DataFrame:
    """
    Enrich a raw Meta Insights dataframe with core derived fields.

    Expects the dataframe to contain (where available):

        Required for best results:
            - 'timestamp'
            - 'reach'
            - 'likes'
            - 'comments'
            - 'saved'
            - 'shares'
            - 'views'
            - 'total_interactions'
            - 'ig_reels_video_view_total_time'
            - 'ig_reels_avg_watch_time'
            - 'follower_count_today'   (for per-follower metrics)

        It will create / overwrite these columns (if possible):
            - engagement_raw
            - total_interactions        (if not already present)
            - watch_time_seconds_total
            - watch_time_seconds_avg
            - watch_time_minutes_total
            - watch_seconds
            - avg_watch_seconds
            - watch_time_per_reach
            - engagement_rate
            - engagement_rate_pct
            - save_share_rate
            - save_share_rate_pct
            - view_through_rate
            - reach_per_follower
            - views_per_follower
            - saves_shares_per_100_followers
            - timestamp_est
            - hour
            - day_of_week
            - week
            - month
            - is_weekend
            - hours_since_prev_post
            - days_since_prev_post
            - time_of_day
    """
    df = df.copy()

    numeric_cols = [
        "reach",
        "likes",
        "comments",
        "saved",
        "shares",
        "views",
        "total_interactions",
        "ig_reels_video_view_total_time",
        "ig_reels_avg_watch_time",
        "follower_count_today",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    def _safe_div(num: pd.Series, den: pd.Series) -> pd.Series:
        return np.where(den.fillna(0) != 0, num / den, np.nan)

    # Fill NaNs with 0 for raw interactions
    for col in ["likes", "comments", "saved", "shares", "views"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # Engagement / interactions
    if all(c in df.columns for c in ["likes", "comments", "saved", "shares"]):
        df["engagement_raw"] = (
            df["likes"] + df["comments"] + df["saved"] + df["shares"]
        )
    else:
        df["engagement_raw"] = np.nan

    if "total_interactions" not in df.columns:
        df["total_interactions"] = df["engagement_raw"]

    if "reach" in df.columns:
        df["engagement_rate"] = _safe_div(df["engagement_raw"], df["reach"])
        df["engagement_rate_pct"] = df["engagement_rate"] * 100.0
    else:
        df["engagement_rate"] = np.nan
        df["engagement_rate_pct"] = np.nan

    if "reach" in df.columns and all(c in df.columns for c in ["saved", "shares"]):
        save_share = df["saved"] + df["shares"]
        df["save_share_rate"] = _safe_div(save_share, df["reach"])
        df["save_share_rate_pct"] = df["save_share_rate"] * 100.0
    else:
        df["save_share_rate"] = np.nan
        df["save_share_rate_pct"] = np.nan

    # Watch time
    if "ig_reels_video_view_total_time" in df.columns:
        df["watch_time_seconds_total"] = df["ig_reels_video_view_total_time"]
        df["watch_seconds"] = df["ig_reels_video_view_total_time"]
        df["watch_time_minutes_total"] = df["watch_time_seconds_total"] / 60.0
    else:
        df["watch_time_seconds_total"] = np.nan
        df["watch_seconds"] = np.nan
        df["watch_time_minutes_total"] = np.nan

    if "ig_reels_avg_watch_time" in df.columns:
        df["watch_time_seconds_avg"] = df["ig_reels_avg_watch_time"]
        df["avg_watch_seconds"] = df["ig_reels_avg_watch_time"]
    else:
        df["watch_time_seconds_avg"] = np.nan
        df["avg_watch_seconds"] = np.nan

    if "reach" in df.columns and "watch_time_seconds_total" in df.columns:
        df["watch_time_per_reach"] = _safe_div(
            df["watch_time_seconds_total"], df["reach"]
        )
    else:
        df["watch_time_per_reach"] = np.nan

    if "views" in df.columns and "reach" in df.columns:
        df["view_through_rate"] = _safe_div(df["views"], df["reach"])
    else:
        df["view_through_rate"] = np.nan

    # Per-follower metrics
    if "follower_count_today" in df.columns:
        fc = df["follower_count_today"].replace({0: np.nan})
        if "reach" in df.columns:
            df["reach_per_follower"] = df["reach"] / fc
        else:
            df["reach_per_follower"] = np.nan

        if "views" in df.columns:
            df["views_per_follower"] = df["views"] / fc
        else:
            df["views_per_follower"] = np.nan

        if all(c in df.columns for c in ["saved", "shares"]):
            df["saves_shares_per_100_followers"] = (
                (df["saved"] + df["shares"]) * 100.0 / fc
            )
        else:
            df["saves_shares_per_100_followers"] = np.nan
    else:
        df["reach_per_follower"] = np.nan
        df["views_per_follower"] = np.nan
        df["saves_shares_per_100_followers"] = np.nan

    # Time fields
    if "timestamp" in df.columns:
        ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
        ts_est = ts.dt.tz_convert(tz)

        df["timestamp"] = ts
        df["timestamp_est"] = ts_est

        df["hour"] = ts_est.dt.hour
        df["day_of_week"] = ts_est.dt.day_name()
        df["week"] = ts_est.dt.isocalendar().week.astype("Int64")
        df["month"] = ts_est.dt.to_period("M").astype(str)
        df["is_weekend"] = ts_est.dt.dayofweek >= 5

        df = df.sort_values("timestamp_est")

        diff = ts_est.diff()
        df["hours_since_prev_post"] = diff.dt.total_seconds() / 3600.0
        df["days_since_prev_post"] = df["hours_since_prev_post"] / 24.0

        bins = [-0.1, 6, 12, 18, 24]
        labels = ["Late Night", "Morning", "Afternoon", "Evening"]
        df["time_of_day"] = pd.cut(df["hour"], bins=bins, labels=labels)
    else:
        df["timestamp_est"] = pd.NaT
        df["hour"] = np.nan
        df["day_of_week"] = np.nan
        df["week"] = pd.Series([pd.NA] * len(df), dtype="Int64")
        df["month"] = np.nan
        df["is_weekend"] = np.nan
        df["hours_since_prev_post"] = np.nan
        df["days_since_prev_post"] = np.nan
        df["time_of_day"] = np.nan

    return df
