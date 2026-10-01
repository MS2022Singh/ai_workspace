from fastapi import Request, HTTPException

CURRENT_PERMISSION_LEVEL = 2 # Default: Standard Access

def enforce_permission(required_level: int):
    if CURRENT_PERMISSION_LEVEL < required_level:
        raise HTTPException(status_code=403, detail=f'Permission Denied: Level {required_level} required.')
    return True
