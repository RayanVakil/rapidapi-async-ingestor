import os
import re

def build_script():
    """
    Compiles the modular src/ architecture into a single execution script
    to satisfy the assessment submission requirements.
    """
    # Exact dependency order to ensure classes/functions are defined before use
    files_to_compile = [
        "src/models/schemas.py",
        "src/client.py",          
        "src/processing.py",
        "src/visual.py",
        "src/main.py"
    ]
    
    output_filename = "script_Rayan_Vakil.txt"
    compiled_code = []
    
    for filepath in files_to_compile:
        if not os.path.exists(filepath):
            print(f"Error: Could not find {filepath}. Build failed.")
            return
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Regex to strip out internal module imports (e.g., from src.models.schemas import...)
            # The MULTILINE flag ensures ^ matches the start of every line
            content = re.sub(r"^from src.*import.*$\n?", "", content, flags=re.MULTILINE)
            content = re.sub(r"^import src.*$\n?", "", content, flags=re.MULTILINE)
            
            # Append a header comment for readability in the compiled file
            compiled_code.append(f"# {'='*50}\n# Extracted from: {filepath}\n# {'='*50}\n")
            compiled_code.append(content)
            compiled_code.append("\n\n")
            
    final_script = "".join(compiled_code)
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(final_script)
        
    print(f"Successfully compiled {len(files_to_compile)} modules into {output_filename}")

if __name__ == "__main__":
    build_script()
