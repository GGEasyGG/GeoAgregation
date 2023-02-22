point_schema = {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["Point"]
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "number"
                        },
                    "minItems": 2,
                    "maxItems": 2
                    }
            },
            "additionalProperties": False
        }

polygon_schema = {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["Polygon"]
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "number"
                                },
                            "minItems": 2,
                            "maxItems": 2
                            },
                        "minItems": 1
                        },
                    "minItems": 1
                    }
            },
            "additionalProperties": False
        }
