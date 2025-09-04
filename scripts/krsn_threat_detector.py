#!/usr/bin/env python3
"""
KRSN-RT2I Real-Time Threat Detection API Integration
===================================================

Real-time threat detection service for integration with the KRSN-RT2I platform.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KRSNThreatDetector:
    """KRSN-RT2I Real-Time Threat Detection System."""
    
    def __init__(self, models_dir: str = "./models"):
        """Initialize the threat detector."""
        self.models_dir = Path(models_dir)
        self.models = {}
        self.scaler = None
        self.is_trained = False
        self.feature_names = []
        
        # Create models directory
        self.models_dir.mkdir(exist_ok=True)
        
        # Try to load existing models
        self._load_models()
    
    def train_on_dataset(self, data_path: str = "./data/train.csv") -> Dict[str, Any]:
        """Train the threat detection models on the provided dataset."""
        logger.info("🚀 KRSN-RT2I Threat Detection Training Started")
        
        try:
            # Load and prepare data
            logger.info(f"📊 Loading dataset from {data_path}")
            
            # Handle large dataset efficiently
            chunk_size = 10000
            sample_data = pd.read_csv(data_path, nrows=chunk_size, header=None)
            
            logger.info(f"📈 Loaded sample data: {sample_data.shape}")
            
            # Prepare features and labels
            X = sample_data.iloc[:, :-1].values  # All columns except last
            y_labels = sample_data.iloc[:, -1].values  # Last column as labels
            
            # Create binary classification (most common label = normal)
            unique_labels, counts = np.unique(y_labels, return_counts=True)
            normal_label = unique_labels[np.argmax(counts)]
            
            y = (y_labels != normal_label).astype(int)  # 0 = normal, 1 = threat
            
            logger.info(f"📊 Dataset summary:")
            logger.info(f"   - Samples: {X.shape[0]:,}")
            logger.info(f"   - Features: {X.shape[1]}")
            logger.info(f"   - Normal: {np.sum(y == 0):,}")
            logger.info(f"   - Threats: {np.sum(y == 1):,}")
            logger.info(f"   - Threat rate: {np.mean(y):.2%}")
            
            # Handle non-numeric data
            X = pd.DataFrame(X).fillna(0).values.astype(float)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale features
            logger.info("📊 Scaling features...")
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train models
            models_config = {
                'random_forest': RandomForestClassifier(
                    n_estimators=100, 
                    max_depth=15,
                    random_state=42, 
                    n_jobs=-1
                ),
                'anomaly_detector': IsolationForest(
                    contamination=0.1, 
                    random_state=42,
                    n_jobs=-1
                )
            }
            
            results = {}
            
            for model_name, model in models_config.items():
                logger.info(f"🧠 Training {model_name}...")
                
                if model_name == 'anomaly_detector':
                    # Train on normal data only
                    normal_indices = y_train == 0
                    model.fit(X_train_scaled[normal_indices])
                    
                    # Test
                    y_pred = model.predict(X_test_scaled)
                    y_pred = np.where(y_pred == -1, 1, 0)
                    accuracy = accuracy_score(y_test, y_pred)
                    
                    logger.info(f"   ✅ Anomaly Detection Accuracy: {accuracy:.4f}")
                    
                else:
                    # Regular classification
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    accuracy = accuracy_score(y_test, y_pred)
                    
                    logger.info(f"   ✅ Classification Accuracy: {accuracy:.4f}")
                    
                    # Detailed metrics
                    report = classification_report(y_test, y_pred, output_dict=True)
                    if '1' in report:  # Threat class
                        precision = report['1']['precision']
                        recall = report['1']['recall']
                        f1 = report['1']['f1-score']
                        logger.info(f"   📊 Threat Detection - P: {precision:.3f}, R: {recall:.3f}, F1: {f1:.3f}")
                
                self.models[model_name] = model
                results[model_name] = {'accuracy': accuracy}
            
            # Save models
            self._save_models()
            self.is_trained = True
            
            logger.info("✅ Training completed successfully!")
            return results
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            return {}
    
    def predict_threat(self, network_features: List[float]) -> Dict[str, Any]:
        """Predict if network traffic is a threat."""
        if not self.is_trained:
            return {"error": "Model not trained. Call train_on_dataset() first."}
        
        try:
            # Prepare features
            if isinstance(network_features, list):
                features = np.array([network_features])
            else:
                features = np.array([network_features])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Get predictions from all models
            predictions = {}
            
            # Random Forest prediction
            if 'random_forest' in self.models:
                rf_pred = self.models['random_forest'].predict(features_scaled)[0]
                rf_proba = self.models['random_forest'].predict_proba(features_scaled)[0]
                
                predictions['classification'] = {
                    'is_threat': bool(rf_pred == 1),
                    'confidence': float(max(rf_proba)),
                    'threat_probability': float(rf_proba[1]) if len(rf_proba) > 1 else 0.0
                }
            
            # Anomaly detection
            if 'anomaly_detector' in self.models:
                anom_pred = self.models['anomaly_detector'].predict(features_scaled)[0]
                anom_score = self.models['anomaly_detector'].decision_function(features_scaled)[0]
                
                predictions['anomaly'] = {
                    'is_anomaly': bool(anom_pred == -1),
                    'anomaly_score': float(anom_score)
                }
            
            # Ensemble decision
            is_threat = False
            confidence = 0.0
            
            if 'classification' in predictions:
                is_threat = predictions['classification']['is_threat']
                confidence = predictions['classification']['confidence']
            
            # Combine with anomaly detection
            if 'anomaly' in predictions and predictions['anomaly']['is_anomaly']:
                is_threat = True
                confidence = max(confidence, 0.7)  # High confidence for anomalies
            
            # Determine severity
            if is_threat:
                if confidence > 0.8:
                    severity = "HIGH"
                elif confidence > 0.6:
                    severity = "MEDIUM"
                else:
                    severity = "LOW"
            else:
                severity = "NORMAL"
            
            return {
                "is_threat": is_threat,
                "confidence": confidence,
                "severity": severity,
                "threat_type": "Network Anomaly" if is_threat else "Normal Traffic",
                "timestamp": datetime.now().isoformat(),
                "detailed_predictions": predictions
            }
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def batch_analyze(self, traffic_batch: List[List[float]]) -> Dict[str, Any]:
        """Analyze a batch of network traffic samples."""
        results = []
        threat_count = 0
        
        for i, sample in enumerate(traffic_batch):
            prediction = self.predict_threat(sample)
            prediction['sample_id'] = i
            
            if prediction.get('is_threat', False):
                threat_count += 1
            
            results.append(prediction)
        
        return {
            "total_samples": len(traffic_batch),
            "threats_detected": threat_count,
            "threat_rate": threat_count / len(traffic_batch) if traffic_batch else 0,
            "analysis_timestamp": datetime.now().isoformat(),
            "results": results
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the trained models."""
        return {
            "is_trained": self.is_trained,
            "models_available": list(self.models.keys()),
            "models_directory": str(self.models_dir),
            "feature_count": len(self.feature_names) if self.feature_names else 0
        }
    
    def _save_models(self):
        """Save trained models to disk."""
        try:
            # Save individual models
            for model_name, model in self.models.items():
                model_path = self.models_dir / f'{model_name}.pkl'
                joblib.dump(model, model_path)
                logger.info(f"💾 Saved {model_name} to {model_path}")
            
            # Save scaler
            if self.scaler:
                scaler_path = self.models_dir / 'scaler.pkl'
                joblib.dump(self.scaler, scaler_path)
                logger.info(f"💾 Saved scaler to {scaler_path}")
            
            # Save metadata
            metadata = {
                'training_timestamp': datetime.now().isoformat(),
                'models': list(self.models.keys()),
                'is_trained': True
            }
            
            with open(self.models_dir / 'metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"📊 Models saved to {self.models_dir}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save models: {e}")
    
    def _load_models(self):
        """Load existing models from disk."""
        try:
            metadata_path = self.models_dir / 'metadata.json'
            
            if not metadata_path.exists():
                logger.info("📋 No existing models found")
                return
            
            # Load metadata
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            if not metadata.get('is_trained', False):
                return
            
            # Load scaler
            scaler_path = self.models_dir / 'scaler.pkl'
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
                logger.info("✅ Loaded scaler")
            
            # Load models
            for model_name in metadata.get('models', []):
                model_path = self.models_dir / f'{model_name}.pkl'
                if model_path.exists():
                    self.models[model_name] = joblib.load(model_path)
                    logger.info(f"✅ Loaded {model_name}")
            
            self.is_trained = len(self.models) > 0
            
            if self.is_trained:
                logger.info(f"🔄 Loaded {len(self.models)} trained models")
            
        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")


# Convenience functions for easy integration
def train_threat_detector(data_path: str = "./data/train.csv") -> KRSNThreatDetector:
    """Train and return a threat detector."""
    detector = KRSNThreatDetector()
    results = detector.train_on_dataset(data_path)
    
    if results:
        logger.info("🎉 Threat detector training completed!")
        logger.info(f"📊 Model performance: {results}")
    else:
        logger.error("❌ Training failed!")
    
    return detector

def load_threat_detector() -> KRSNThreatDetector:
    """Load an existing threat detector."""
    detector = KRSNThreatDetector()
    
    if detector.is_trained:
        logger.info("✅ Loaded existing threat detector")
    else:
        logger.warning("⚠️ No trained models found. Train first with train_threat_detector()")
    
    return detector

def quick_test():
    """Quick test of the threat detection system."""
    print("🚀 KRSN-RT2I Threat Detection - Quick Test")
    print("=" * 50)
    
    try:
        # Create synthetic test data
        logger.info("📊 Creating test data...")
        
        # Normal traffic pattern
        normal_sample = [100, 80, 443, 1500, 0, 1, 0, 0, 1] + [0] * 30
        
        # Suspicious traffic pattern
        attack_sample = [100, 80, 22, 50000, 1, 0, 1, 1, 0] + [5] * 30
        
        # Initialize detector
        detector = KRSNThreatDetector()
        
        # Quick training with synthetic data
        logger.info("🧠 Quick training...")
        
        # Create synthetic training data
        np.random.seed(42)
        n_samples = 1000
        n_features = 39
        
        X_normal = np.random.normal(0, 1, (n_samples//2, n_features))
        X_attack = np.random.normal(2, 1.5, (n_samples//2, n_features))
        
        X = np.vstack([X_normal, X_attack])
        y = np.hstack([np.zeros(n_samples//2), np.ones(n_samples//2)])
        
        # Quick train
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        detector.scaler = StandardScaler()
        X_train_scaled = detector.scaler.fit_transform(X_train)
        X_test_scaled = detector.scaler.transform(X_test)
        
        # Train models
        detector.models['random_forest'] = RandomForestClassifier(n_estimators=50, random_state=42)
        detector.models['random_forest'].fit(X_train_scaled, y_train)
        
        detector.models['anomaly_detector'] = IsolationForest(contamination=0.2, random_state=42)
        detector.models['anomaly_detector'].fit(X_train_scaled[y_train == 0])
        
        detector.is_trained = True
        
        # Test predictions
        logger.info("🧪 Testing predictions...")
        
        normal_result = detector.predict_threat(normal_sample)
        attack_result = detector.predict_threat(attack_sample)
        
        print(f"\n🔍 Test Results:")
        print(f"📡 Normal Traffic: {normal_result['threat_type']} (Confidence: {normal_result['confidence']:.3f})")
        print(f"🚨 Attack Traffic: {attack_result['threat_type']} (Confidence: {attack_result['confidence']:.3f})")
        
        # Batch test
        batch_results = detector.batch_analyze([normal_sample, attack_sample, normal_sample])
        print(f"\n📈 Batch Analysis:")
        print(f"   Total: {batch_results['total_samples']}")
        print(f"   Threats: {batch_results['threats_detected']}")
        print(f"   Rate: {batch_results['threat_rate']:.1%}")
        
        print(f"\n✅ KRSN-RT2I Threat Detection System - OPERATIONAL! 🚀")
        
        return detector
        
    except Exception as e:
        logger.error(f"❌ Quick test failed: {e}")
        return None


if __name__ == "__main__":
    # Run quick test
    detector = quick_test()
    
    if detector:
        print(f"\n🔧 Integration Example:")
        print(f"```python")
        print(f"from scripts.krsn_threat_detector import load_threat_detector")
        print(f"")
        print(f"# Load detector")
        print(f"detector = load_threat_detector()")
        print(f"")
        print(f"# Analyze network traffic")
        print(f"result = detector.predict_threat(network_features)")
        print(f"if result['is_threat']:")
        print(f"    print(f'🚨 THREAT DETECTED: {{result[\"severity\"]}} severity')")
        print(f"```")
        
        print(f"\n🎉 Ready for KRSN-RT2I platform integration!")
