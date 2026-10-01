from fastapi import HTTPException

POLICY = {
    "READ": True,
    "WRITE": True,
    "EXECUTE": False,
    "NETWORK": True,
    "AUTONOMY_LEVEL": 1
}

def get_policy():
    return POLICY

def update_policy(autonomy_level: int, allow_network: bool, allow_file_write: bool, allow_execute: bool = False):
    POLICY["AUTONOMY_LEVEL"] = autonomy_level
    POLICY["NETWORK"] = allow_network
    POLICY["WRITE"] = allow_file_write
    POLICY["EXECUTE"] = allow_execute or (autonomy_level >= 2)
    return POLICY

def require_permission(permission_type: str):
    if not POLICY.get(permission_type, False):
        raise HTTPException(
            status_code=403, 
            detail=f"Action blocked: '{permission_type}' permission is disabled under Autonomy Level {POLICY['AUTONOMY_LEVEL']}."
        )