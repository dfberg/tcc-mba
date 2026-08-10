param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$TemplatePath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

$inputJson = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $InputPath)) | ConvertFrom-Json
$template = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $TemplatePath))

$allowedEvidence = [ordered]@{
    '[ENDPOINT]' = [string]$inputJson.endpoint
    '[HTTP_METHOD]' = [string]$inputJson.httpMethod
    '[TEST_NAME]' = [string]$inputJson.testName
    '[GIT_DIFF]' = [string]$inputJson.gitDiff
    '[APPROVED_SNAPSHOT]' = [string]$inputJson.expectedSnapshot
    '[RECEIVED_SNAPSHOT]' = [string]$inputJson.receivedSnapshot
    '[TEST_OUTPUT]' = [string]$inputJson.testOutput
}

$templatePlaceholders = @([regex]::Matches($template, '\[[A-Z][A-Z_]+\]') | ForEach-Object { $_.Value } | Select-Object -Unique)
$unknownPlaceholders = @($templatePlaceholders | Where-Object { $_ -notin $allowedEvidence.Keys })
if ($unknownPlaceholders.Count -gt 0) {
    throw "Unknown template placeholder(s): $($unknownPlaceholders -join ', ')"
}

foreach ($entry in $allowedEvidence.GetEnumerator()) {
    if ([string]::IsNullOrEmpty($entry.Value)) {
        throw "Required evidence is empty for placeholder $($entry.Key)"
    }
    $template = $template.Replace($entry.Key, $entry.Value)
}

foreach ($placeholder in $allowedEvidence.Keys) {
    if ($template.Contains($placeholder)) {
        throw "The rendered prompt contains unresolved placeholder $placeholder"
    }
}

$outputDirectory = Split-Path -Parent $OutputPath
if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
    throw "Output directory does not exist: $outputDirectory"
}

[System.IO.File]::WriteAllText($OutputPath, $template, [System.Text.UTF8Encoding]::new($false))
