def single_layer_schema_validator(schema, supported_types):
    if not schema:
        return False

    for attribute, attribute_type in schema.items():
        if attribute_type not in supported_types:
            return False
    
    return True
    
    