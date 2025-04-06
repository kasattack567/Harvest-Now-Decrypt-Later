from typing import Any

import pandas as pd
import json
from collections import defaultdict

# File paths
handshake_file = r"tls_handshake.csv"
appdata_file = r"tls_appdata.csv"
output_file = r"tls_sessions_with_resumptions.json"


def load_tab_csv(path: str) -> pd.DataFrame:
    """
    Returns a DataFrame converted from the CSV file.
    :param path: File path of the CSV file.
    :return: DataFrame converted from the CSV file.
    """
    return pd.read_csv(filepath_or_buffer=path, delimiter='\t', dtype=str).fillna(value="")


def build_session_key(row) -> tuple[str, str, str, str]:
    """
    Build session key
    :param row: dataframe row
    :return: session key
    """
    return row['ip.src'], row['ip.dst'], row['tcp.srcport'], row['tcp.dstport']


def group_sessions(handshake_df: pd.DataFrame, appdata_df: pd.DataFrame) -> dict[str, dict[str, list | None | bool]]:
    """
    Group sessions
    :param handshake_df: Handshake DataFrame
    :param appdata_df: Application DataFrame
    :return: Dictionary of session keys
    """
    sessions: defaultdict[Any, dict[str, list | None | bool]] = defaultdict(
        lambda: {"handshake": [], "appdata": [], "resumption_of": None, "missing_keys": False})
    session_ids: dict = {}

    for _, row in handshake_df.iterrows():
        key: tuple[str, str, str, str] = build_session_key(row=row)
        session_id: str = row.get(key="tls.handshake.session_id", default="")

        if session_id and session_id not in session_ids:
            session_ids[session_id]: str = key

        missing_keys: bool = (
                not row.get(key="tls.handshake.modulus") and
                not row.get(key="tls.handshake.extensions_key_share_key_exchange")
        )

        sessions[key]["handshake"].append(row.to_dict())
        sessions[key]["missing_keys"] |= missing_keys

    for _, row in appdata_df.iterrows():
        key: tuple[str, str, str, str] = build_session_key(row=row)
        sessions[key]["appdata"].append(row.to_dict())

    for key, session in sessions.items():
        for record in session["handshake"]:
            session_id: str = record.get("tls.handshake.session_id", "")
            if session_id and session_ids.get(session_id) != key:
                session["resumption_of"] = session_ids.get(session_id)

    return {f"{k[0]}->{k[1]}:{k[2]}->{k[3]}": v for k, v in sessions.items()}


def main() -> None:
    handshake_df: pd.DataFrame = load_tab_csv(path=handshake_file)
    appdata_df: pd.DataFrame = load_tab_csv(path=appdata_file)
    session_dict: dict[str, dict[str, list | None | bool]] = group_sessions(handshake_df=handshake_df, appdata_df=appdata_df)

    with open(file=output_file, mode='w', encoding='utf-8') as f:
        json.dump(obj=session_dict, fp=f, indent=2)

    print(f"Session data saved to: {output_file}")


if __name__ == "__main__":
    main()
