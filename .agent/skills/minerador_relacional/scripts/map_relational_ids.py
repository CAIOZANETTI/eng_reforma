import json
import os
import argparse
from glob import glob

def map_ids(input_dir, output_file):
    whitelist = {
        "service_ids": set(),
        "material_ids": set(),
        "material_category_ids": set(),
        "labor_ids": set(),
        "labor_category_ids": set()
    }
    
    files = glob(os.path.join(input_dir, "*.json"))
    print(f"Scanning {len(files)} files...")
    
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                spaces = data.get("spaces", [])
                for space in spaces:
                    services = space.get("services", [])
                    for svc in services:
                        whitelist["service_ids"].add(svc.get("service_id"))
                        
                        # Material Cats
                        for mc in svc.get("material_categories", []):
                            whitelist["material_category_ids"].add(mc.get("material_category_id"))
                            for m in mc.get("materials", []):
                                whitelist["material_ids"].add(m.get("material_id"))
                                
                        # Labor Cats
                        for lc in svc.get("labor_categories", []):
                            whitelist["labor_category_ids"].add(lc.get("labor_category_id"))
                            for l in lc.get("labors", []):
                                whitelist["labor_ids"].add(l.get("labor_id"))
                                
            except Exception as e:
                print(f"Error reading {fpath}: {e}")

    # Convert sets to sorted lists for JSON serialization
    final_output = {k: sorted(list(v)) for k, v in whitelist.items()}
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)
        
    print(f"Whitelist generated at {output_file}")
    print(f"Stats: {len(final_output['service_ids'])} Services, {len(final_output['material_ids'])} Materials.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()
    
    map_ids(args.input_dir, args.output_file)
