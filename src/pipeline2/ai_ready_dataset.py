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
    flowceptpath = Path("flowcept_buffer.jsonl")
    dstpath = DST_JSON_PATH / "redi_flowcept.jsonl"
    shutil.move(flowceptpath, dstpath)

    # Get datacard from redi
    redicardpath = Path("DATA_CARD.md")
    dstpath = DST_DATACARDS_PATH / "redi_datacard.md"
    shutil.move("tmp/" / redicardpath, dstpath)

    # Cleanup stuff from exec
    os.system(f"rm -rf {provpath}")

    if flowceptpath.exists(): 
        os.remove(flowceptpath)
    if ("tmp/" / redicardpath).exists(): 
        os.remove("tmp/" / redicardpath)
    # os.remove("DomainInference.jsonl")
    # os.remove("InputFilesValidation.jsonl")
    # os.remove("OutputGeneration.jsonl")
    # os.remove("PipelineCreation.jsonl")
    # os.remove("PipelineExecution.jsonl")
    # os.remove("PipelineFinalize.jsonl")
    # os.remove("flowcept_buffer.jsonl")
    os.system(f"rm -rf tmp")