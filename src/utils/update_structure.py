import os
from pathlib import Path

def generate_structure_file(max_depth=3):
    """
    Genera estructura.txt con una estructura legible del proyecto,
    ignorando carpetas y archivos irrelevantes.
    """
    base_dir = Path(".")
    
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', '.venv'}
    ignore_files = {'.DS_Store', 'estructura.txt', 'estructura_actual.txt'}
    
    allowed_root_dirs = {"src", "app"}  # muestra sólo estas carpetas principales
    
    structure_lines = ["Administrador_estadisticas/"]
    
    for item in sorted(base_dir.rglob("*")):
        
        # ignorar no deseados
        if any(part in ignore_dirs for part in item.parts):
            continue
        
        if item.name in ignore_files:
            continue
        
        # limitar profundidad
        depth = len(item.relative_to(base_dir).parts)
        if depth > max_depth:
            continue
        
        # whitelist: solo mostrar src y app + sus contenidos
        if item.is_dir() and depth == 1 and item.name not in allowed_root_dirs:
            continue
        
        # armar indentación
        indent = "│   " * (depth - 1) + "├── " if depth > 0 else ""
        
        if item.is_dir() and item != base_dir:
            structure_lines.append(f"{indent}{item.name}/")
        elif item.is_file():
            structure_lines.append(f"{indent}{item.name}")
    
    with open('estructura.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(structure_lines))
    
    print("✅ estructura.txt generado correctamente")


if __name__ == "__main__":
    generate_structure_file()
