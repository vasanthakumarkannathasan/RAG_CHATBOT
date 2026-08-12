# ADD AND INDEX DOCUMENTS - PowerShell Script
# This script helps you add PDF files and index them in one go

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  📚 ENTERPRISE RAG - ADD AND INDEX DOCUMENTS" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$dataFolder = "C:\Personal\AI_Roadmap\RAG\Projects\Enterprise-RAG\data"

# Show current PDFs
Write-Host "📂 Current PDFs in data folder:" -ForegroundColor Yellow
$currentPdfs = Get-ChildItem -Path $dataFolder -Filter "*.pdf" -ErrorAction SilentlyContinue
if ($currentPdfs) {
    foreach ($pdf in $currentPdfs) {
        Write-Host "   • $($pdf.Name)" -ForegroundColor White
    }
} else {
    Write-Host "   (No PDFs found)" -ForegroundColor Gray
}
Write-Host ""

# Ask if user wants to add new PDFs
Write-Host "📥 Do you want to add new PDF files? (y/n): " -ForegroundColor Green -NoNewline
$addFiles = Read-Host

if ($addFiles -eq 'y' -or $addFiles -eq 'yes') {
    Write-Host ""
    Write-Host "📁 Please select the folder containing your PDF files..." -ForegroundColor Yellow
    Write-Host ""
    
    # Open folder browser dialog
    Add-Type -AssemblyName System.Windows.Forms
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "Select folder containing PDF files"
    $folderBrowser.RootFolder = "MyComputer"
    
    if ($folderBrowser.ShowDialog() -eq "OK") {
        $sourceFolder = $folderBrowser.SelectedPath
        Write-Host "✅ Selected folder: $sourceFolder" -ForegroundColor Green
        Write-Host ""
        
        # Find PDFs in selected folder
        $pdfFiles = Get-ChildItem -Path $sourceFolder -Filter "*.pdf"
        
        if ($pdfFiles.Count -eq 0) {
            Write-Host "❌ No PDF files found in selected folder!" -ForegroundColor Red
            Write-Host ""
            exit
        }
        
        Write-Host "📄 Found $($pdfFiles.Count) PDF file(s):" -ForegroundColor Yellow
        foreach ($pdf in $pdfFiles) {
            Write-Host "   • $($pdf.Name)" -ForegroundColor White
        }
        Write-Host ""
        
        Write-Host "📋 Copy these files to data folder? (y/n): " -ForegroundColor Green -NoNewline
        $confirmCopy = Read-Host
        
        if ($confirmCopy -eq 'y' -or $confirmCopy -eq 'yes') {
            Write-Host ""
            Write-Host "📂 Copying files..." -ForegroundColor Yellow
            
            foreach ($pdf in $pdfFiles) {
                Copy-Item -Path $pdf.FullName -Destination $dataFolder -Force
                Write-Host "   ✓ Copied: $($pdf.Name)" -ForegroundColor Green
            }
            
            Write-Host ""
            Write-Host "✅ All files copied successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Copy cancelled." -ForegroundColor Red
            Write-Host ""
            exit
        }
    } else {
        Write-Host "❌ No folder selected. Exiting..." -ForegroundColor Red
        Write-Host ""
        exit
    }
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to index now
Write-Host "🔄 Do you want to index the documents now? (y/n): " -ForegroundColor Green -NoNewline
$indexNow = Read-Host

if ($indexNow -eq 'y' -or $indexNow -eq 'yes') {
    Write-Host ""
    Write-Host "🔄 Starting indexing process..." -ForegroundColor Yellow
    Write-Host ""
    
    # Run the indexing script
    $pythonExe = "c:/Personal/AI_Roadmap/RAG/Projects/Enterprise-RAG/.venv/Scripts/python.exe"
    & $pythonExe index_documents.py
    
} else {
    Write-Host ""
    Write-Host "💡 To index later, run:" -ForegroundColor Yellow
    Write-Host "   python index_documents.py" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  ✅ DONE!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Your documents are ready!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Start server: .\START_SERVER.ps1" -ForegroundColor Cyan
Write-Host "   2. Open web UI: http://127.0.0.1:8000/static/index.html" -ForegroundColor Cyan
Write-Host "   3. Ask questions about your documents!" -ForegroundColor Cyan
Write-Host ""
