from typing import Any, Dict


def _filter_form_fields(field: Dict[str, Any]) -> bool:
    return (
        (
            isinstance(field.get("answer"), str)
            or isinstance(field.get("answerArray"), list)
            or field.get("isHeader") is not None
        )
        and field.get("_id") is not None
        and field.get("fieldType") is not None
        and field.get("question") is not None
    )


def determine_is_form_fields(tbd: Any) -> bool:
    if not isinstance(tbd, list):
        return False

    filtered = list(filter(lambda internal: _filter_form_fields(internal), tbd))
    return len(filtered) == len(tbd)
