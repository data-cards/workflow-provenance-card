import torch
import shutil
import os
from pathlib import Path
import sys
sys.path.append("/Users/gabrielepadovani/Desktop/Università/yProv4ML")
import yprov4ml
from flowcept import Flowcept, FlowceptTask

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

        flowcept = Flowcept(workflow_name="finetuning", save_workflow=False, workflow_id="finetuning")
        t = FlowceptTask()
        flowcept.start()

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
        flowcept.stop()


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