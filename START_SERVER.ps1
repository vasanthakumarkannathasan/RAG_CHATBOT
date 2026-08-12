# START RAG SERVER SCRIPT
# Copy and paste this into PowerShell terminal:

Write-Host "🚀 Starting Enterprise RAG Server..." -ForegroundColor Green
Write-Host ""

# Navigate to project directory
Set-Location "C:\Personal\AI_Roadmap\RAG\Projects\Enterprise-RAG"

# Start server using virtual environment Python
& "c:/Personal/AI_Roadmap/RAG/Projects/Enterprise-RAG/.venv/Scripts/python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

Write-Host ""
Write-Host "✅ Server started!" -ForegroundColor Green
Write-Host "📱 Web Interface: http://127.0.0.1:8000/static/index.html" -ForegroundColor Cyan
Write-Host "📖 API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
