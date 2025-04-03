import pandas as pd
import json

# File paths – update if needed
handshake_file = r"C:\Users\Qasim Bedford\Documents\Harvest-Now-Decrypt-Later\tls_handshake.csv"
appdata_file = r"C:\Users\Qasim Bedford\Documents\Harvest-Now-Decrypt-Later\tls_appdata.csv"
output_file = r"C:\Users\Qasim Bedford\Documents\Harvest-Now-Decrypt-Later\tls_sessions.json"

def load_csv(file_path):
    return pd.read_csv(file_path, delimiter="\t")

def build_session_key(row):
    """
    Tries to construct a session identifier from the row.
    Prefers 'tls.handshake.session_id', else falls back to ip:port-based tuple.
    """
    session_id = row.get("tls.handshake.session_id")
    if pd.notna(session_id) and session_id.strip() != "":
        return f"session_{session_id.strip()}"
    # fallback: 5-tuple or ip pair
    return f"{row.get('ip.src', '')}->{row.get('ip.dst', '')}"

def group_sessions(handshake_df, appdata_df):
    sessions = {}

    for _, row in handshake_df.iterrows():
        key = build_session_key(row)
        if key not in sessions:
            sessions[key] = {"handshake": [], "appdata": []}
        sessions[key]["handshake"].append(row.dropna().to_dict())

    for _, row in appdata_df.iterrows():
        key = build_session_key(row)
        if key not in sessions:
            sessions[key] = {"handshake": [], "appdata": []}
        sessions[key]["appdata"].append(row.dropna().to_dict())

    return sessions

def main():
    handshake_df = load_csv(handshake_file)
    appdata_df = load_csv(appdata_file)
    sessions = group_sessions(handshake_df, appdata_df)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2)

    print(f"TLS session data written to: {output_file}")

if __name__ == "__main__":
    main()
 # type: ignore