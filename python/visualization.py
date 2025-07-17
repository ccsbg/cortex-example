import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def load_emotiv_csv(path: str):
    with open(path, "r", encoding="utf-8") as f:
        meta_line = f.readline().strip()

    metadata = {}
    for pair in meta_line.split(","):
        pair = pair.strip()
        if ":" in pair:
            k, v = pair.split(":", 1)
            metadata[k.strip()] = v.strip()

    df = pd.read_csv(
        path,
        skiprows=1,         
        engine="python",     
    )

    df = df.loc[:, ~df.columns.str.match(r"Unnamed")]

    df["Timestamp"] = pd.to_numeric(df["Timestamp"], errors="coerce")
    df["Datetime"]  = pd.to_datetime(df["Timestamp"], unit="s")  
    return metadata, df

def plot_metrics(df: pd.DataFrame, metrics: list[str] | None = None, x_axis: str = "Datetime", save_root: str | None = None, title_prefix: str = ""):
    sns.set_theme(style="whitegrid")
    os.makedirs(save_root, exist_ok=True) if save_root else None

    if metrics is None:
        metrics = [
            c for c in df.columns
            if c not in ("Timestamp", "Datetime") and pd.api.types.is_numeric_dtype(df[c])
        ]

    for col in metrics:
        plt.figure(figsize=(12, 5))
        plt.plot(df[x_axis], df[col])
        plt.xlabel("Time" if x_axis == "Datetime" else "Epoch seconds")
        plt.ylabel(col)
        plt.title(f"{title_prefix}{col}")
        plt.tight_layout()

        if save_root:
            fname = f"{title_prefix}{col}.png".replace("/", "_")
            plt.savefig(os.path.join(save_root, fname))
            plt.close()
        else:
            plt.show()

def plot_all_recordings(folder_path: str = "recordings_csv",
                        start_time: float | None = None,
                        end_time:   float | None = None,
                        output_folder: str = "recording_graphs",
                        metrics: list[str] | None = None,
                        use_datetime: bool = True):

    for fname in os.listdir(folder_path):
        if not fname.lower().endswith(".csv"):
            continue

        meta, df = load_emotiv_csv(os.path.join(folder_path, fname))

        if start_time is not None:
            df = df[df["Timestamp"] >= start_time]
        if end_time is not None:
            df = df[df["Timestamp"] <= end_time]
        if df.empty:
            print(f"Skipping {fname}: no data in requested window.")
            continue

        x_axis = "Datetime" if use_datetime else "Timestamp"
        title_prefix = f"{os.path.splitext(fname)[0]}_"
        save_dir = os.path.join(output_folder, os.path.splitext(fname)[0])
        plot_metrics(df, metrics, x_axis=x_axis, save_root=save_dir, title_prefix=title_prefix)
        print(f"Plots for {fname} saved to {save_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default="recordings_csv")
    parser.add_argument("--output", default="recording_graphs")
    parser.add_argument("--start", type=float, default=None)
    parser.add_argument("--end", type=float, default=None)
    parser.add_argument("--metrics", nargs="+", default=None)
    parser.add_argument("--no_datetime", action="store_true")
    args = parser.parse_args()

    plot_all_recordings(
        folder_path=args.folder,
        start_time=args.start,
        end_time=args.end,
        output_folder=args.output,
        metrics=args.metrics,
        use_datetime=not args.no_datetime
    )
