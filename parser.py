import pandas as pd
import json
from collections import defaultdict

# File paths
handshake_file = r"C:\Users\Qasim Bedford\Documents\Harvest-Now-Decrypt-Later\tls_handshake.csv"
appdata_file = r"C:\Users\Qasim Bedford\Documents\Harvest-Now-Decrypt-Later\tls_appdata.csv"
output_file = r"C:\Users\Qasim Bedford\Documents\Harvest-Now-Decrypt-Later\tls_sessions_with_resumptions.json"

def load_tab_csv(path):
    return pd.read_csv(path, delimiter='\t', dtype=str).fillna("")

def build_session_key(row):
    return (row['ip.src'], row['ip.dst'], row['tcp.srcport'], row['tcp.dstport'])

def group_sessions(handshake_df, appdata_df):
    sessions = defaultdict(lambda: {"handshake": [], "appdata": [], "resumption_of": None, "missing_keys": False})
    session_ids = {}

    for _, row in handshake_df.iterrows():
        key = build_session_key(row)
        session_id = row.get("tls.handshake.session_id", "")

        if session_id and session_id not in session_ids:
            session_ids[session_id] = key

        missing_keys = (
            not row.get("tls.handshake.modulus") and
            not row.get("tls.handshake.extensions_key_share_key_exchange")
        )

        sessions[key]["handshake"].append(row.to_dict())
        sessions[key]["missing_keys"] |= missing_keys

    for _, row in appdata_df.iterrows():
        key = build_session_key(row)
        sessions[key]["appdata"].append(row.to_dict())

    for key, session in sessions.items():
        for record in session["handshake"]:
            session_id = record.get("tls.handshake.session_id", "")
            if session_id and session_ids.get(session_id) != key:
                session["resumption_of"] = session_ids.get(session_id)

    return {f"{k[0]}->{k[1]}:{k[2]}->{k[3]}": v for k, v in sessions.items()}

def main():
    handshake_df = load_tab_csv(handshake_file)
    appdata_df = load_tab_csv(appdata_file)
    session_dict = group_sessions(handshake_df, appdata_df)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(session_dict, f, indent=2)

    print(f"Session data saved to: {output_file}")

if __name__ == "__main__":
    main()
 # type: ignore