
import sys
sys.path.append("src")

# from pipeline2.ai_ready_dataset import run_step1
# from pipeline2.finetune_model import run_step2
# from pipeline2.run_inferences import run_step3
# from pipeline2.analysis import run_step4


import torch
import shutil
import os
from pathlib import Path
import sys
sys.path.append("/Users/gabrielepadovani/Desktop/Università/yProv4ML")
import yprov4ml
from flowcept import Flowcept, FlowceptTask

import os
from pathlib import Path
import shutil
import sys
sys.path.append("../redi/")

def run_step1(): 
    # Reset env
    os.system("rm -rf pipeline2_output")

    DST_DATACARDS_PATH = Path("pipeline2_output/datacards")
    os.makedirs(DST_DATACARDS_PATH, exist_ok=True)
    DST_JSON_PATH = Path("pipeline2_output/jsons")
    os.makedirs(DST_JSON_PATH, exist_ok=True)

    OUT_DIR = Path("tmp/")
    os.makedirs(OUT_DIR, exist_ok=True)
    INP_DIR = Path("../jan2017_hpx64_9varCoupledAtmos-sst.zarr")


    from redi.cli import run_pipeline
    # command = f"redi run -o {OUT_DIR} {INP_DIR}"
    # os.system(command)
    run_pipeline(input_path=INP_DIR, output_dir=OUT_DIR)

    # Retrieve provenance zip for yProv
    # prov_save_path
    provpath = Path("prov_save_path")
    srcpath = provpath / os.listdir(provpath)[0]
    dstpath = DST_JSON_PATH / "redi_yprov/"#os.listdir(provpath)[0]
    shutil.move(srcpath, dstpath)

    # Retrieve jsonl from flowcept
    # flowceptpath = Path("flowcept_buffer.jsonl")
    # dstpath = DST_JSON_PATH / "redi_flowcept.jsonl"
    # shutil.move(flowceptpath, dstpath)

    # Get datacard from redi
    redicardpath = Path("DATA_CARD.md")
    dstpath = DST_DATACARDS_PATH / "redi_datacard.md"
    shutil.move("tmp/" / redicardpath, dstpath)

    # Cleanup stuff from exec
    os.system(f"rm -rf {provpath}")

    # if flowceptpath.exists(): 
    #     os.remove(flowceptpath)
    # if ("tmp/" / redicardpath).exists(): 
    #     os.remove("tmp/" / redicardpath)
    # os.remove("DomainInference.jsonl")
    # os.remove("InputFilesValidation.jsonl")
    # os.remove("OutputGeneration.jsonl")
    # os.remove("PipelineCreation.jsonl")
    # os.remove("PipelineExecution.jsonl")
    # os.remove("PipelineFinalize.jsonl")
    # os.remove("flowcept_buffer.jsonl")
    os.system(f"rm -rf tmp")

import torch
import time
import shutil
import os
from multiprocessing import Process
from pathlib import Path
import sys
sys.path.append("/Users/gabrielepadovani/Desktop/Università/yProv4ML")
import yprov4ml
from flowcept import Flowcept, FlowceptTask

def simulate_cpu_load(duration_sec):
    end_time = time.time() + duration_sec
    while time.time() < end_time:
        _ = [x**2 for x in range(1000)]
        
def run_step2(): 

    DST_JSON_PATH = Path("pipeline2_output/jsons")
    os.makedirs(DST_JSON_PATH, exist_ok=True)


    def fake_finetune(batch_size=32, model_dim=4096, model_depth=20, epochs=1, batches_per_epoch=20):

        os.system(f"rm -rf prov")

        yprov4ml.start_run(
            prov_user_namespace="www.example.org",
            experiment_name=f"finetuning",
            provenance_save_dir="prov",
            disable_codecarbon=True,
            metrics_file_type="csv",
        ) 
        model = torch.nn.Linear(1,1)
        torch.save(model, "dlesym_pretrained.pt")
        yprov4ml.log_model("dlesym_pretrained", model, is_input=True)
        yprov4ml.log_source_code()
        yprov4ml.log_execution_command(cmd="python", path="src/pipeline2/02_finetune_model.py")

        # flowcept = Flowcept(workflow_name="finetuning", save_workflow=False, workflow_id="finetuning")
        # flowcept.start()

        t3 = FlowceptTask(activity_id=f"preprocess", agent_id="gabrielepadovani")

        # --- Device Selection ---
        if torch.backends.mps.is_available():
            device_type = "mps"
            sync_func = torch.mps.synchronize
            print("--- Using Apple Silicon (MPS) ---")
        elif torch.cuda.is_available():
            device_type = "cuda"
            sync_func = torch.cuda.synchronize
            print("--- Using NVIDIA GPU (CUDA) ---")
        else:
            device_type = "cpu"
            sync_func = lambda: None
            print("--- Using CPU (Simulation will be slow) ---")
        device = torch.device(device_type)

        # 1. Allocate VRAM (or System RAM shared by Unified Memory on Mac)
        print(f"Allocating ~{(model_dim**2 * 4 * 2) / 1e9:.2f} GB of memory...")
        fake_model_weights = torch.randn((model_dim, model_dim), device=device)
        fake_optimizer_state = torch.randn((model_dim, model_dim), device=device)

        t3.end(generated={"w": 1})
        yprov4ml.log_system_metrics(context="preprocess", step=0) 
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            
            t3 = FlowceptTask(activity_id=f"epoch {epoch}", used={"z": 1}, agent_id="gabrielepadovani")

            for _ in range(batches_per_epoch):
                cpu_proc = Process(target=simulate_cpu_load, args=(0.2,))
                cpu_proc.start()

                for _ in range(model_depth):
                    # Using matmul to stress the GPU cores
                    _ = torch.matmul(fake_model_weights, fake_model_weights)
                
                sync_func() # Critical to wait for the GPU to actually finish
                            
                cpu_proc.join()
                time.sleep(0.05) 

            t3.end(generated={"w": 1})
            
            yprov4ml.log_system_metrics(context="finetune", step=epoch) 
                
        t3 = FlowceptTask(activity_id=f"save", agent_id="gabrielepadovani")

        model = torch.nn.Linear(1,1)
        torch.save(model, "dlesym.pt")
        yprov4ml.log_model("dlesym", model, context="finetune", is_input=False)
        yprov4ml.log_dataset("era5_redi", None, log_dataset_info=False)

        # Cleanup
        del fake_model_weights
        del fake_optimizer_state
        if device_type == "mps":
            torch.mps.empty_cache()
        elif device_type == "cuda":
            torch.cuda.empty_cache()

        t3.end(generated={"w": 1})
        yprov4ml.log_system_metrics(context="save", step=epoch) 

        yprov4ml.end_run()
        # flowcept.stop()


        provpath = Path("prov")
        srcpath = provpath / os.listdir(provpath)[0]
        dstpath = DST_JSON_PATH / "finetuning_yprov/"#os.listdir(provpath)[0]
        shutil.move(srcpath, dstpath)

        # flowceptpath = Path("flowcept_buffer.jsonl")
        # dstpath = DST_JSON_PATH / "finetuning_flowcept.jsonl"
        # shutil.move(flowceptpath, dstpath)

        os.system(f"rm -rf prov")
        os.system(f"rm dlesym.pt")
        os.system(f"rm dlesym_pretrained.pt")

    fake_finetune()

def run_step3(): 

    DST_DATACARDS_PATH = Path("pipeline2_output/datacards")
    os.makedirs(DST_DATACARDS_PATH, exist_ok=True)
    DST_JSON_PATH = Path("pipeline2_output/jsons")
    os.makedirs(DST_JSON_PATH, exist_ok=True)
    DST_PROVCARDS_PATH = Path("pipeline2_output/provenancecards")
    os.makedirs(DST_PROVCARDS_PATH, exist_ok=True)

    def simulate_inference(model_dim=8192, input_seq_len=512, batch_size=32, model_depth=20):

        os.system(f"rm -rf prov")

        yprov4ml.start_run(
            prov_user_namespace="www.example.org",
            experiment_name=f"inferences", 
            provenance_save_dir="prov",
            disable_codecarbon=True, 
            metrics_file_type="csv",
        )

        yprov4ml.log_source_code()
        yprov4ml.log_execution_command(cmd="python", path="src/pipeline2/03_run_inferences.py")
        model = torch.nn.Linear(1,1)
        torch.save(model, "dlesym.pt")
        yprov4ml.log_model("dlesym_finetuned", model, context="inference", is_input=True)
        yprov4ml.log_dataset("era5_redi", None, log_dataset_info=False)

        # flowcept = Flowcept(workflow_name="finetuning", save_workflow=False, workflow_id="finetuning")
        # flowcept.start()
        t = FlowceptTask()

        if torch.backends.mps.is_available():
            device_type = "mps"
            sync_func = torch.mps.synchronize
            print("--- Using Apple Silicon (MPS) ---")
        elif torch.cuda.is_available():
            device_type = "cuda"
            sync_func = torch.cuda.synchronize
            print("--- Using NVIDIA GPU (CUDA) ---")
        else:
            device_type = "cpu"
            sync_func = lambda: None
            print("--- Using CPU (Simulation will be slow) ---")
        device = torch.device(device_type)

        fake_model_weights = torch.randn((model_dim, model_dim), dtype=torch.float16, device=device)
        input_tensor = torch.randn((1, input_seq_len, model_dim), dtype=torch.float16, device=device)
        torch.save(input_tensor, "input_tensor_0.pt")
        yprov4ml.log_artifact("input_tensor", "input_tensor_0.pt", is_input=True, log_copy_in_prov_directory=False)

        _ = torch.matmul(input_tensor, fake_model_weights)
        sync_func() # Critical to wait for the GPU to actually finish

        # Simulate the transformer blocks (Multiple matrix multiplications)
        for _ in range(model_depth): # Simulate 32 layers
            input_tensor = torch.matmul(input_tensor, fake_model_weights)
            input_tensor = torch.nn.functional.relu(input_tensor)
        
        sync_func() # Critical to wait for the GPU to actually finish
        
        yprov4ml.log_model("dlesym", torch.nn.Linear(1,1))
        yprov4ml.log_system_metrics(context="inference", step=0)
        with open("output.nc", "w") as f: 
            f.write("ciao mamma" * 150)
        yprov4ml.log_artifact("output", "output.nc", log_copy_in_prov_directory=False)

        # Cleanup
        del fake_model_weights
        del input_tensor
        torch.cuda.empty_cache()
        print("\n--- Inference Complete ---")

        yprov4ml.end_run()
        t.end()
        # flowcept.stop()


        provpath = Path("prov")
        srcpath = provpath / os.listdir(provpath)[0]
        dstpath = DST_JSON_PATH / "inference_yprov/"#os.listdir(provpath)[0]
        if dstpath.exists(): 
            os.system(f"rm -rf {dstpath}")
        shutil.move(srcpath, dstpath)

        # flowceptpath = Path("flowcept_buffer.jsonl")
        # dstpath = DST_JSON_PATH / "inference_flowcept.jsonl"
        # shutil.move(flowceptpath, dstpath)

        os.system(f"rm -rf prov")
        os.system(f"rm output.nc")
        os.system(f"rm dlesym.pt")
        os.system(f"rm input_tensor_0.pt")
        os.system(f"rm dlesym_finetuned.pt")
        
    simulate_inference()

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
# from flowcept import Flowcept, FlowceptTask

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

    VAR = "t2m0"

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
    # flowcept.stop()

    provpath = Path("prov")
    srcpath = provpath / os.listdir(provpath)[0]
    dstpath = DST_JSON_PATH / "analysis_yprov/"#os.listdir(provpath)[0]
    if dstpath.exists(): 
        os.system(f"rm -rf {dstpath}")
    shutil.move(srcpath, dstpath)

    # flowceptpath = Path("flowcept_buffer.jsonl")
    # dstpath = DST_JSON_PATH / "analysis_flowcept.jsonl"
    # shutil.move(flowceptpath, dstpath)

    os.system(f"rm -rf prov")
    os.system(f"rm results.csv")
    os.system(f"rm input_tensor.pt")
    os.system(f"rm error_modes_2x6.pdf")




def main(): 

    flowcept = Flowcept(workflow_name="finetuning", workflow_id="finetuning", check_safe_stops=False)
    flowcept.start()
    run_step1()
    run_step2()
    run_step3()
    run_step4()

    flowcept.stop()

if __name__ == "__main__": 
    main()

# KMP_DUPLICATE_LIB_OK=TRUE python src/pipeline2/run_flowcept.py