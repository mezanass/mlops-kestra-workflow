from pathlib import Path
import os
import hydra
import pandas as pd
from helpers import save_data
from omegaconf import DictConfig


def get_files_in_a_directory(dir_path: str):
    dir_ = Path(dir_path)
    return dir_.glob("*.csv")


def merge_files(csv_files: list):
    print("Merging the following files:")
    dfs = []
    for file in csv_files:
        print(file.name)
        dfs.append(pd.read_csv(file))
    return pd.concat(dfs, ignore_index=True)


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def merge_data(config: DictConfig):
    if config.prefix =='detect':
        merge_path =config.detect.data.current
        files_dir =config.s3.raw.detect.local_path
    else:
        merge_path =config.data.merged.path 
        files_dir =config.data.raw.dir   


    csv_files = get_files_in_a_directory(files_dir)
    merged_df = merge_files(csv_files)
    print(f'{merge_path=}')
    print(f'{files_dir=}')
    print(f'csv_files', [f.name for f in csv_files])
    print(f'{merged_df.shape=}')
    

    save_data(merged_df, merge_path)

    print('data/final', os.listdir('data/final'))
    print('data/detect', os.listdir('data/detect'))


if __name__ == "__main__":
    merge_data()
