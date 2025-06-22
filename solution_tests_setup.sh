#!/bin/bash

# Solution Tests Setup Script
# Überprüft ob Tests für Musterlösungen vorhanden sind

set -e

echo "✅ Solution Tests Validation"
echo "============================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to validate solution tests
validate_solution_tests() {
    local exercise_dir="$1"
    local language="$2"
    local errors=0
    
    if [[ ! -d "$exercise_dir/solution" ]]; then
        return 0  # No solution directory, skip
    fi
    
    case "$language" in
        "php")
            if [[ ! -f "$exercise_dir/solution/"*"Refactored.php" ]]; then
                print_error "PHP: Missing refactored solution in $exercise_dir/solution/"
                ((errors++))
            fi
            if [[ ! -f "$exercise_dir/solution/"*"RefactoredTest.php" ]]; then
                print_error "PHP: Missing solution test in $exercise_dir/solution/"
                ((errors++))
            else
                print_success "PHP: $exercise_dir/solution/"
            fi
            ;;
            
        "typescript")
            if [[ ! -f "$exercise_dir/solution/"*"Refactored.ts" ]]; then
                print_error "TypeScript: Missing refactored solution in $exercise_dir/solution/"
                ((errors++))
            fi
            if [[ ! -f "$exercise_dir/solution/"*"Refactored.test.ts" ]]; then
                print_error "TypeScript: Missing solution test in $exercise_dir/solution/"
                ((errors++))
            else
                print_success "TypeScript: $exercise_dir/solution/"
            fi
            ;;
            
        "python")
            if [[ ! -f "$exercise_dir/solution/"*"_refactored.py" ]]; then
                print_error "Python: Missing refactored solution in $exercise_dir/solution/"
                ((errors++))
            fi
            if [[ ! -f "$exercise_dir/solution/test_"*"_refactored.py" ]]; then
                print_error "Python: Missing solution test in $exercise_dir/solution/"
                ((errors++))
            else
                print_success "Python: $exercise_dir/solution/"
            fi
            ;;
    esac
    
    return $errors
}

total_errors=0

# Process PHP exercises
if [[ -d "php/exercises" ]]; then
    print_info "Validating PHP solution tests..."
    find php/exercises -type d -name "solution" | while read solution_dir; do
        exercise_dir=$(dirname "$solution_dir")
        validate_solution_tests "$exercise_dir" "php"
        total_errors=$((total_errors + $?))
    done
fi

# Process TypeScript exercises
if [[ -d "typescript/exercises" ]]; then
    print_info "Validating TypeScript solution tests..."
    find typescript/exercises -type d -name "solution" | while read solution_dir; do
        exercise_dir=$(dirname "$solution_dir")
        validate_solution_tests "$exercise_dir" "typescript"
        total_errors=$((total_errors + $?))
    done
fi

# Process Python exercises
if [[ -d "python/exercises" ]]; then
    print_info "Validating Python solution tests..."
    find python/exercises -type d -name "solution" | while read solution_dir; do
        exercise_dir=$(dirname "$solution_dir")
        validate_solution_tests "$exercise_dir" "python"
        total_errors=$((total_errors + $?))
    done
fi

echo ""
if [[ $total_errors -eq 0 ]]; then
    print_success "All solution tests are properly set up!"
else
    print_error "Found $total_errors missing solution tests!"
    exit 1
fi

echo ""
echo "📋 Nächste Schritte:"
echo "  1. Tests für Original-Code ausführen"
echo "  2. Tests für Musterlösungen ausführen:"
echo "     - PHP: cd php && vendor/bin/phpunit exercises/"
echo "     - TypeScript: cd typescript && npm test"
echo "     - Python: cd python && source venv/bin/activate && pytest exercises/ -v"
echo ""
echo "💡 Hinweis: Jede Musterlösung hat separate Test-Dateien mit identischer Logik"
echo "    aber korrekten Imports für die refactorierten Klassen."