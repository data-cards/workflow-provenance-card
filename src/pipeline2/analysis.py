import matplotlib.pyplot as plt
import xarray as xr
from tqdm import tqdm
import pandas as pd
from pathlib import Path
import shutil
import os
import time
import numpy as np
import torch
import sys
sys.path.append("/Users/gabrielepadovani/Desktop/Università/yProv4ML")
import yprov4ml
from flowcept import Flowcept, FlowceptTask

def run_step4(): 

    os.system(f"rm -rf prov")

    DST_JSON_PATH = Path("pipeline2_output/jsons")
    os.makedirs(DST_JSON_PATH, exist_ok=True)


    yprov4ml.start_run(
        prov_user_namespace="www.example.org",
        experiment_name=f"analysis", 
        provenance_save_dir="prov",
        disable_codecarbon=True, 
        metrics_file_type="csv",
    )

    yprov4ml.log_source_code()
    yprov4ml.log_execution_command(cmd="python", path="src/pipeline2/04_analysis.py")

    flowcept = Flowcept(workflow_name="finetuning", workflow_id="finetuning")
    flowcept.start()

    torch.save(torch.tensor([1,2,3]), "input_tensor.pt")
    yprov4ml.log_artifact("input_tensor_0", "input_tensor.pt", is_input=True, log_copy_in_prov_directory=False)
    yprov4ml.log_artifact("input_tensor_1", "input_tensor.pt", is_input=True, log_copy_in_prov_directory=False)
    yprov4ml.log_artifact("input_tensor_2", "input_tensor.pt", is_input=True, log_copy_in_prov_directory=False)
    yprov4ml.log_artifact("input_tensor_3", "input_tensor.pt", is_input=True, log_copy_in_prov_directory=False)

    PATH = Path("forecasts")
    paths = list(PATH.rglob("*.nc"))
    paths = sorted(paths)[0::8] # sample every 8 cause it does not fit in mem

    def simulate_xarray_alignment(num_files=20, steps_per_file=50, var_dim=(12, 64, 64)):
        target_sim = np.random.rand(29000).astype(np.float32) 
        all_results_size = 0
        for i in tqdm(range(num_files), desc="Processing NetCDF files"):
            time.sleep(0.2) 
            _ = np.zeros((steps_per_file, *var_dim))
            for _ in range(5):
                _ = np.random.rand(100, 100).T
            fake_ds = np.random.rand(steps_per_file, *var_dim).astype(np.float32)
            fake_target = np.random.rand(steps_per_file, *var_dim).astype(np.float32)
            diff = fake_ds - fake_target
            all_results_size += diff.nbytes
            time.sleep(0.05)

    # _targets = xr.open_zarr("hpx64_1983-2017_3h_9varCoupledAtmos-sst.zarr")["targets"]
    # targets = _targets.sel(channel_out=VAR)
    # targets = targets.sel(time=slice("2000", "2010"))
    # all_gts = []
    # for path in tqdm(paths): 
    #     ds = xr.open_dataset(path)
    #     valid_times = ds.time + ds.step
    #     ds = ds.assign_coords(valid_time=valid_times)
    #     ds = ds[VAR].stack(sample=("time", "step")).swap_dims({"sample": "valid_time"})
    #     target = targets.sel(time=ds["valid_time"] + pd.Timedelta(hours=6), method="nearest")
    #     target = target.transpose('face', 'height', 'width', 'valid_time')
    #     all_gts.append(ds - target)
    # all_gts = xr.concat(all_gts, dim="valid_time").sortby("valid_time").drop_vars(["sample"])#.to_dataset(name=VAR)

    t3 = FlowceptTask(activity_id=f"elaboration", agent_id="gabrielepadovani")
    simulate_xarray_alignment()

    t3.end(generated={"w": 1})

    yprov4ml.log_system_metrics(context="elaboration", step=0)

    t3 = FlowceptTask(activity_id=f"analysis", agent_id="gabrielepadovani")

    scores = [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]]

    # 2. 2x6 Grid for Scores and Components
    # We use a wide figsize because we have 6 columns
    fig, axes = plt.subplots(1, 6, figsize=(24, 8), constrained_layout=True)

    for i, mode in enumerate(range(1, 7)):
        # --- Top Row: Scores (Time Series) ---
        ax_score = axes[i]
        # Using .values to avoid the coordinate misalignment issue you found
        ax_score.plot(scores[i-1], lw=1)
        ax_score.set_title(f"Mode {mode} - Score")
        ax_score.set_xlabel("Time Index")
        
    # Save the entire grid to one PDF
    plt.savefig("error_modes_2x6.pdf", dpi=300)
    plt.close()

    yprov4ml.log_dataset("targets", {})
    yprov4ml.log_dataset("inferences", {})
    yprov4ml.log_system_metrics(context="analysis", step=0)
    with open("results.csv", "w") as f: 
        f.write("ciao mamma" * 150)
    yprov4ml.log_artifact("results", "results.csv", log_copy_in_prov_directory=False)

    t3.end(generated={"w": 1})
    yprov4ml.end_run()
    flowcept.stop()

    provpath = Path("prov")
    srcpath = provpath / os.listdir(provpath)[0]
    dstpath = DST_JSON_PATH / "analysis_yprov/"#os.listdir(provpath)[0]
    if dstpath.exists(): 
        os.system(f"rm -rf {dstpath}")
    shutil.move(srcpath, dstpath)

    flowceptpath = Path("flowcept_buffer.jsonl")
    dstpath = DST_JSON_PATH / "analysis_flowcept.jsonl"
    shutil.move(flowceptpath, dstpath)

    os.system(f"rm -rf prov")
    os.system(f"rm results.csv")
    os.system(f"rm input_tensor.pt")
    os.system(f"rm error_modes_2x6.pdf")

