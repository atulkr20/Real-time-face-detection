import mediapipe as mp
import numpy as np

mp_face_detection = mp.solutions.face_detection

class FaceDetector:
    def __init__(self):
        self.detector = mp_face_detection.FaceDetection(
            model_selection=0,  # 0 = short range (within 2m), good for webcam
            min_detection_confidence=0.5
        )

    def detect(self, frame_rgb: np.ndarray):
        """
        Takes an RGB numpy array, returns ROI dict or None.
        ROI contains x, y, width, height (absolute pixels) and confidence.
        """
        h, w, _ = frame_rgb.shape
        results = self.detector.process(frame_rgb)

        if not results.detections:
            return None

        # We assume only one face per the spec
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        confidence = detection.score[0]

        # Convert relative coords to absolute pixels
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        width = int(bbox.width * w)
        height = int(bbox.height * h)

        # Clamp to frame boundaries
        x = max(0, x)
        y = max(0, y)
        width = min(width, w - x)
        height = min(height, h - y)

        return {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "confidence": round(confidence, 4)
        }