from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI()

# Path to your saved fine-tuned model (make sure this directory matches what you saved in train_model.py)
model_path = "./my-medical-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Define request and response schemas using Pydantic
class InferenceRequest(BaseModel):
    transcript: str

class InferenceResponse(BaseModel):
    doctor_notes: str

@app.post("/generate-notes", response_model=InferenceResponse)
def generate_notes(request: InferenceRequest):
    try:
        # Encode the transcript into model input tokens
        inputs = tokenizer.encode(request.transcript, return_tensors="pt", truncation=True, max_length=512)
        
        # Generate output tokens using beam search (or adjust parameters as needed)
        outputs = model.generate(inputs, max_length=128, num_beams=5, early_stopping=True)
        
        # Decode the generated tokens back into a human-readable string
        doctor_notes = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return InferenceResponse(doctor_notes=doctor_notes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI server on host 0.0.0.0 and port 8000 in development mode
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
