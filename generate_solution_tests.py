#!/usr/bin/env python3
"""
Automatisches Script zur Generierung von Solution-Tests.
Kopiert Original-Tests und transformiert sie für die Solution-Klassen.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def find_test_files() -> List[Tuple[Path, str]]:
    """Findet alle Test-Dateien in den Exercises."""
    test_files = []
    
    # PHP Tests
    for php_test in Path("php/exercises").rglob("*Test.php"):
        if "solution" not in str(php_test):
            test_files.append((php_test, "php"))
    
    # TypeScript Tests  
    for ts_test in Path("typescript/exercises").rglob("*.test.ts"):
        if "solution" not in str(ts_test):
            test_files.append((ts_test, "typescript"))
    
    # Python Tests
    for py_test in Path("python/exercises").rglob("test_*.py"):
        if "solution" not in str(py_test):
            test_files.append((py_test, "python"))
    
    return test_files


def transform_php_test(content: str, original_class: str) -> Tuple[str, str]:
    """Transformiert PHP Test für Solution."""
    refactored_class = f"{original_class}Refactored"
    solution_test_class = f"{original_class}RefactoredTest"
    
    # Remove namespace (solutions use require_once instead)
    content = re.sub(r'namespace [^;]+;', '', content)
    
    # Add require_once after use statement
    old_use = 'use PHPUnit\\Framework\\TestCase;'
    new_use = f"use PHPUnit\\Framework\\TestCase;\n\nrequire_once __DIR__ . '/{refactored_class}.php';"
    content = content.replace(old_use, new_use)
    
    # Change class name - use literal string matching
    old_class_def = f'class {original_class}Test extends TestCase'
    new_class_def = f'final class {solution_test_class} extends TestCase'
    content = content.replace(old_class_def, new_class_def)
    
    # Change property type
    old_property = f'private {original_class} $processor;'
    new_property = f'private {refactored_class} $processor;'
    content = content.replace(old_property, new_property)
    
    # Change instantiation
    old_instantiation = f'new {original_class}()'
    new_instantiation = f'new {refactored_class}()'
    content = content.replace(old_instantiation, new_instantiation)
    
    return content, f"{solution_test_class}.php"


def transform_typescript_test(content: str, original_class: str) -> Tuple[str, str]:
    """Transformiert TypeScript Test für Solution."""
    refactored_class = f"{original_class}Refactored"
    
    # Change import
    content = re.sub(
        rf"import {{ {original_class} }} from '../src/{original_class}';",
        f"import {{ {original_class} }} from './{refactored_class}';",
        content
    )
    
    # Change describe block
    content = re.sub(
        rf"describe\('{original_class}',",
        f"describe('{original_class} (Refactored Solution)',",
        content
    )
    
    return content, f"{refactored_class}.test.ts"


def transform_python_test(content: str, original_module: str, original_class: str) -> Tuple[str, str]:
    """Transformiert Python Test für Solution."""
    refactored_module = f"{original_module}_refactored"
    
    # Remove sys.path manipulation
    content = re.sub(r'import sys\nfrom pathlib import Path[^"]+', '', content)
    content = re.sub(r'# Add the src directory to Python path[^"]+', '', content)
    content = re.sub(r'sys\.path\.insert\([^)]+\)', '', content)
    
    # Change import
    content = re.sub(
        rf'from {original_module} import {original_class}',
        f'from .{refactored_module} import {original_class}',
        content
    )
    
    # Update class documentation
    content = re.sub(
        r'"""Tests for [^"]+"""',
        '"""Tests for the refactored OrderProcessor solution."""',
        content
    )
    
    # Change test class name
    content = re.sub(
        rf'class Test{original_class}:',
        f'class Test{original_class}Refactored:',
        content
    )
    
    # Update docstrings
    content = re.sub(
        r'"""Test cases for [^"]+"""',
        f'"""Test the refactored {original_class} solution."""',
        content
    )
    
    return content, f"test_{refactored_module}.py"


def extract_class_names(test_file: Path, language: str) -> Dict[str, str]:
    """Extrahiert Klassen- und Modul-Namen aus Test-Datei."""
    content = test_file.read_text(encoding='utf-8')
    
    if language == "php":
        # Extract class name from "class OrderProcessorTest"
        match = re.search(r'class (\w+)Test extends TestCase', content)
        if match:
            return {"class": match.group(1)}
    
    elif language == "typescript":
        # Extract from import
        match = re.search(r"import { (\w+) } from", content)
        if match:
            return {"class": match.group(1)}
    
    elif language == "python":
        # Extract from import "from order_processor import OrderProcessor"
        # Look for imports that don't contain common library names
        import_matches = re.findall(r'from (\w+) import (\w+)', content)
        for module, class_name in import_matches:
            # Skip common libraries
            if module not in ['pathlib', 'pytest', 'sys', 'os', 'typing', 'unittest']:
                return {"module": module, "class": class_name}
        
        # Fallback: Use test file name pattern
        test_name = test_file.stem
        if test_name.startswith("test_"):
            module_name = test_name[5:]  # Remove "test_" prefix
            return {"module": module_name, "class": "OrderProcessor"}
    
    return {}


def generate_solution_test(test_file: Path, language: str) -> bool:
    """Generiert Solution-Test für eine Test-Datei."""
    try:
        # Solution directory bestimmen
        if language == "php":
            # PHP tests are directly in the exercise directory
            exercise_dir = test_file.parent
        else:
            # TypeScript/Python tests are in tests/ subdirectory
            exercise_dir = test_file.parent.parent
        solution_dir = exercise_dir / "solution"
        
        if not solution_dir.exists():
            print(f"⚠️  Skipping {test_file} - no solution directory")
            return True
        
        # Check if solution code exists
        if language == "php" and not any(solution_dir.glob("*Refactored.php")):
            print(f"⚠️  Skipping {test_file} - no PHP solution code found")
            return True
        elif language == "typescript" and not any(solution_dir.glob("*Refactored.ts")):
            print(f"⚠️  Skipping {test_file} - no TypeScript solution code found") 
            return True
        elif language == "python" and not any(solution_dir.glob("*_refactored.py")):
            print(f"⚠️  Skipping {test_file} - no Python solution code found")
            return True
        
        # Original Test lesen
        content = test_file.read_text(encoding='utf-8')
        names = extract_class_names(test_file, language)
        
        if not names:
            print(f"❌ Could not extract class names from {test_file}")
            return False
        
        # Transformation durchführen
        if language == "php":
            transformed_content, solution_filename = transform_php_test(content, names["class"])
        elif language == "typescript":
            transformed_content, solution_filename = transform_typescript_test(content, names["class"])
        elif language == "python":
            transformed_content, solution_filename = transform_python_test(content, names["module"], names["class"])
        else:
            return False
        
        # Solution test schreiben
        solution_test_path = solution_dir / solution_filename
        solution_test_path.write_text(transformed_content, encoding='utf-8')
        
        print(f"✅ Generated: {solution_test_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {test_file}: {e}")
        return False


def main():
    """Hauptfunktion."""
    print("🔄 Generating Solution Tests")
    print("============================")
    
    # Working directory prüfen
    if not Path("php").exists() or not Path("typescript").exists() or not Path("python").exists():
        print("❌ Script must be run from refactoring-exercises directory")
        return 1
    
    test_files = find_test_files()
    if not test_files:
        print("❌ No test files found")
        return 1
    
    success_count = 0
    total_count = len(test_files)
    
    for test_file, language in test_files:
        print(f"\n📝 Processing {language}: {test_file}")
        if generate_solution_test(test_file, language):
            success_count += 1
    
    print(f"\n🎉 Summary:")
    print(f"   ✅ Success: {success_count}/{total_count}")
    print(f"   ❌ Failed:  {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print(f"\n💡 Next steps:")
        print(f"   1. Run tests: ./solution_tests_setup.sh")
        print(f"   2. Verify all solutions pass their tests")
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())