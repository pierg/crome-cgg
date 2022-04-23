import hashlib


def generate_goal_id(value: str) -> str:
    id: str = hashlib.sha1(value.encode("UTF-8")).hexdigest()[:5]

    return f"G_{id}"


def generate_goal_operations_name(value: str) -> str:
    id: str = hashlib.sha1(value.encode("UTF-8")).hexdigest()[:5]

    return f"G_{id}"
