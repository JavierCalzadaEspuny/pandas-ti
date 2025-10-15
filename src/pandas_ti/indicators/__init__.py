import os
import glob
import importlib

# Get the directory of the current file
current_dir = os.path.dirname(__file__)

# Find all Python files in the current directory
indicator_files = glob.glob(os.path.join(current_dir, "*.py"))

# Initialize the __all__ list to store the names of exported functions
__all__ = []

# Loop through all Python files found
for f in indicator_files:
    # Extract the base name of the file (without extension)
    name = os.path.splitext(os.path.basename(f))[0]
    
    # Skip files that start with an underscore (e.g., private modules)
    if name.startswith("_"):
        continue
    
    # Dynamically import the module
    module = importlib.import_module(f".{name}", package=__package__)
    
    # Get the function with the same name as the module, if it exists
    func = getattr(module, name, None)
    
    # If the function is callable, add it to the global namespace and __all__
    if callable(func):
        globals()[name] = func
        __all__.append(name)
