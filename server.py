import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = None

def get_session():
    global session
    if session is None:
        print("Chargement du modèle rembg (u2net_p)...")
        session = new_session("u2net_p")
        print("Modèle chargé avec succès !")
    return session

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        input_image = Image.open(io.BytesIO(image_data))
        
        current_session = get_session()
        output_image = remove(input_image, session=current_session)
        
        output_io = io.BytesIO()
        output_image.save(output_io, "PNG")
        output_io.seek(0)
        
        return Response(content=output_io.getvalue(), media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    # Récupère automatiquement le port attribué par Render (ou 10000 par défaut)
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
