import json
import argparse
import sys

def validate(input_file, whitelist_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open(whitelist_file, 'r', encoding='utf-8') as f:
        whitelist = json.load(f)
        
    errors = []
    
    # Check Project Structure
    if 'template' not in data or 'project' not in data:
        errors.append("Missing 'template' or 'project' root keys")

    spaces = data.get('spaces', [])
    if not spaces:
        errors.append("No spaces found")
        
    for space in spaces:
        if 'space_id' not in space:
            errors.append("Detailed: Space missing space_id")
            
        for svc in space.get('services', []):
            svc_id = svc.get('service_id')
            if svc_id not in whitelist['service_ids']:
                errors.append(f"SQL VIOLATION: Service ID '{svc_id}' not in whitelist.")
                
            # Material Cats
            for mc in svc.get('material_categories', []):
                mc_id = mc.get('material_category_id')
                if mc_id not in whitelist['material_category_ids']:
                     errors.append(f"SQL VIOLATION: Mat Category ID '{mc_id}' not in whitelist.")
                     
                for m in mc.get('materials', []):
                    m_id = m.get('material_id')
                    if m_id not in whitelist['material_ids']:
                        errors.append(f"SQL VIOLATION: Material ID '{m_id}' not in whitelist.")

            # Labor Cats
            for lc in svc.get('labor_categories', []):
                lc_id = lc.get('labor_category_id')
                if lc_id not in whitelist['labor_category_ids']:
                     errors.append(f"SQL VIOLATION: Labor Category ID '{lc_id}' not in whitelist.")
                     
                for l in lc.get('labors', []):
                    l_id = l.get('labor_id')
                    if l_id not in whitelist['labor_ids']:
                        errors.append(f"SQL VIOLATION: Labor ID '{l_id}' not in whitelist.")

    if errors:
        print("REPROVADO (Programador - SQL Integrity):")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    else:
        print("APROVADO (Programador): Integridade Relacional Garantida.")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--whitelist", required=True)
    args = parser.parse_args()
    
    validate(args.input_file, args.whitelist)
