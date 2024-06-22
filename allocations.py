import json
from pathlib import Path

def json_loader(json_file_name):
    with open(json_file_name) as f:
        data = json.load(f)
    return data

def helper_calculate_allocations(allocation_amount, allocations, investors, denom):
    for investor in investors:
        amount_to_allocate = round((investor["average_amount"] / denom) * allocation_amount, 5)
        allocations[investor["name"]]["amount"] = min(amount_to_allocate, investor["requested_amount"])
    return allocations

def format_results(allocations):
    '''
    Format the final result to match that of given test data output.json
    '''
    final = {}
    for k, v in allocations.items():
        final[k] = v['amount']
    return final

def calculate_allocations(data, has_complex_data=False):
    allocation_amount = data["allocation_amount"]
    investors = data["investor_amounts"]
    denominator = 0
    allocations = {}
    # Pre-populate allocations with all 0 amounts and get the total requested amount of all investors
    for investor in investors: 
        denominator += investor["average_amount"]
        allocations[investor["name"]] =  {"amount": 0, "requested_amount": investor["requested_amount"]}
    if denominator == 0:
        return format_results(allocations)
    allocations = helper_calculate_allocations(allocation_amount, allocations, investors, denominator)
        
    for k, v in allocations.items():
        if has_complex_data:
            diff = allocation_amount - sum([v["amount"] for k, v in allocations.items()])
            denominator -= diff
            allocations = helper_calculate_allocations(allocation_amount, allocations, investors, denominator)
            
    return format_results(allocations)
   

## Unit tests
p = Path(__file__).parents[1]

print("Running unit test case: simple_1_input.json")
data = json_loader(str(p) + "/data/simple_1_input.json")
expected_data = json_loader(str(p) + "/data/simple_1_output.json")
assert calculate_allocations(data) == expected_data

print("Running unit test case: simple_2_input.json")
data = json_loader(str(p) + "/data/simple_2_input.json")
expected_data = json_loader(str(p) + "/data/simple_2_output.json")
assert calculate_allocations(data) == expected_data

print("Running unit test case: complex_1_input.json with feature flag has_complex_data on")
data = json_loader(str(p) + "/data/complex_1_input.json")
expected_data = json_loader(str(p) + "/data/complex_1_output.json")
assert calculate_allocations(data, True) == expected_data

print("Running unit test case: complex_2_input.json  with feature flag has_complex_data on")
data = json_loader(str(p) + "/data/complex_2_input.json")
expected_data = json_loader(str(p) + "/data/complex_2_output.json")
assert calculate_allocations(data, True) == expected_data