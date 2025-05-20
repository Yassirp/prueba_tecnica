def structure_beneficiary(beneficiary, contrato_assignment=None, contract=None, department=None, municipality=None, documents=None):
  
    data = {
        "id": getattr(beneficiary, 'id', None),
        "name": getattr(beneficiary, 'name', None),
        "last_name": getattr(beneficiary, 'last_name', None),
        "full_name": f"{getattr(beneficiary, 'name', '')} {getattr(beneficiary, 'last_name', '')}".strip(),
        "cellphone": getattr(beneficiary, 'cellphone', None),
        "document_number": getattr(beneficiary, 'document_number', None),
        "budget_id": getattr(beneficiary, 'budget_id', None),
        # "contract_company": contract_company,
        "id_home": getattr(beneficiary, 'consecutive_number_home', None),
        "vereda": getattr(beneficiary, 'vereda', None)
    }
    if documents:
        data['documents'] = [
            {
                "id": document.id,
                "document_type": document.document_type,
                "url": document.url,
                "associate_id": document.associate_id,
                "associate_to": document.associate_to,
            }
            for document in documents
        ]

    if contrato_assignment:
        data['contractor'] = {
            "id": getattr(contrato_assignment, 'id', None),
            "schema": getattr(contrato_assignment, 'schema', None),
            "gestor_id": getattr(contrato_assignment, 'parent_id', None)
        }
        
    if contract:
        data['contract'] = {
            "id": getattr(contract, 'id', None),
            "document_date": getattr(contract, 'document_date', None),
            "resolution": f"{getattr(contract, 'name', '')} {getattr(contract, 'code', '')} {getattr(contract, 'resolution_number', '')}".strip()
        }

    if department:
        data['department'] = {
            "name": getattr(department, 'name', None),
            "code": getattr(department, 'code', None),
            "id": getattr(department, 'id', None)
        }

    if municipality:
        data['municipality'] = {
            "name": getattr(municipality, 'name', None),
            "code": getattr(municipality, 'code', None),
            "id": getattr(municipality, 'id', None)
        }

    return data
