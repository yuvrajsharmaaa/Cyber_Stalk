from aquilify.wrappers import Request, Response
from aquilify import shortcuts, responses

from .import (
    db,
    exception
)

import traceback
import os
import uuid
import aiofiles

from datetime import datetime

async def registerReportHome(request: Request) -> Response:
    
    UPLOAD_DIR = "media/evidence"
    try: 
        formData = await request.form()
        file = formData.get("evidence")
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        uid = str(uuid.uuid4())
        filename = file.filename
        ext = os.path.splitext(filename)[1] 

        new_filename = f"{uid}{ext}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := await file.read(1024): 
                await out_file.write(chunk)
                
        insertionStructure = {
            "id": "$auto",
            "incidentType": formData.get("incidentType"),
            "firstOccurrence": formData.get("firstOccurrence"),
            "recentOccurrence": formData.get("recentOccurrence"),
            "description": formData.get("description"),
            "legalCompliance": True if formData.get("legalCompliance") == "on" else False,
            "evidence": {
                "filename": filename,
                "stored_filename": new_filename,
                "extension": ext,
                "file_path": file_path,
                "url": f"{request.url.scheme}://{request.host}/{UPLOAD_DIR}/{new_filename}",
                "datetime": datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            "date": "$date",
            "datetime": "$datetime",
            "status": "Active",
            "resolve": {
                "register": [True ,"Case Registered"]
            }
        }        
        
        if not (await db.collection.insert_one(data = insertionStructure)).success:
            raise exception.CyberSystemException("Insternal server error! please try again.", 409)
        
        return "Report Registered", 200
    
    except exception.CyberSystemException as e:
        return responses.JsonResponse(content = {"error": e.details}, status = e.status)
    
    except Exception as exc:
        traceback.print_exc()
        return responses.JsonResponse(content = {"error": "Internal Server Error"}, status = 500)
    
async def registerReportPage(request: Request) -> Response:
    
    UPLOAD_DIR = "media/evidence"
    try: 
        formData = await request.form()
        file = formData.get("evidenceFiles")
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        uid = str(uuid.uuid4())
        filename = file.filename
        ext = os.path.splitext(filename)[1] 

        new_filename = f"{uid}{ext}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := await file.read(1024): 
                await out_file.write(chunk)
                
        insertionStructure = {
            "id": "$auto",
            "incidentType": formData.get("incidentType"),
            "firstOccurrence": formData.get("firstOccurrence"),
            "recentOccurrence": formData.get("recentOccurrence"),
            "description": formData.get("incidentDescription"),
            "legalCompliance": True if formData.get("safetyCheck") == "on" else False,
            "evidence": {
                "filename": filename,
                "stored_filename": new_filename,
                "extension": ext,
                "file_path": file_path,
                "url": f"{request.url.scheme}://{request.host}/{UPLOAD_DIR}/{new_filename}",
                "datetime": datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            "date": "$date",
            "datetime": "$datetime",
            "status": "Active",
            "resolve": {
                "register": [True ,"Case Registered"]
            }
        }        
        
        if not (await db.collection.insert_one(data = insertionStructure)).success:
            raise exception.CyberSystemException("Insternal server error! please try again.", 409)
        
        return "Report Registered", 200
    
    except exception.CyberSystemException as e:
        return responses.JsonResponse(content = {"error": e.details}, status = e.status)
    
    except Exception as exc:
        traceback.print_exc()
        return responses.JsonResponse(content = {"error": "Internal Server Error"}, status = 500)