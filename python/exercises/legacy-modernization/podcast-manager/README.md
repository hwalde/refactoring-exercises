# Podcast Manager Refactoring Exercise

## Overview
This exercise demonstrates the refactoring of a legacy podcast management CLI application from a monolithic, poorly structured codebase to a clean, maintainable architecture following SOLID principles.

## Exercise Structure

### Legacy Code
- `src/podcast_manager.py` - The original "God Class" implementation with multiple code smells

### Tests
- `tests/test_podcast_manager.py` - Black-box tests defining expected behavior
- `test_feed.xml` - Sample RSS feed for testing

### Solution
- `solution/` - Refactored implementation demonstrating clean architecture
  - `domain_models.py` - Domain objects (Podcast, Episode)
  - `repository.py` - Data access layer
  - `services.py` - Business logic services
  - `podcast_manager_refactored.py` - Application orchestrator
  - `cli.py` - Command line interface
  - `exceptions.py` - Custom exception types

### Guidance
- `task.md` - Detailed exercise instructions
- `hints/` - Progressive hints for the refactoring process

## Code Smells Demonstrated

The legacy code intentionally contains these code smells:

1. **God Class** - `PodcastThing` handles everything
2. **Long Methods** - `do_stuff()` and `handle_things()` are overly complex
3. **Duplicate Code** - JSON serialization repeated multiple times
4. **Feature Envy** - Direct external API access throughout
5. **Primitive Obsession** - Overuse of dicts and strings
6. **Data Clumps** - Related data not properly grouped

## Architecture Improvements

The solution demonstrates:

1. **Single Responsibility Principle** - Each class has one clear purpose
2. **Dependency Injection** - Services receive dependencies via constructor
3. **Repository Pattern** - Data access abstraction
4. **Domain-Driven Design** - Rich domain models with behavior
5. **Clean Error Handling** - Specific exceptions and proper error management
6. **Type Safety** - Complete type hints throughout

## Running the Exercise

### Original Legacy Code
```bash
python src/podcast_manager.py add "file://test_feed.xml"
python src/podcast_manager.py list
```

### Tests
```bash
# From the python directory
source venv/bin/activate
pytest exercises/legacy-modernization/podcast-manager/tests/ -v
```

### Code Quality Checks
```bash
# Type checking
mypy exercises/legacy-modernization/podcast-manager/src/

# Code formatting
black exercises/legacy-modernization/podcast-manager/
ruff check exercises/legacy-modernization/podcast-manager/
```

## Learning Objectives

After completing this exercise, you will understand:

1. How to identify and address common code smells
2. Techniques for incremental refactoring
3. Clean architecture principles and layered design
4. Dependency injection and inversion of control
5. Domain-driven design concepts
6. Test-driven refactoring approaches

## Key Refactoring Techniques

- **Extract Method** - Breaking down long methods
- **Extract Class** - Separating concerns into focused classes
- **Move Method** - Relocating methods to appropriate classes
- **Introduce Parameter Object** - Grouping related parameters
- **Replace Type Code with Polymorphism** - Using strategy pattern for export formats
- **Encapsulate Field** - Protecting data with proper accessors