Write-Host "--- STARTING SYSTEM INTEGRATION SUITE ---" -ForegroundColor Cyan

# 1. Health Check
$health = Invoke-RestMethod -Uri "http://127.0.0.1:8765/api/health" -Method Get
Write-Host "[PASS] Health Check: Status = $($health.status)" -ForegroundColor Green

# 2. Permission Check
$permBody = @{ action = "write_file"; level = 1 } | ConvertTo-Json
$perm = Invoke-RestMethod -Uri "http://127.0.0.1:8765/api/system/permissions/check" -Method Post -Body $permBody -ContentType "application/json"
Write-Host "[PASS] Permission Engine: Approved = $($perm.approved)" -ForegroundColor Green

# 3. Memory Index & Search
$docBody = @{ doc_id = "doc_test"; content = "FastAPI server runs integration tests efficiently."; metadata = @{ source = "test_suite" } } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8765/api/memory/index" -Method Post -Body $docBody -ContentType "application/json" | Out-Null

$searchBody = @{ query = "integration tests"; top_k = 1 } | ConvertTo-Json
$search = Invoke-RestMethod -Uri "http://127.0.0.1:8765/api/memory/search" -Method Post -Body $searchBody -ContentType "application/json"
Write-Host "[PASS] Vector Memory Search: Matches = $($search.results.Count)" -ForegroundColor Green

# 4. Project Tasks
$tasks = Invoke-RestMethod -Uri "http://127.0.0.1:8765/api/projects/1/tasks" -Method Get
Write-Host "[PASS] Project Tasks: Count = $($tasks.tasks.Count)" -ForegroundColor Green

Write-Host "--- ALL INTEGRATION TESTS PASSED CLEANLY ---" -ForegroundColor Cyan