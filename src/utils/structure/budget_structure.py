from utils.structure.beneficiary_structure import structure_beneficiary


def structure_budget_data(budget, beneficiary=None, contract_assignment=None, contract=None, department=None, municipality=None,documents=None):
        return {
            "id": getattr(budget, "id", None),
            "code": getattr(budget, "code", None),
            "contractor_id": getattr(budget, "contractor_id", None),
            "contract_id": getattr(budget, "contract_id", None),
            "department_id": getattr(budget, "department_id", None),
            "municipality_id": getattr(budget, "municipality_id", None),
            "village": getattr(budget, "village", None),
            "beneficiary_id": getattr(budget, "beneficiary_id", None),
            "documents": [
                {
                    "id": document.id,
                    "document_type": document.document_type,
                    "url": document.url,
                    "associate_id": document.associate_id,
                    "associate_to": document.associate_to,
                } for document in documents
            ] if documents else None,
            "beneficiary": structure_beneficiary(beneficiary, contract_assignment, contract, department, municipality) if beneficiary else None,
            "resolution_id": getattr(budget, "resolution_id", None),
            "improvement_type": {
                "id": getattr(budget.improvement_type, "id", None),
                "name": getattr(budget.improvement_type, "value", None)
            } if getattr(budget, "improvement_type", None) else None,
            "minimum_salary": {
                "id": getattr(budget.minimum_salary, "id", None),
                "value": getattr(budget.minimum_salary, "value", None)
            } if getattr(budget, "minimum_salary", None) else None,
            "scheme_type": {
                "id": getattr(budget.scheme_type, "id", None),
                "value": getattr(budget.scheme_type, "value", None)
            } if getattr(budget, "scheme_type", None) else None,
            "status": {
                "id": getattr(budget.status, "id", None),
                "name": getattr(budget.status, "name", None)
            } if getattr(budget, "status", None) else None,
            "budget_status_changes": [
                {
                    "user_id": getattr(observation, "user_id", None),
                    "observations": getattr(observation, "observations", None),
                    "type": {
                        "id": getattr(getattr(observation, "type", None), "id", None),
                        "value": getattr(getattr(observation, "type", None), "value", None)                        
                    },
                    "status": {
                        "id": getattr(getattr(observation, "status", None), "id", None),
                        "name": getattr(getattr(observation, "status", None), "name", None)
                    }
                } for observation in getattr(budget, 'observations', []) or []
            ],
            "budget_category": [
                {
                    "id": getattr(category, "id", None),
                    "category": {
                        "name": getattr(getattr(getattr(category, "categories_region", None), "category", None), "name", None),
                        "id": getattr(category, "category_id", None),
                    },
                    "budget_subcategory": [
                        {
                            "id": getattr(subcategory, "id", None),
                            **({
                                "timeline": {
                                    "start_date": getattr(subcategory.timeline, "start_date", None),
                                    "end_date": getattr(subcategory.timeline, "end_date", None),
                                }
                            } if getattr(subcategory, "timeline", None) else {}),
                            "subcategory": {
                                "id": getattr(getattr(subcategory, "subcategory", None), "id", None),
                                "name": getattr(getattr(subcategory, "subcategory", None), "name", None),
                                "apu": getattr(getattr(subcategory, "subcategory", None), "apu", None),
                                "total_value": getattr(getattr(subcategory, "subcategory", None), "total_value", None),
                            },
                            "quantities": [
                                {
                                    "id": getattr(quantity, "id", None),
                                    "location": getattr(quantity, "location", None),
                                    "height": getattr(quantity, "height", None),
                                    "width": getattr(quantity, "width", None),
                                    "length": getattr(quantity, "length", None),
                                    "quantity": getattr(quantity, "quantity", None),
                                    "subtotal": getattr(quantity, "subtotal", None),
                                    "total": {
                                        "id": getattr(getattr(quantity, "total", None), "id", None),
                                        "total": getattr(getattr(quantity, "total", None), "total", None)
                                    } if getattr(quantity, "total", None) else None,
                                    "discounts": [
                                        {
                                            "element": getattr(discount, "element", None),
                                            "height": getattr(discount, "height", None),
                                            "width": getattr(discount, "width", None),
                                            "length": getattr(discount, "length", None),
                                            "quantity": getattr(discount, "quantity", None),
                                            "subtotal": getattr(discount, "subtotal", None),
                                        } for discount in getattr(quantity, "discounts", []) or []
                                    ]
                                } for quantity in getattr(subcategory, "quantity_details", []) or []
                            ],
                            "total_quantity": getattr(subcategory, "total_quantity", None),
                            "total_value": getattr(subcategory, "total_value", None),
                        } for subcategory in getattr(category, "subcategories", []) or []
                    ]
                } for category in getattr(budget, "categories", []) or []
            ],
            "legal_minimum_wages": getattr(budget, "legal_minimum_wages", None),
            "budget_details": [
                {
                    "id": getattr(budget_detail, "id", None),
                    "concept": {
                        "id": getattr(getattr(budget_detail, "concept", None), "id", None),
                        "value": getattr(getattr(budget_detail, "concept", None), "value", None),
                    } if getattr(budget_detail, "concept", None) else None,
                    "type": {
                        "id": getattr(getattr(budget_detail, "type", None), "id", None),
                        "value": getattr(getattr(budget_detail, "type", None), "value", None),
                    } if getattr(budget_detail, "type", None) else None,
                    "value": getattr(budget_detail, "value", None),
                    "percentage": getattr(budget_detail, "percentage", None),
                } for budget_detail in getattr(budget, "budget_details", []) or []
            ],
            "subtotal_direct_costs": float(getattr(budget, "subtotal_direct_costs", 0) or 0),
            "subtotal_indirect_costs": float(getattr(budget, "subtotal_indirect_costs", 0) or 0),
            "total_diagnosis": float(getattr(budget, "total_diagnosis", 0) or 0),
            "total_budget": float(getattr(budget, "total_budget", 0) or 0),
            "presentation_date": str(budget.presentation_date) if getattr(budget, "presentation_date", None) else None,
            "valid_year": getattr(budget, "valid_year", None),
            "total_days_execution": max(
                (
                    getattr(subcategory.timeline, "end_date", 0)
                    for category in getattr(budget, "categories", []) or []
                    for subcategory in getattr(category, "subcategories", []) or []
                    if getattr(subcategory, "timeline", None) and getattr(subcategory.timeline, "end_date", None)
                ),
                default=0
            )
        }
    