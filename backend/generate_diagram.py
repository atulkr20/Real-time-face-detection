from PIL import Image, ImageDraw, ImageFont

# canvas
W, H = 1200, 700
img = Image.new("RGB", (W, H), "#0f0f0f")
draw = ImageDraw.Draw(img)

def box(x, y, w, h, fill, outline, text, subtext=""):
    draw.rectangle([x, y, x+w, y+h], fill=fill, outline=outline, width=2)
    draw.text((x + w//2, y + h//2 - 8), text, fill="white", anchor="mm")
    if subtext:
        draw.text((x + w//2, y + h//2 + 12), subtext, fill="#aaaaaa", anchor="mm")

def arrow(x1, y1, x2, y2):
    draw.line([x1, y1, x2, y2], fill="#00ff88", width=2)
    draw.polygon([x2, y2, x2-6, y2-10, x2+6, y2-10], fill="#00ff88")

# title
draw.text((W//2, 30), "Mega AI — Face Detection System Architecture", fill="#00ff88", anchor="mm")

# Docker Compose boundary
draw.rectangle([20, 60, W-20, H-20], outline="#333333", width=2)
draw.text((40, 70), "Docker Compose", fill="#555555")

# Browser/Client
box(30, 120, 160, 60, "#1a1a2e", "#4444ff", "Browser", "React Frontend")

# Frontend container
box(30, 260, 160, 60, "#16213e", "#4444ff", "Frontend", "Port 3000")

# Backend container
box(500, 200, 200, 60, "#1a2e1a", "#00ff88", "Backend", "FastAPI :8000")

# Endpoints
box(420, 320, 140, 50, "#0f1f0f", "#006600", "/feed", "POST")
box(580, 320, 140, 50, "#0f1f0f", "#006600", "/stream", "WebSocket")
box(740, 320, 140, 50, "#0f1f0f", "#006600", "/roi", "GET")

# Services
box(420, 430, 160, 50, "#1f1a0f", "#ff8800", "FaceDetector", "mediapipe")
box(620, 430, 160, 50, "#1f1a0f", "#ff8800", "DrawingService", "Pillow")

# PostgreSQL
box(820, 430, 160, 50, "#1a0f1a", "#aa44ff", "PostgreSQL", "ROI Data")

# arrows — browser to frontend
draw.line([110, 180, 110, 260], fill="#4444ff", width=2)
draw.text((120, 220), "HTTP/WS", fill="#4444ff")

# frontend to backend
draw.line([190, 290, 500, 230], fill="#00ff88", width=2)
draw.text((340, 250), "WebSocket / REST", fill="#00ff88")

# backend to endpoints
draw.line([550, 260, 490, 320], fill="#006600", width=2)
draw.line([600, 260, 650, 320], fill="#006600", width=2)
draw.line([650, 260, 810, 320], fill="#006600", width=2)

# endpoints to services
draw.line([490, 370, 500, 430], fill="#ff8800", width=2)
draw.line([650, 370, 700, 430], fill="#ff8800", width=2)

# services to db
draw.line([780, 455, 820, 455], fill="#aa44ff", width=2)

# legend
draw.rectangle([30, H-100, 400, H-30], fill="#111111", outline="#333333")
draw.text((40, H-90), "Legend:", fill="#ffffff")
draw.rectangle([40, H-70, 60, H-55], fill="#1a2e1a", outline="#00ff88")
draw.text((70, H-65), "Backend", fill="#aaaaaa")
draw.rectangle([140, H-70, 160, H-55], fill="#16213e", outline="#4444ff")
draw.text((170, H-65), "Frontend", fill="#aaaaaa")
draw.rectangle([240, H-70, 260, H-55], fill="#1a0f1a", outline="#aa44ff")
draw.text((270, H-65), "Database", fill="#aaaaaa")
draw.rectangle([340, H-70, 360, H-55], fill="#1f1a0f", outline="#ff8800")
draw.text((370, H-65), "Services", fill="#aaaaaa")

img.save("architecture.png")
print("architecture.png saved!")