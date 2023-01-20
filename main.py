from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import boto3
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import io
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

''''
1. Read the files in chunk
2. Should not load all the bytes into memory - tricky
3. Create zip at clients location - Stream contents directly to zip file at client location
4. Connect the download button and start streaming to browser to zip files
'''

@app.get("/")
def hello_world():
    return "Hello world"


@app.get("/download")
async def download_s3_zip():
    session = boto3.Session(aws_access_key_id='AWS_ACCESS_KEY',
                            aws_secret_access_key='AWS_SECRET_KEY')
    s3_client = session.resource('s3')
    bucket_name = 'filespin-052022'
    s3_bucket = s3_client.Bucket(bucket_name)
    zip_buffer = io.BytesIO()
    chunk_size = 10000


    with zipfile.ZipFile(zip_buffer, mode='w') as zf:
        for file in s3_bucket.objects.all():
            s3_object = s3_client.Object(bucket_name, file.key)

            #reading file as chunks
            zf.writestr(file.key, s3_object.get()['Body'].read(chunk_size))

    # Rewind the buffer
    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type='application/zip',
                             headers={'content-disposition': 'attachment; filename=files.zip'})




if __name__ == "__main__":
    uvicorn.run(app=app, host='0.0.0.0', port=8080)