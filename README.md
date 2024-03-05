# PyDataSteps
## Overview
This repository introduces the Simple Workflow Executor, a tool designed to simplify the creation, management, and execution of data-fetching workflows. This tool is especially suited for scenarios that do not require the complexities of serverless compute platforms or containerized applications, such as AWS Step Functions and Microsoft Logic Apps.

The need for this tool arises from common issues faced in data integration and automation tasks:

* **Overhead of Serverless Solutions:** While powerful, serverless platforms can introduce unnecessary complexity for straightforward tasks like fetching data from APIs.
* **Readability:** Traditional scripting solutions, such as Bash scripts, can become difficult to maintain and understand, especially as workflows grow in complexity.
* **Code Maintenance:** Writing and maintaining Python code for every API connector increases development time and can lead to a sprawling codebase, making updates and bug fixes challenging.
* **PyDataSteps** aims to address these issues by providing a structured yet flexible approach to defining and running workflows.

## Features
* **JSON or YAML-Based Workflow Definitions:** Define your workflows in an easy-to-read YAML format, separating the workflow logic from the execution code. 
* **Parallel Execution:** Speed up your workflows with built-in support for parallel execution, ideal for handling paginated API responses.
* **Configurable Settings:** Pass in dynamic settings such as API endpoints and authentication tokens, keeping your workflows adaptable and secure.
* **Integration-Friendly:** Designed to be used as a standalone batch process or integrated into larger Python applications, providing versatility in how workflows are executed.

## Usage
1. **Defining a Workflow:** Create a YAML file defining the steps of your workflow. Specify actions such as API calls, data parsing, and conditional logic.
```yaml
steps:
  - name: Fetch Data
    type: api_call
    properties:
      method: GET
      path: /data
    output: raw_data
```
2. **Executing a Workflow:** Use the provided Python script to execute your workflow, passing in any necessary settings.

```bash
python execute_workflow.py --workflow my_workflow.yaml --settings settings.json
```
3. **Integrating with Applications:** Import the workflow executor as a module in your Python projects to enhance automation and data processing capabilities.
```python
from workflow_executor import execute_workflow
final_state = execute_workflow(workflow_content, settings)
```

## Getting Started
To get started with PyDataSteps clone this repository and follow the instructions in the Installation and Quick Start sections.

## Installation
TBC

## Quick Start
TBC

## Contributing
Contributions are welcome.

## License
MIT