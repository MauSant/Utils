from dataclasses import fields, is_dataclass
from typing import Literal, get_args, get_origin

''' 
[THIS WAS NOT TESTED]
Because is it very specific this is not in use
This is only useful when:
1-  type_hint is a Union(python3.10^) of Dataclasses
2- The dataclasses has a identifier attribute that is a Literal Type
Example: type_hint = HttpAction | WorkflowAction
This function does not validate the contents of the dictionary
'''
def from_dict_to_dataclass(data: dict, type_hint: type, identifier_attr:str) -> object:
    # Get all possible types from the Union (or single type)
    possible_types = get_args(type_hint)

    # Create mapping of action_type values to their classes
    type_registry = {}
    for p_type in possible_types:
        if not is_dataclass(p_type):
            raise ValueError("Not dataclass type inside hint")
            
        # Get the Literal value from action_type annotation
        type_hint = p_type.__annotations__.get(identifier_attr)
        if type_hint and (get_origin(type_hint) is Literal):
            literal_value = get_args(type_hint)[0]
            type_registry[literal_value] = p_type

    # Find matching type using action_type from data
    if (action_type := data.get(identifier_attr)) is None:
        raise ValueError("Missing 'action_type' in data")
    
    if (p_type := type_registry.get(action_type)) is None:
        raise ValueError(f"No matching type for action_type: {action_type}")

    # Filter data to only valid fields for the matched class
    valid_fields = {f.name for f in fields(p_type)}
    filtered_data = {k: v for k, v in data.items() if k in valid_fields}

    return p_type(**filtered_data)
