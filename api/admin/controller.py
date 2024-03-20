from flask import request
from api.database import connection
import os

def update_version():
    user_agent = request.headers.get('User-Agent')
    expected_header = os.getenv('SECRET_ADMIN_HEADER')
    
    if user_agent != expected_header:
        return {"status": "error", "message": "Unauthorized access."}, 401
    
    version = request.args.get('version')
    if version:
        try:
            try:
                version_value = int(version)
            except ValueError:
                version_value = float(version)
            with connection.cursor() as cursor:
                update_sql = "UPDATE info SET sb_version = %s WHERE id = 1"
                cursor.execute(update_sql, [version_value])
                connection.commit()
                return {"status": "success", "message": "Version updated successfully."}
        except ValueError:
            return {"status": "error", "message": "Version must be an integer or a float."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update version: {e}"}
    else:
        return {"status": "error", "message": "No version provided."}


def update_sb_update_status():
    user_agent = request.headers.get('User-Agent')
    expected_header = os.getenv('SECRET_ADMIN_HEADER')
    if user_agent != expected_header:
        return {"status": "error", "message": "Unauthorized access."}, 401
    update_status = request.args.get('update_status')
    if update_status and update_status.lower() in ['true', 'false']:
        try:
            with connection.cursor() as cursor:
                update_sql = "UPDATE info SET sb_update = %s WHERE id = 1"
                cursor.execute(update_sql, [update_status.lower()])
                connection.commit()
                return {"status": "success", "message": "Update status changed successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to change update status: {e}"}
    else:
        return {"status": "error", "message": "Invalid or no update status provided."}
    


def update_sb_branch():
    user_agent = request.headers.get('User-Agent')
    expected_header = os.getenv('SECRET_ADMIN_HEADER')
    if user_agent != expected_header:
        return {"status": "error", "message": "Unauthorized access."}, 401
    branch_name = request.args.get('branch')
    if branch_name:
        try:
            with connection.cursor() as cursor:
                update_sql = "UPDATE info SET sb_branch = %s WHERE id = 1"
                cursor.execute(update_sql, [branch_name])
                connection.commit()
                return {"status": "success", "message": "Branch updated successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update branch: {e}"}
    else:
        return {"status": "error", "message": "No branch name provided."}

