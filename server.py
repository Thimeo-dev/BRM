from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI()

# Autorise ton site web à interroger ce serveur (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Chargement du modèle rembg (u2net_p)...")
# On utilise u2net_p (version allégée) pour ne pas saturer la RAM gratuite de Render
session = new_session("u2net_p")
print("Modèle chargé ! Le serveur est prêt.")

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        input_image = Image.open(io.BytesIO(image_data))
        
        # Traitement de suppression du fond
        output_image = remove(input_image, session=session)
        
        # Préparation de l'image de sortie en PNG
        output_io = io.BytesIO()
        output_image.save(output_io, "PNG")
        output_io.seek(0)
        
        return Response(content=output_io.getvalue(), media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}, 500
