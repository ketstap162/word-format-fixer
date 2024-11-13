# Word Format Fixer

## Description
This application is aimed at processing Word files. 
It is unique in its versatility, as it works through the JSON format specification.  
This project is a PoC and therefore does not fully meet its functional requirements. 
It is a confirmation of the possibility of implementing an application based on concept.  
The program uses the `getattr()` and `setattr()` functions to compare and set the necessary parameters in the `.docx` file.

### Concept
Processing `.docx` files by correcting formatting according to certain requirements described in JSON file.

### Working principle
1) Upload the `.docx` file.
2) Find errors according to the JSON specification.
3) Get a JSON file with errors.
4) Use the received JSON file, remove unnecessary corrections from it and send it for error handling.
5) Get a corrected `.docx` file.

## Used technologies:
- Python 3.10
- FastAPI
- python-docx


## Advantages:
- **JSON:** Works via JSON specifications that can be imported from anywhere.
- **Style Flexibility:** Can work with different Word formats.
- **Parameter Flexibility:** Ignores unspecified parameters when checking.
- **Client-Service:** Adding specifications does not require technical support.
- **Logic Segmentation:** Allows segmentation of processing, allowing you to add new libraries for tasks that `python-docx` cannot handle.
- **API Doc:** Has Swagger documentation with endpoints describing.

## Disadvantages
- Has strict requirements for the JSON specification.
- Applies the same type of formatting to all identical elements.
- Correction correlation requires a smart client.
- Inability to work with writing style, grammar checking, etc.

### Commands and endpoints for developers
Command to run project:
```commandline
uvicorn main:app --reload
```

Documentation endpoint:
```commandline
http://127.0.0.1:8000/docs
```

### Time spent:
- **11.11.2024** - 8 hours (Project structure and base features)
- **12.11.2024** - 6 hours (The first prototype of the working application is ready)
- **13.11.2024** - 1 hour (Optimization, code cleaning and reports)
