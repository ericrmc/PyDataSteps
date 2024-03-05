import yaml
import requests
import json
import jsonpath_ng
import time

def execute_step(step, state, settings, base_url, global_headers):
    properties = step.get('properties', {})
    step_type = step.get('type', '')
    retry_after = 10  # Default retry sleep time

    if step_type == 'api_call':
        while True:
            # Handle API call, similar to previous implementation
            full_url = base_url + properties.get('path', '')
            method = properties.get('method', 'GET')
            if 'loop_over' in properties:
                items = state.get(properties['loop_over'], [])
                response_data = []
                for item in items:
                    response = requests.request(method=method, url=full_url.format(id=item), headers=global_headers)
                    if response.status_code == 429:
                        time.sleep(retry_after)
                        continue  # Retry the current item
                    response_data.append(response.json())
                state[step['output']] = response_data
                break  # Exit loop if successful
            else:
                response = requests.request(method=method, url=full_url, headers=global_headers)
                if response.status_code == 429:
                    time.sleep(retry_after)
                    continue  # Retry the entire step
                state[step['output']] = {'content': response.json(), 'status_code': response.status_code}
                break  # Exit loop if successful

    elif step_type == 'switch':
        # Check the status code and decide on the action
        status_code = state.get(properties['input'], 0)
        action_info = properties['actions'].get(str(status_code), properties['actions'].get('default', {}))

        if action_info.get('action') == 'run_step':
            # Prepare to run another step based on the current status code
            new_step_name = action_info['run_step'].get('name')
            new_step_parameters = action_info['run_step'].get('parameters', [])
            
            # Find the step in the workflow by name
            new_step = next((s for s in settings['steps'] if s['name'] == new_step_name), None)
            if new_step:
                # Replace placeholders in the new step with actual parameters
                new_step = json.loads(json.dumps(new_step).replace('parameter', new_step_parameters[0]))
                # Execute the new step
                execute_step(new_step, state, settings, base_url, global_headers)

    elif step_type == 'update_state':
        # Handle state update, similar to previous but now can handle 'append'
        if properties['update_type'] == 'append':
            state.setdefault(properties['output'], []).append(state.get(properties['input']))

    elif step['type'] == 'parse_json':
        data = state.get(properties['input'], {})
        json_expr = jsonpath_ng.parse(properties['jsonpath'])
        match = json_expr.find(data)
        state[step['output']] = [m.value for m in match]

    elif step['type'] == 'save_file':
        filename = properties.get('filename', '')
        input_data = properties.get('input', '')
        with open(filename, 'w') as f:
            json.dump(state.get(input_data, {}), f)

def execute_workflow(workflow_file):
    with open(workflow_file, 'r') as file:
        workflow = yaml.safe_load(file)

    settings = workflow.get('settings', {})
    base_url = settings.get('base_url', '')
    global_headers = settings.get('headers', {})
    state = settings.get('state', {})

    for step in workflow['steps']:
        execute_step(step, state, settings, base_url, global_headers)

    return state

# Usage
final_state = execute_workflow('templates/starter.yaml')
