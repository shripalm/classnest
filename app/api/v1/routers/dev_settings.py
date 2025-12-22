import subprocess
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.response import StandardResponse
from app.utils.response import success_response
from app.db.session import get_db
from app.services import upload

router = APIRouter()


class MockUploadFile:
    def __init__(self, file_path: str):
        self.filename = file_path.split('/')[-1]
        self.file_path = file_path

    async def read(self):
        with open(self.file_path, 'rb') as f:
            return f.read()



@router.get("/db_seed", response_model=StandardResponse[dict])
async def db_seed(
    db: AsyncSession = Depends(get_db)
):
    """Seed the database with dummy data."""
    try:
        # Read and execute seed data
        with open("dummy_data_insert.sql", "r") as f:
            sql_script = f.read()

        statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]

        for stmt in statements:
            await db.execute(text(stmt))

        await db.commit()

        # Process the CSV file for contact imports
        try:
            csv_file_path = "uploading-files/test_uploadCSV_200.csv"
            mock_file = MockUploadFile(csv_file_path)
            file_content = await mock_file.read()
            upload_result = await upload.process_file(
                db=db,
                file_content=file_content,
                filename="test_uploadCSV_200.csv"
            )
        except Exception as e:
            # Log the error but don't fail the seeding
            print(f"File upload processing skipped or failed: {str(e)}")

        return success_response(data={"status": "DB Seeding Service ran successfully"})
    except Exception as e:
        if 'db' in locals():
            await db.rollback()
        raise HTTPException(status_code=500, detail=f"DB seeding failed: {str(e)}")
