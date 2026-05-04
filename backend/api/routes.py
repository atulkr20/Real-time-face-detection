import io
import base64
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from PIL import Image

from db.database import get_db
from db.models import ROI
from services.face_detector import FaceDetector
from services.drawing import draw_bounding_box

router = APIRouter()
detector = FaceDetector()

frame_counter = {"count": 0}


@router.post("/feed")
async def receive_frame(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts a single video frame as an image upload.
    Detects face, stores ROI in DB, returns processed frame + ROI.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    frame_rgb = np.array(image)

    frame_counter["count"] += 1
    frame_number = frame_counter["count"]

    roi = detector.detect(frame_rgb)

    if roi:
        roi_record = ROI(
            frame_number=frame_number,
            x=roi["x"],
            y=roi["y"],
            width=roi["width"],
            height=roi["height"],
            confidence=roi["confidence"]
        )
        db.add(roi_record)
        db.commit()

        processed_frame = draw_bounding_box(frame_rgb, roi)
    else:
        processed_frame = frame_rgb

    output_image = Image.fromarray(processed_frame)
    buffer = io.BytesIO()
    output_image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return JSONResponse({
        "frame_number": frame_number,
        "roi": roi,
        "processed_frame": encoded
    })


@router.websocket("/stream")
async def stream_feed(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WebSocket endpoint. Client sends raw frame bytes, gets back
    processed frame (base64) + ROI data as JSON.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()

            image = Image.open(io.BytesIO(data)).convert("RGB")
            frame_rgb = np.array(image)

            frame_counter["count"] += 1
            frame_number = frame_counter["count"]

            roi = detector.detect(frame_rgb)

            if roi:
                roi_record = ROI(
                    frame_number=frame_number,
                    x=roi["x"],
                    y=roi["y"],
                    width=roi["width"],
                    height=roi["height"],
                    confidence=roi["confidence"]
                )
                db.add(roi_record)
                db.commit()

                processed_frame = draw_bounding_box(frame_rgb, roi)
            else:
                processed_frame = frame_rgb

            output_image = Image.fromarray(processed_frame)
            buffer = io.BytesIO()
            output_image.save(buffer, format="PNG")
            encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

            await websocket.send_json({
                "frame_number": frame_number,
                "roi": roi,
                "processed_frame": encoded
            })

    except WebSocketDisconnect:
        pass


@router.get("/roi")
def get_roi_data(limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns the last N ROI records from the database.
    """
    records = db.query(ROI).order_by(ROI.id.desc()).limit(limit).all()

    return JSONResponse({
        "count": len(records),
        "data": [
            {
                "id": r.id,
                "frame_number": r.frame_number,
                "x": r.x,
                "y": r.y,
                "width": r.width,
                "height": r.height,
                "confidence": r.confidence,
                "created_at": str(r.created_at)
            }
            for r in records
        ]
    })