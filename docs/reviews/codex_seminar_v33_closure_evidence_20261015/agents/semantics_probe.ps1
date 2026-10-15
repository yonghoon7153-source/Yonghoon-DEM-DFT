param([int[]]$Slides = @(3,5,7,11,13,15), [switch]$Compare, [switch]$Check)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$inputRoot = Join-Path $PSScriptRoot '../input'

function Read-ZipXml($archive, [string]$part) {
    $entry = $archive.GetEntry($part)
    if ($null -eq $entry) { throw "Missing part: $part" }
    $reader = [System.IO.StreamReader]::new($entry.Open())
    try { return [xml]$reader.ReadToEnd() } finally { $reader.Dispose() }
}
function Resolve-Part([string]$part, [string]$target) {
    $uri = [uri]::new([uri]('https://package.invalid/' + $part), $target)
    return $uri.AbsolutePath.TrimStart('/')
}
function Read-Paragraphs($node) {
    return @($node.SelectNodes('.//*[local-name()="p" and namespace-uri()="http://schemas.openxmlformats.org/drawingml/2006/main"]') | ForEach-Object {
        ($_.SelectNodes('.//*[local-name()="t"]') | ForEach-Object { $_.InnerText }) -join ''
    })
}
function Read-Deck([string]$path) {
    $archive = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path -LiteralPath $path))
    try {
        $presentation = Read-ZipXml $archive 'ppt/presentation.xml'
        $relationships = Read-ZipXml $archive 'ppt/_rels/presentation.xml.rels'
        $ordinal = 0
        foreach ($id in $presentation.SelectNodes('//*[local-name()="sldId"]')) {
            $ordinal++
            if ($ordinal -notin $Slides) { continue }
            $rid = $id.GetAttribute('id','http://schemas.openxmlformats.org/officeDocument/2006/relationships')
            $relationship = @($relationships.Relationships.Relationship | Where-Object { $_.Id -eq $rid })[0]
            $part = Resolve-Part 'ppt/presentation.xml' $relationship.Target
            $slide = Read-ZipXml $archive $part
            $body = Read-Paragraphs $slide
            $directory = $part.Substring(0,$part.LastIndexOf('/'))
            $basename = $part.Substring($part.LastIndexOf('/')+1)
            $rels = Read-ZipXml $archive ($directory + '/_rels/' + $basename + '.rels')
            $noteRelationship = @($rels.Relationships.Relationship | Where-Object { $_.Type -match '/notesSlide$' })
            $notesPart = if ($noteRelationship.Count) { Resolve-Part $part $noteRelationship[0].Target } else { $null }
            $notes = if ($notesPart) { Read-Paragraphs (Read-ZipXml $archive $notesPart) } else { @() }
            $shapes = @($slide.SelectNodes('//*[local-name()="spTree"]/*[local-name()="sp"]') | ForEach-Object {
                $shapeText = (Read-Paragraphs $_) -join "`n"
                $off = $_.SelectSingleNode('./*[local-name()="spPr"]/*[local-name()="xfrm"]/*[local-name()="off"]')
                if ($shapeText) { [pscustomobject]@{ text=$shapeText; x=$off.x; y=$off.y } }
            })
            [pscustomobject]@{ slide=$ordinal; part=$part; notesPart=$notesPart; body=$body; notes=$notes; shapes=$shapes }
        }
    } finally { $archive.Dispose() }
}
$current = @(Read-Deck (Join-Path $inputRoot 'deck/seminar_20261013_v33.pptx'))
if ($Check) {
    $previous = @(Read-Deck (Join-Path $inputRoot 'v32/seminar_20261013_v32.pptx'))
    function Current($number) { return @($current | Where-Object slide -eq $number)[0] }
    function Previous($number) { return @($previous | Where-Object slide -eq $number)[0] }
    function Same($left,$right) { return (($left -join "`n") -ceq ($right -join "`n")) }
    $checks = [ordered]@{}
    $s3 = Current 3; $p3 = Previous 3
    $checks['Q1_representative_source_line'] = (Same $s3.body @($p3.body | ForEach-Object {
        if ($_ -ceq 'This work — implemented equations of LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1]') {
            'This work — representative equations based on LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1].'
            'Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ.'
        } else { $_ }
    }))
    $checks['Q1_notes_lever_and_CDT_caveats'] = ($s3.notes -clike '*implemented lever arm has magnitude Rᵢ − δᵢⱼ/2*') -and ($s3.notes -clike '*CDT rolling torque is zero when the relative angular velocity is zero*')
    $s5 = Current 5; $p5 = Previous 5
    $checks['S5_body_unchanged'] = Same $s5.body $p5.body
    $checks['S5_only_notes_update'] = $s5.notes -ceq $p5.notes.Replace('listed by the author on 10-14 for this deck; the progress log of 10-14 evening still records it as a recommendation awaiting an answer','one large-particle LPSCl pellet added to the EIS plan, approved by the author on 10-14; docs/session_20260923_progress.md, 10-14 night 9 entry')
    $s7 = Current 7; $p7 = Previous 7
    $checks['S7_only_body_update'] = Same $s7.body @($p7.body | ForEach-Object { $_.Replace('pressed to 300 MPa;','pressed to 300 MPa (nominal stopping pressure; see Problem 4);') })
    $checks['S7_notes_unchanged'] = Same $s7.notes $p7.notes
    $s11 = Current 11; $p11 = Previous 11
    $old11 = 'At fixed platen the same bed relaxes to 165 MPa; a servo branch holding the target force (damping 1e-5) instead compacts it further (111.05 → 105.84 µm) — model-internal until the open checks pass.'
    $new11 = 'At fixed platen, the original run relaxes to 165 MPa. A combined follow-up protocol—plate-contact history reset, lower damping and force hold—reduces thickness from 111.05 to 105.84 µm. This remains a model-internal diagnostic; static-equilibrium and conservation checks are pending.'
    $checks['Q2_only_body_updates'] = Same @($s11.body | ForEach-Object { $_.Replace([char]0xA0,' ') }) @($p11.body | ForEach-Object { $_.Replace($old11,$new11).Replace('shaded = band registered before the run','shaded = registered prediction band') })
    $checks['Q2_table_history_row'] = 'Plate re-created at servo start: contact history reset' -cin $s11.body
    $checks['Q2_table_loss_row'] = 'Atom-count guard vs. conservation (13 SE particles lost)' -cin $s11.body
    $checks['Q2_three_open_statuses'] = @($s11.body | Where-Object { $_ -ceq 'open' }).Count -eq 3
    $checks['Q2_explicit_internal_not_experiment'] = $s11.notes.Contains('Passing these internal checks would qualify the numerical state of this bed; it would not validate the model against experiment.')
    $checks['Q2_existing_combined_and_loss_notes_retained'] = $s11.notes.Contains('(ii) The servo deck re-creates the plate and wall fixes, which also resets the normal plastic contact history, so B is a combined protocol (history reset + damping drop + force hold); the registered follow-up protocol includes a reset of the plate contact history (MV-02). (iii) The atom-count guard does not certify conservation; the 13 lost particles are SE (MV-08).')
    $checks['Q5_prediction_definition'] = $s11.notes.Contains('a model prediction registered before the run, not an experimental range or a statistical confidence interval.')
    $checks['Q5_hatching_still_open'] = (($s11.body -join ' ').Contains('hatched = checks still open'))
    $s13 = Current 13; $p13 = Previous 13
    $checks['Q4_body_unchanged'] = Same $s13.body $p13.body
    $checks['Q4_only_requested_note_replacement'] = $s13.notes -ceq $p13.notes.Replace('NCM: coating coverage followed the stress intensity rather than the number of stress events.','NCM. Coating coverage depended on stress intensity as well as stress number; increasing stress number alone did not collapse results across rotor speeds.')
    $s15 = Current 15; $p15 = Previous 15
    $checks['Q3_only_body_swap_and_future'] = Same $s15.body @($p15.body | ForEach-Object {
        if ($_ -ceq 'platen removal') { 'unloading' } elseif ($_ -ceq 'unloading') { 'platen removal' } else { $_.Replace('Heckel analysis redone','Heckel analysis to be redone') }
    })
    $flow = @($s15.shapes | Where-Object { $_.y -ceq '4937760' } | Sort-Object { [long]$_.x } | ForEach-Object text)
    $checks['Q3_spatial_left_to_right_flow'] = Same $flow @('insertion','stabilization','compression','servo','relaxation','unloading','platen removal')
    $checks['Q3_notes_order_and_future'] = $s15.notes.Contains('relaxation → unloading → platen removal (order ratified on 10-14:') -and $s15.notes.Contains('Heckel analysis to be redone,')
    $checks['S15_provisional_definition_and_distinct_target'] = $s15.notes.Contains('ε_union 10–13 %: Provisional geometric calibration target; experimental definition and load state still to be matched. It is a planned geometric target for the new protocol, not the existing 10 % calibration target on the MPM-inputs slide.')
    $checks['S15_no_runs_no_results_and_kit_hold_preserved'] = $s15.notes.Contains('plan only, no runs and no results') -and (($s15.body -join ' ').Contains('history test passed; kit re-review HOLD, fixes ratified'))
    $failed = @($checks.Keys | Where-Object { -not $checks[$_] })
    [pscustomobject]@{ checks=$checks; passed=$checks.Count-$failed.Count; total=$checks.Count; failed=$failed; flow=$flow } | ConvertTo-Json -Depth 10
    if ($failed.Count) { exit 1 }
} elseif ($Compare) {
    $previous = @(Read-Deck (Join-Path $inputRoot 'v32/seminar_20261013_v32.pptx'))
    foreach ($c in $current) {
        $p = @($previous | Where-Object slide -eq $c.slide)[0]
        [pscustomobject]@{
            slide=$c.slide
            oldBodyOnly=@($p.body | Where-Object { $_ -cnotin $c.body })
            newBodyOnly=@($c.body | Where-Object { $_ -cnotin $p.body })
            oldNotesOnly=@($p.notes | Where-Object { $_ -cnotin $c.notes })
            newNotesOnly=@($c.notes | Where-Object { $_ -cnotin $p.notes })
        } | ConvertTo-Json -Depth 10
    }
} else {
    $current | ConvertTo-Json -Depth 10
}
