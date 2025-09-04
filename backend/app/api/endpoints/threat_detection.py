"""
KRSN-RT2I Threat Detection API Integration
==========================================

FastAPI integration for real-time threat detection using the trained AI model.
Add this to your backend/app/api/endpoints/ directory.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Import our trained threat detector
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from scripts.krsn_threat_detector import KRSNThreatDetector, load_threat_detector

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/threat-detection", tags=["AI Threat Detection"])

# Global detector instance
threat_detector = None

def get_threat_detector():
    """Get or initialize the threat detector."""
    global threat_detector
    if threat_detector is None:
        threat_detector = load_threat_detector()
    return threat_detector

# Pydantic models for API
class NetworkTrafficData(BaseModel):
    """Network traffic data for analysis."""
    features: List[float]
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = {}

class BatchTrafficData(BaseModel):
    """Batch network traffic data for analysis."""
    traffic_samples: List[NetworkTrafficData]
    batch_id: Optional[str] = None

class ThreatAnalysisResponse(BaseModel):
    """Threat analysis response."""
    is_threat: bool
    confidence: float
    severity: str
    threat_type: str
    timestamp: str
    detailed_predictions: Dict[str, Any]
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None

class BatchAnalysisResponse(BaseModel):
    """Batch analysis response."""
    total_samples: int
    threats_detected: int
    threat_rate: float
    analysis_timestamp: str
    batch_id: Optional[str] = None
    results: List[ThreatAnalysisResponse]

# API Endpoints

@router.post("/analyze", response_model=ThreatAnalysisResponse)
async def analyze_network_traffic(
    traffic_data: NetworkTrafficData,
    background_tasks: BackgroundTasks
):
    """
    Analyze network traffic for threats in real-time.
    
    Features should be a list of 39 numerical values representing:
    - Header_Length, Protocol Type, Time_To_Live, Rate, etc.
    """
    try:
        detector = get_threat_detector()
        
        if not detector.is_trained:
            raise HTTPException(
                status_code=503, 
                detail="AI model not trained. Please train the model first."
            )
        
        # Validate features
        if len(traffic_data.features) != 39:
            raise HTTPException(
                status_code=400,
                detail=f"Expected 39 features, got {len(traffic_data.features)}"
            )
        
        # Perform threat analysis
        result = detector.predict_threat(traffic_data.features)
        
        if 'error' in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        # If threat detected, trigger background alert processing
        if result['is_threat']:
            background_tasks.add_task(
                process_threat_alert, 
                result, 
                traffic_data.source_ip, 
                traffic_data.destination_ip
            )
        
        # Prepare response
        response = ThreatAnalysisResponse(
            **result,
            source_ip=traffic_data.source_ip,
            destination_ip=traffic_data.destination_ip
        )
        
        logger.info(f"Threat analysis completed: {result['threat_type']} - {result['severity']}")
        
        return response
        
    except Exception as e:
        logger.error(f"Threat analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-batch", response_model=BatchAnalysisResponse)
async def analyze_batch_traffic(
    batch_data: BatchTrafficData,
    background_tasks: BackgroundTasks
):
    """
    Analyze multiple network traffic samples in batch.
    Useful for historical analysis or bulk processing.
    """
    try:
        detector = get_threat_detector()
        
        if not detector.is_trained:
            raise HTTPException(
                status_code=503,
                detail="AI model not trained. Please train the model first."
            )
        
        # Validate batch data
        if not batch_data.traffic_samples:
            raise HTTPException(
                status_code=400,
                detail="No traffic samples provided"
            )
        
        # Extract features for batch analysis
        features_batch = []
        sample_metadata = []
        
        for sample in batch_data.traffic_samples:
            if len(sample.features) != 39:
                raise HTTPException(
                    status_code=400,
                    detail=f"All samples must have 39 features"
                )
            
            features_batch.append(sample.features)
            sample_metadata.append({
                'source_ip': sample.source_ip,
                'destination_ip': sample.destination_ip,
                'timestamp': sample.timestamp,
                'metadata': sample.metadata
            })
        
        # Perform batch analysis
        batch_result = detector.batch_analyze(features_batch)
        
        # Prepare detailed results
        detailed_results = []
        threat_count = 0
        
        for i, result in enumerate(batch_result['results']):
            if 'error' not in result:
                metadata = sample_metadata[i]
                
                detailed_result = ThreatAnalysisResponse(
                    **result,
                    source_ip=metadata['source_ip'],
                    destination_ip=metadata['destination_ip']
                )
                
                detailed_results.append(detailed_result)
                
                # Count threats for background processing
                if result['is_threat']:
                    threat_count += 1
        
        # If threats detected, trigger background alert processing
        if threat_count > 0:
            background_tasks.add_task(
                process_batch_threat_alerts,
                detailed_results,
                batch_data.batch_id
            )
        
        response = BatchAnalysisResponse(
            total_samples=batch_result['total_samples'],
            threats_detected=batch_result['threats_detected'],
            threat_rate=batch_result['threat_rate'],
            analysis_timestamp=batch_result['analysis_timestamp'],
            batch_id=batch_data.batch_id,
            results=detailed_results
        )
        
        logger.info(f"Batch analysis completed: {threat_count}/{len(features_batch)} threats detected")
        
        return response
        
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-status")
async def get_model_status():
    """Get the status of the AI threat detection model."""
    try:
        detector = get_threat_detector()
        model_info = detector.get_model_info()
        
        return {
            "status": "operational" if detector.is_trained else "not_trained",
            "model_info": model_info,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get model status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train-model")
async def train_model(
    background_tasks: BackgroundTasks,
    data_path: str = "./data/train.csv"
):
    """
    Train the AI model on the provided dataset.
    This is a long-running operation that runs in the background.
    """
    try:
        # Trigger training in background
        background_tasks.add_task(train_model_background, data_path)
        
        return {
            "message": "Model training started in background",
            "data_path": data_path,
            "started_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start model training: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background tasks

async def process_threat_alert(
    threat_result: Dict[str, Any], 
    source_ip: Optional[str] = None, 
    destination_ip: Optional[str] = None
):
    """Process threat alert in background."""
    try:
        logger.warning(f"THREAT DETECTED: {threat_result['threat_type']} - {threat_result['severity']}")
        
        # Here you can add integration with:
        # - Alert system
        # - SIEM integration
        # - Notification services
        # - Database logging
        # - Grafana dashboards
        
        # Example: Save to database
        # await save_threat_to_database(threat_result, source_ip, destination_ip)
        
        # Example: Send to alert queue
        # await send_to_alert_queue(threat_result)
        
    except Exception as e:
        logger.error(f"Failed to process threat alert: {e}")

async def process_batch_threat_alerts(
    threat_results: List[ThreatAnalysisResponse],
    batch_id: Optional[str] = None
):
    """Process batch threat alerts in background."""
    try:
        threat_count = len([r for r in threat_results if r.is_threat])
        
        logger.warning(f"BATCH THREATS DETECTED: {threat_count} threats in batch {batch_id}")
        
        # Process each threat
        for result in threat_results:
            if result.is_threat:
                await process_threat_alert(
                    result.dict(), 
                    result.source_ip, 
                    result.destination_ip
                )
        
    except Exception as e:
        logger.error(f"Failed to process batch threat alerts: {e}")

async def train_model_background(data_path: str):
    """Train the AI model in background."""
    try:
        logger.info(f"Starting model training with data: {data_path}")
        
        from scripts.krsn_threat_detector import train_threat_detector
        
        # Train the model
        detector = train_threat_detector(data_path)
        
        if detector.is_trained:
            logger.info("Model training completed successfully")
            
            # Update global detector
            global threat_detector
            threat_detector = detector
            
        else:
            logger.error("Model training failed")
            
    except Exception as e:
        logger.error(f"Background model training failed: {e}")

# Example usage and testing endpoints

@router.get("/test-detection")
async def test_threat_detection():
    """Test the threat detection with sample data."""
    try:
        detector = get_threat_detector()
        
        if not detector.is_trained:
            return {"error": "Model not trained"}
        
        # Test samples
        test_samples = [
            {
                "name": "Normal Traffic",
                "features": [64, 6, 80, 1024, 0, 1, 0, 0, 1, 0, 0, 10, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 100, 50, 150, 75, 25, 2048, 0.1, 1, 0.5]
            },
            {
                "name": "Suspicious Activity",
                "features": [32, 6, 22, 0, 1, 0, 1, 0, 0, 0, 0, 100, 0, 10, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 1000, 500, 500, 0, 5.0, 100, 10.0]
            }
        ]
        
        results = []
        for sample in test_samples:
            result = detector.predict_threat(sample["features"])
            result["sample_name"] = sample["name"]
            results.append(result)
        
        return {"test_results": results}
        
    except Exception as e:
        return {"error": str(e)}

# Add this router to your main FastAPI app:
# app.include_router(router)
