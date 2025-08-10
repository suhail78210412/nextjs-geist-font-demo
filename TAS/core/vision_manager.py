"""
Vision Manager for TAS
Handles camera operations and face recognition
"""

import logging
import cv2
import numpy as np
from typing import Optional, Dict, Any
import face_recognition
from pathlib import Path
import pickle

class VisionManager:
    def __init__(self, config, consent_manager):
        self.config = config
        self.consent_manager = consent_manager
        self.logger = logging.getLogger('TAS.Vision')
        self.camera = None
        self.known_faces = {}
        self.face_data_path = Path.home() / '.tas' / 'faces.pkl'
        
    async def initialize(self):
        """Initialize vision system"""
        if not self.consent_manager.get_camera_consent():
            self.logger.info("Camera consent not given, vision system disabled")
            return
            
        self._load_known_faces()
        self.logger.info("Vision manager initialized")
        
    def _load_known_faces(self):
        """Load known faces from storage"""
        if self.face_data_path.exists():
            with open(self.face_data_path, 'rb') as f:
                self.known_faces = pickle.load(f)
                
    def _save_known_faces(self):
        """Save known faces to storage"""
        with open(self.face_data_path, 'wb') as f:
            pickle.dump(self.known_faces, f)
            
    async def start_monitoring(self):
        """Start camera monitoring"""
        if not self.consent_manager.get_camera_consent():
            return
            
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            self.logger.error("Failed to open camera")
            return
            
        while True:
            ret, frame = self.camera.read()
            if ret:
                await self._process_frame(frame)
            await asyncio.sleep(1)
            
    async def _process_frame(self, frame):
        """Process camera frame for face detection"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    list(self.known_faces.values()), 
                    face_encoding
                )
                
                if True in matches:
                    # Known person detected
                    name = list(self.known_faces.keys())[matches.index(True)]
                    self.logger.info(f"Detected known person: {name}")
                else:
                    # Unknown person - ask for name
                    self.logger.info("Unknown person detected")
                    
    async def shutdown(self):
        """Shutdown vision system"""
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()
