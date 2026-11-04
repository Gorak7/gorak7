PROMPTS={
'v1': 'Create valid API test cases from this OpenAPI spec. Return only JSON array. Spec: {spec}',
'v2': 'Act as a senior QA engineer. Generate positive, negative, boundary and authentication API cases from this OpenAPI spec. Return only a JSON array matching the schema: name, operation_id, method, path, expected_status, category, rationale. Do not invent operations or success codes. Include unanswerable or invalid input cases only when supported by the contract. Spec: {spec}'
}
