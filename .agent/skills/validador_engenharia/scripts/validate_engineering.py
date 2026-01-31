import json
import argparse
import sys

def validate(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    errors = []
    
    # Check Spaces
    for space in data.get('spaces', []):
        area = space.get('area', 0)
        
        if area <= 0:
            errors.append(f"Space {space.get('_name')} has invalid area: {area}")
            
        for svc in space.get('services', []):
            qtd = svc.get('quantity', 0)
            if qtd < 0:
                errors.append(f"Service {svc.get('_name')} in {space.get('_name')} has negative quantity: {qtd}")
                
            # Basic Density Check: Floor tiles should not exceed area * 1.5 (generous waste factor)
            # This requires checking service name or ID basics
            name_lower = svc.get('_name', '').lower()
            if 'piso' in name_lower or 'porcelanato' in name_lower:
                if qtd > area * 1.5:
                     errors.append(f"Suspicious quantity for {svc.get('_name')}: {qtd} for room area {area}")

    if errors:
        print("REPROVADO (Engenharia):")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    else:
        print("APROVADO (Engenharia): Projeto fisicamente coerente.")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    args = parser.parse_args()
    
    validate(args.input_file)
