import json
import argparse
import uuid
import os
import math
from datetime import datetime

def generate_variation(template_path, scale_factor, output_dir):
    with open(template_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Generate new container IDs
    new_project_id = str(uuid.uuid4())
    
    # Update Metadata
    data['exportedAt'] = datetime.now().isoformat() + "Z"
    data['template']['description'] += f" (Variação Escala x{scale_factor})"
    
    # Scale Project
    if 'project' in data:
        data['project']['total_area'] = round(data['project'].get('total_area', 0) * scale_factor, 2)
        
    # Scale Spaces
    for space in data.get('spaces', []):
        space['_name'] += " (V)"
        original_area = space.get('area', 0)
        new_area = round(original_area * scale_factor, 2)
        space['area'] = new_area
        space['space_id'] = str(uuid.uuid4()) # New space ID is safe
        
        # Scale Services
        for svc in space.get('services', []):
            # Check for non-scalable units in materials/labor
            is_scalable = True
            for cat in svc.get('material_categories', []) + svc.get('labor_categories', []):
                unit = cat.get('base_unit', '').lower()
                if unit in ['un', 'cj', 'kit', 'pç', 'pc']:
                    is_scalable = False
                    break
            
            original_qtd = svc.get('quantity', 0)
            
            if is_scalable:
                svc['quantity'] = round(original_qtd * scale_factor, 2)
            else:
                # Keep original quantity for countable items
                svc['quantity'] = original_qtd
            
            # Note: We DO NOT touch service_id, material_id, etc.
            
    # Output
    os.makedirs(output_dir, exist_ok=True)
    filename = f"reforma_var_{new_project_id}.json"
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Generated variation: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True)
    parser.add_argument("--scale", type=float, required=True)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()
    
    generate_variation(args.template, args.scale, args.output_dir)
