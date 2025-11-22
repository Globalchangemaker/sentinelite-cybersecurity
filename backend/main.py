from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import json

# Initialize FastAPI app
app = FastAPI(title="SentinelLite Backend", version="1.0.0")

# CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ThreatRequest(BaseModel):
    network_data: dict
    user_behavior: dict

class ThreatResponse(BaseModel):
    threat_detected: bool
    threat_type: str
    confidence: float
    action_taken: str
    timestamp: str

# Your actual AI detection logic (simplified for now)
def analyze_threat(network_data: dict, user_behavior: dict) -> ThreatResponse:
    """
    AI threat detection - you can add your actual AUIP logic here later
    """
    # Simulate AI analysis - REPLACE THIS WITH YOUR ACTUAL AI CODE
    source_ip = network_data.get("source_ip", "")
    
    # Simple rule-based detection for demo
    is_threat = "fake" in str(network_data.get("destination", "")).lower()
    threat_type = "phishing" if is_threat else "none"
    confidence = 0.92 if is_threat else 0.15
    
    return ThreatResponse(
        threat_detected=is_threat,
        threat_type=threat_type,
        confidence=confidence,
        action_taken="block_ip" if is_threat else "monitor",
        timestamp=datetime.now().isoformat()
    )

# In-memory storage for demo (replace with database later)
threat_logs = []

# API Routes
@app.get("/")
async def root():
    return {"message": "SentinelLite Backend API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/detect-threat", response_model=ThreatResponse)
async def detect_threat(request: ThreatRequest):
    try:
        # Process with your AI engine
        result = analyze_threat(request.network_data, request.user_behavior)
        
        # Log the detection
        threat_logs.append({
            "timestamp": result.timestamp,
            "threat_detected": result.threat_detected,
            "threat_type": result.threat_type,
            "confidence": result.confidence
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/system-stats")
async def get_system_stats():
    total_threats = len([log for log in threat_logs if log["threat_detected"]])
    
    return {
        "threats_blocked": total_threats,
        "uptime_days": 15,
        "active_devices": 8,
        "detection_accuracy": 0.987,
        "total_scans": len(threat_logs)
    }

@app.get("/threat-logs")
async def get_threat_logs():
    return {"threats": threat_logs[-10:]}  # Last 10 entries

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)