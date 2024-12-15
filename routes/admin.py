from fastapi import APIRouter, Depends, HTTPException
from auth.jwt_handler import get_current_user

router = APIRouter()

@router.get("/dashboard")
def admin_dashboard(current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Access denied: Admins only")
    return {"message": "Welcome to the admin dashboard"}