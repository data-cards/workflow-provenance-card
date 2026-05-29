
import os

def main(): 
    os.system("python src/pipeline2/convert_json2card.py pipeline2_output/jsons/redi_yprov")
    os.system("python src/pipeline2/convert_json2card.py pipeline2_output/jsons/finetuning_yprov")
    os.system("python src/pipeline2/convert_json2card.py pipeline2_output/jsons/inference_yprov")
    os.system("python src/pipeline2/convert_json2card.py pipeline2_output/jsons/analysis_yprov")

if __name__ == "__main__": 
    main()