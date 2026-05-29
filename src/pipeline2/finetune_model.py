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

        flowcept = Flowcept(workflow_name="finetuning", save_workflow=False, workflow_id="finetuning")
        flowcept.start()

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
        flowcept.stop()


        provpath = Path("prov")
        srcpath = provpath / os.listdir(provpath)[0]
        dstpath = DST_JSON_PATH / "finetuning_yprov/"#os.listdir(provpath)[0]
        shutil.move(srcpath, dstpath)

        flowceptpath = Path("flowcept_buffer.jsonl")
        dstpath = DST_JSON_PATH / "finetuning_flowcept.jsonl"
        shutil.move(flowceptpath, dstpath)

        os.system(f"rm -rf prov")
        os.system(f"rm dlesym.pt")
        os.system(f"rm dlesym_pretrained.pt")

    fake_finetune()