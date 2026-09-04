"""Fail-closed, offline reconstruction of Benchmark V2 frozen Git evidence."""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).parent
PTAG="benchmark-v2-results-consolidation-protocol"
PCOMMIT="6a2c37446ca9de22b4538f62f0540408b47a708a"
PBLOB="5380a1bb25a1b6d00e4e1f4d484b22c74a7935ee"
PPATH="docs/benchmark/results_consolidation_protocol.md"
ATAG="benchmark-v2-results-consolidation-protocol-amendment-01"
ACOMMIT="5decff5a741f5c4dee045bdd935b567b8a9250d4"
ABLOB="2bc68ae055a24274ba8b559974d4f342fccd0059"
APATH="docs/benchmark/results_consolidation_protocol_amendment_01.md"
ATAG2="benchmark-v2-results-consolidation-protocol-amendment-02"
ACOMMIT2="a13727c16994edf7e0a83bf7e9b6c949181696cd"
ABLOB2="52e78ec2cd34af8c6ba435ccb57515c485abfaae"
APATH2="docs/benchmark/results_consolidation_protocol_amendment_02.md"
CTAG="benchmark-v2-gemini-config-v2"; CCOMMIT="98b568d21330fee1365c3247916011ab5ec0bcf4"
CPATH="docs/benchmark/configurations/CONFIG-GEMINI-02.json"
TPATH="docs/benchmark/prompts/snapshot-review-v1.md"
OSPATH="docs/benchmark/schemas/llm-output.schema.json"
OSBLOB="0b39bfa67288222d15732b3657a020206f4fc02e"
PARSER_PATH="scripts/snapshot_ai_review.py"
PARSER_BLOB="6a2a9d518825f4bb28c5f3cd03dfec9247d3f08d"
PAIR_PATHS=("docs/benchmark/evaluation_protocol.md","docs/benchmark/change_control.md")
EXPECTED_PRIMARY_SOURCE_FAMILIES=("protocol","amendment","amendment_02","catalog","baseline","configuration","canonicalization","retry_resume","provider_conditions","rerun","evaluation_freezes","ground_truth","prompt_template","raw_output_parsing_implementation","exp_case_mapping_technical_freezes")
OPTIONAL_SOURCE_FAMILIES=("contrastive_pairs",)
GLOBAL_PRIMARY_SOURCE_SPECS=(
    ("baseline","benchmark-v2-baseline","frozen benchmark baseline",["docs/benchmark/baseline/README.md"]),
    ("canonicalization","benchmark-v2-git-canonicalization-protocol","frozen Git canonicalization protocol",["docs/benchmark/evaluation_protocol.md"]),
    ("retry_resume","benchmark-v2-inference-resume-protocol","frozen inference retry/resume protocol",["docs/benchmark/evaluation_protocol.md"]),
    ("provider_conditions","benchmark-v2-provider-technical-conditions-protocol","frozen provider technical conditions",["docs/benchmark/evaluation_protocol.md"]),
    ("rerun","benchmark-v2-provider-limit-rerun-adapter-persistent-lock","frozen provider-limit rerun adapter",["docs/benchmark/evaluation_protocol.md"]),
)
MAPPING_SOURCE_TAGS=(
    "benchmark-v2-evaluation-protocol",
    "benchmark-v2-exp-002-005-validated",
    "benchmark-v2-exp-006-010-validated",
    "benchmark-v2-exp-011-015-validated",
    "benchmark-v2-exp-017-020-validated",
    "benchmark-v2-exp-021-025-validated",
    "benchmark-v2-exp-026-validated",
    "benchmark-v2-exp-027-030-validated",
)
class ConsolidationIntegrityError(RuntimeError): pass
class ContrastivePairProvenanceError(RuntimeError):
    def __init__(self,code,path,detail):
        self.code=code;self.path=path;self.detail=detail
        super().__init__(f"{code}: {path}: {detail}")
def result(passed,evidence=None,failures=None):
    return {"passed":bool(passed),"evidence":evidence or {},"failures":failures or []}
def run(*a):
    try:return subprocess.run(["git",*a],cwd=ROOT,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
    except subprocess.CalledProcessError as e:raise ConsolidationIntegrityError(e.stderr.decode("utf-8","replace")) from e
def txt(*a):
    try:return run(*a).decode("utf-8-sig")
    except UnicodeDecodeError as e:raise ConsolidationIntegrityError(f"non-UTF8 Git blob: {a}") from e
def typ(ref):return txt("cat-file","-t",ref).strip()
def commit(tag):return txt("rev-parse",f"{tag}^{{}}").strip()
def blob(c,path):return run("show",f"{c}:{path}")
def sha(c,path):return txt("rev-parse",f"{c}:{path}").strip()
def j(c,path):
    try:return json.loads(blob(c,path).decode("utf-8-sig"))
    except (UnicodeDecodeError,json.JSONDecodeError) as e:raise ConsolidationIntegrityError(f"invalid JSON {c}:{path}: {e}") from e
def tag_ref_exists(tag):
    return subprocess.run(["git","show-ref","--verify","--quiet",f"refs/tags/{tag}"],cwd=ROOT).returncode==0
def src(tag,purpose):
    t=typ(tag)
    if t not in ("tag","commit"):raise ConsolidationIntegrityError(f"bad source type {tag}: {t}")
    is_tag=tag_ref_exists(tag)
    tag_type="annotated" if t=="tag" else "lightweight" if is_tag and t=="commit" else "commit"
    return {"tag":tag,"tagType":tag_type,"tagObjectSha":txt("rev-parse",tag).strip() if tag_type=="annotated" else None,"dereferencedCommit":commit(tag),"purpose":purpose,"selectedExperiments":[]}
def validate_source(tag,purpose,required_paths):
    s=src(tag,purpose); failures=[]
    for path in required_paths:
        try: read_blob=blob(s["dereferencedCommit"],path)
        except ConsolidationIntegrityError as e: failures.append(str(e)); continue
        if not read_blob: failures.append(f"empty required blob {path}")
    s.update({"ref":tag,"requiredPaths":required_paths,"validationStatus":"PASS" if not failures else "FAIL","validationEvidence":{"commit":s["dereferencedCommit"],"paths":required_paths},"validationFailures":failures})
    if failures: raise ConsolidationIntegrityError(f"frozen source validation failed {tag}: {failures}")
    return s
def register_source(registry,family,tag,purpose,required_paths,required=True):
    """The sole registry writer: every primary entry has a real PASS/FAIL result."""
    entry=validate_source(tag,purpose,required_paths)
    entry.update({"family":family,"requiredForPrimaryResults":required})
    registry.setdefault(family,[]).append(entry)
    return entry
def register_optional_source(registry,family,tag,purpose,required_paths):
    """Register optional frozen evidence without converting programming errors into availability failures."""
    try:s=src(tag,purpose)
    except ConsolidationIntegrityError as e:
        s={"tag":tag,"tagType":None,"tagObjectSha":None,"dereferencedCommit":None,"purpose":purpose,"selectedExperiments":[]}
        failures=[str(e)]
    else:
        failures=[]
        for path in required_paths:
            try:read_blob=blob(s["dereferencedCommit"],path)
            except ConsolidationIntegrityError as e:failures.append(str(e));continue
            if not read_blob:failures.append(f"empty optional blob {path}")
    s.update({"ref":tag,"family":family,"requiredPaths":required_paths,"requiredForPrimaryResults":False,"validationStatus":"PASS" if not failures else "FAIL","validationEvidence":{"commit":s["dereferencedCommit"],"paths":required_paths},"validationFailures":failures})
    registry.setdefault(family,[]).append(s)
    return s
def primary_registry_gate(registry):
    actual=set(registry); expected=set(EXPECTED_PRIMARY_SOURCE_FAMILIES); optional=set(OPTIONAL_SOURCE_FAMILIES)
    required=[source for entries in registry.values() for source in entries if source["requiredForPrimaryResults"]]
    coverage={"expectedFamilies":sorted(expected),"optionalFamilies":sorted(optional),"actualFamilies":sorted(actual),"missingFamilies":sorted(expected-actual),"unexpectedFamilies":sorted(actual-expected-optional)}
    valid=bool(required) and not coverage["missingFamilies"] and all(source.get("validationStatus") in ("PASS","FAIL") for source in required) and all(source["validationStatus"]=="PASS" for source in required)
    return valid,coverage,required
def authority(tag,expected_commit,expected_blob,path,purpose):
    """Validate an immutable methodological authority, including its exact blob."""
    source=validate_source(tag,purpose,[path])
    if source["dereferencedCommit"]!=expected_commit or sha(expected_commit,path)!=expected_blob:
        raise ConsolidationIntegrityError(f"authority identity failure: {tag}")
    source["expectedCommit"]=expected_commit; source["expectedBlobSha"]=expected_blob
    source["blobSha"]=expected_blob
    return source
def descriptive_attributes(catalog_source,case_id):
    """Return attributes only when one frozen, complete structured record proves them."""
    commit_id=catalog_source["dereferencedCommit"]
    for path in txt("ls-tree","-r","--name-only",commit_id).splitlines():
        if not path.endswith(".json"): continue
        try: value=j(commit_id,path)
        except ConsolidationIntegrityError: continue
        if value.get("caseId")==case_id:
            required=("difficulty","category","targetFamily")
            if all(k in value and value[k] is not None for k in required):
                return {k:value[k] for k in required},{"tag":catalog_source["tag"],"commit":commit_id,"path":path,"blobSha":sha(commit_id,path),"passed":True}
    return {"difficulty":None,"category":None,"targetFamily":None},{"tag":catalog_source["tag"],"commit":commit_id,"passed":False,"reason":"no complete frozen deterministic descriptive record"}
SCHEMA_META_KEYWORDS={"$schema","$id","title"}
SCHEMA_VALIDATION_KEYWORDS={"type","additionalProperties","required","properties","minimum","maximum","minLength"}
def validate_schema_subset(instance,schema,location="$"):
    """Validate exactly the frozen schema subset; unknown keywords fail closed."""
    unknown=set(schema)-SCHEMA_META_KEYWORDS-SCHEMA_VALIDATION_KEYWORDS
    if unknown: raise ConsolidationIntegrityError(f"unsupported schema keywords at {location}: {sorted(unknown)}")
    expected=schema.get("type")
    checks={"object":lambda v:isinstance(v,dict),"boolean":lambda v:isinstance(v,bool),"integer":lambda v:isinstance(v,int) and not isinstance(v,bool),"string":lambda v:isinstance(v,str)}
    if expected not in checks or not checks[expected](instance): raise ConsolidationIntegrityError(f"schema type failure at {location}: {expected}")
    if isinstance(instance,dict):
        properties=schema.get("properties",{}); missing=[key for key in schema.get("required",[]) if key not in instance]
        if missing: raise ConsolidationIntegrityError(f"missing required fields at {location}: {missing}")
        if schema.get("additionalProperties") is False:
            extras=sorted(set(instance)-set(properties))
            if extras: raise ConsolidationIntegrityError(f"additional fields at {location}: {extras}")
        for key,value in instance.items():
            if key in properties: validate_schema_subset(value,properties[key],f"{location}.{key}")
    if isinstance(instance,str) and "minLength" in schema and len(instance)<schema["minLength"]: raise ConsolidationIntegrityError(f"minLength failure at {location}")
    if isinstance(instance,int) and not isinstance(instance,bool):
        if "minimum" in schema and instance<schema["minimum"]: raise ConsolidationIntegrityError(f"minimum failure at {location}")
        if "maximum" in schema and instance>schema["maximum"]: raise ConsolidationIntegrityError(f"maximum failure at {location}")
def normative_config():
    source=validate_source(CTAG,"pre-evaluation normative configuration",[CPATH,TPATH,OSPATH])
    if source["dereferencedCommit"]!=CCOMMIT: raise ConsolidationIntegrityError("normative config commit mismatch")
    config=j(CCOMMIT,CPATH)
    required=("configurationId","provider","modelRequested","promptTemplate","promptTemplateSha256","structuredOutput","http","retryPolicy")
    if not all(k in config for k in required): raise ConsolidationIntegrityError("incomplete normative config")
    if config["structuredOutput"].get("responseSchema")!=OSPATH or sha(CCOMMIT,OSPATH)!=OSBLOB: raise ConsolidationIntegrityError("normative output schema identity/link failure")
    output_schema=j(CCOMMIT,OSPATH)
    template=blob(CCOMMIT,TPATH); observed=hashlib.sha256(template).hexdigest().upper(); expected=str(config["promptTemplateSha256"]).upper()
    if observed!=expected: raise ConsolidationIntegrityError("config-to-template SHA mismatch")
    return source,config,{"configurationId":config["configurationId"],"provider":config["provider"],"modelRequested":config["modelRequested"],"templateId":config["promptTemplate"],"templateShaExpected":expected,"templateShaObserved":observed,"templatePath":TPATH,"templateBlobSha":sha(CCOMMIT,TPATH),"outputSchema":output_schema,"outputSchemaPath":OSPATH,"outputSchemaBlobSha":OSBLOB,"timeout":config["http"],"retryPolicy":config["retryPolicy"],"passed":True}
def parse_pairs(c,path):
    """Parse only an explicit contrastive-pair section; a pair member may occur once."""
    try:document=txt("show",f"{c}:{path}")
    except ConsolidationIntegrityError as e:raise ContrastivePairProvenanceError("FROZEN_SOURCE_UNAVAILABLE",path,str(e)) from e
    marker=re.search(r"(?im)^#{1,6}\s+.*(?:contrastive|contrasti).*(?:pair|par).*$",document)
    if not marker: raise ContrastivePairProvenanceError("PAIR_SECTION_ABSENT",path,"contrastive pair section not found")
    section=document[marker.end():]
    next_heading=re.search(r"(?m)^#{1,6}\s+",section)
    if next_heading: section=section[:next_heading.start()]
    found=re.findall(r"CASE-(\d{3})\s*/\s*CASE-(\d{3})",section,re.I)
    if not found: raise ContrastivePairProvenanceError("PAIR_DECLARATIONS_UNPARSEABLE",path,"no complete pair declaration found")
    pairs=set(); members=set()
    for left,right in found:
        if left==right or not (1<=int(left)<=30 and 1<=int(right)<=30): raise ContrastivePairProvenanceError("INVALID_CASE_REFERENCE",path,f"CASE-{left} / CASE-{right}")
        pair=tuple(sorted((f"CASE-{left}",f"CASE-{right}")))
        if pair in pairs or any(member in members for member in pair): raise ContrastivePairProvenanceError("DUPLICATE_OR_REUSED_PAIR_MEMBER",path," / ".join(pair))
        pairs.add(pair); members.update(pair)
    return pairs
def ratio(n,d,label):
    return {"raw":None,"numerator":n,"denominator":d,"displayPercent":None,"notApplicableReason":label} if not d else {"raw":n/d,"numerator":n,"denominator":d,"displayPercent":round(100*n/d,2),"notApplicableReason":None}
def f1(p,r,n,d,label):
    direct=ratio(2*p["raw"]*r["raw"],p["raw"]+r["raw"],label) if p["raw"] is not None and r["raw"] is not None else ratio(0,0,label)
    alt=ratio(n,d,label)
    if direct["raw"] is not None and abs(direct["raw"]-alt["raw"])>1e-12:raise ConsolidationIntegrityError(f"{label} formula mismatch")
    return alt
def etag(n):
    if n==1:return "benchmark-v2-exp-001-evaluated"
    if n<=5:return "benchmark-v2-exp-002-005-evaluated"
    if n<=10:return "benchmark-v2-exp-006-010-evaluated"
    if n<=15:return "benchmark-v2-exp-012-015-evaluated"
    if n in (17,19,20):return "benchmark-v2-exp-017-019-020-rerun-evaluated"
    if n==18:return "benchmark-v2-exp-017-020-inference"
    if n in (21,23,24,25):return "benchmark-v2-exp-021-023-025-evaluated"
    if n==22:return "benchmark-v2-exp-022-evaluated"
    if n>=26:return "benchmark-v2-exp-026-030-evaluated"
    raise ConsolidationIntegrityError(f"no frozen mapping for EXP-{n:03d}")
def exclusion(exp):
    # A frozen JSON status record is mandatory; no manual EXP-011/016 fallback.
    for tag in txt("for-each-ref","--format=%(refname:short)","refs/tags").splitlines():
        c=commit(tag)
        for path in txt("ls-tree","-r","--name-only",c).splitlines():
            if exp in path and path.endswith(".json"):
                try:x=j(c,path)
                except ConsolidationIntegrityError:continue
                if x.get("experimentId")==exp and x.get("finalNormativeStatus")=="REQUIRES_REVIEW":return validate_source(tag,"normative exclusion",[path]),x,path
    raise ConsolidationIntegrityError(f"missing frozen normative exclusion for {exp}")
def build_case_mapping_index(registry):
    """Index explicit EXP-to-CASE metadata introduced by pre-inference technical freezes."""
    index={}
    pattern=re.compile(r"docs/benchmark/experiments/(EXP-\d{3})/metadata\.json")
    for tag in MAPPING_SOURCE_TAGS:
        source_commit=commit(tag)
        paths=sorted(path for path in txt("diff-tree","--no-commit-id","--name-only","-r",source_commit).splitlines() if pattern.fullmatch(path))
        if not paths: raise ConsolidationIntegrityError(f"technical mapping freeze has no introduced metadata: {tag}")
        source=register_source(registry,"exp_case_mapping_technical_freezes",tag,"pre-inference technical EXP-to-CASE mapping",paths)
        source.update({"chronology":"BEFORE_LLM_INFERENCE","sourceType":"TECHNICAL_FREEZE"})
        chronology_checks=[]
        for path in paths:
            metadata=j(source_commit,path);path_exp=pattern.fullmatch(path).group(1)
            exp_id=metadata.get("experimentId");case_id=metadata.get("caseId")
            if exp_id!=path_exp: raise ConsolidationIntegrityError(f"mapping experimentId/path conflict {tag}:{path}")
            if not isinstance(case_id,str) or not re.fullmatch(r"CASE-\d{3}",case_id): raise ConsolidationIntegrityError(f"missing explicit caseId {tag}:{path}")
            if metadata.get("state")!="VALIDATED" or metadata.get("reproducible") is not True: raise ConsolidationIntegrityError(f"mapping metadata is not technically validated {tag}:{path}")
            evaluation_tag=etag(int(exp_id.removeprefix("EXP-")));evaluation_commit=commit(evaluation_tag)
            chronology=subprocess.run(["git","merge-base","--is-ancestor",source_commit,evaluation_commit],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if source_commit==evaluation_commit or chronology.returncode!=0: raise ConsolidationIntegrityError(f"mapping source is not before LLM inference {tag}:{path}")
            evidence={"experimentId":exp_id,"caseId":case_id,"sourceTag":tag,"tagType":source["tagType"],"tagObjectSha":source["tagObjectSha"],"dereferencedCommit":source_commit,"path":path,"blobSha":sha(source_commit,path),"blobSha256":hashlib.sha256(blob(source_commit,path)).hexdigest().upper(),"chronology":"BEFORE_LLM_INFERENCE","chronologyAgainstTag":evaluation_tag,"chronologyAgainstCommit":evaluation_commit,"chronologyValidationStatus":"PASS","validationStatus":"PASS"}
            index.setdefault(exp_id,[]).append(evidence);chronology_checks.append({"experimentId":exp_id,"evaluationTag":evaluation_tag,"status":"PASS"})
        source["selectedExperiments"]=sorted(item["experimentId"] for item in chronology_checks)
        source["validationEvidence"]["chronologyChecks"]=chronology_checks
    for exp_id,candidates in index.items():
        if len({candidate["caseId"] for candidate in candidates})!=1: raise ConsolidationIntegrityError(f"conflicting frozen CASE mappings for {exp_id}")
    return index
def resolve_case_mapping(index,exp_id):
    candidates=index.get(exp_id,[])
    if not candidates:return None,{"passed":False,"status":"NOT_AVAILABLE_FROM_FROZEN_EVIDENCE","experimentId":exp_id,"caseId":None,"conflictStatus":"NONE","sources":[]}
    case_ids={candidate["caseId"] for candidate in candidates}
    if len(case_ids)!=1: raise ConsolidationIntegrityError(f"conflicting frozen CASE mappings for {exp_id}")
    evidence=dict(candidates[0]);evidence.update({"passed":True,"status":"PASS","conflictStatus":"NONE","corroboratingSources":candidates[1:]})
    return evidence["caseId"],evidence
def select_first_valid_attempt(c,root,config):
    """Derive the selected attempt from frozen attempt status evidence."""
    selection_rule=config["retryPolicy"].get("selectionRule")
    if selection_rule!="FIRST_VALID_RESPONSE": raise ConsolidationIntegrityError(f"unsupported attempt selection rule {root}: {selection_rule}")
    paths=[p for p in txt("ls-tree","-r","--name-only",c,f"{root}/attempts").splitlines() if p.endswith("/attempt.json")]
    history=[];seen=set()
    for path in paths:
        attempt=j(c,path);number=attempt.get("attempt")
        if isinstance(number,bool) or not isinstance(number,int) or number<1 or number in seen: raise ConsolidationIntegrityError(f"invalid attempt history {root}")
        if path!=f"{root}/attempts/attempt-{number:02d}/attempt.json": raise ConsolidationIntegrityError(f"attempt path/number mismatch {path}")
        seen.add(number);history.append((number,attempt,path))
    history.sort(key=lambda item:item[0])
    valid=[item for item in history if item[1].get("status")=="VALID_RESPONSE"]
    if not valid: raise ConsolidationIntegrityError(f"no frozen valid attempt {root}")
    number,attempt,path=valid[0]
    evidence=result(True,{"attemptHistory":[{"attempt":n,"status":record.get("status"),"path":p} for n,record,p in history],"selectedAttempt":number,"selectedAttemptPath":path,"validAttempts":[n for n,_,_ in valid],"selectionRuleExpected":selection_rule,"evidenceSource":{"commit":c,"root":root}})
    return number,attempt,evidence
def validate(c,root,config,config_source,template_evidence):
    no,att,first=select_first_valid_attempt(c,root,config)
    attempt_path=f"{root}/attempts/attempt-{no:02d}/attempt.json"; raw_path=f"{root}/attempts/attempt-{no:02d}/response.raw.json"; output_path=f"{root}/llm-output.json"
    prompt_path=root.split("/evaluation/")[0]+"/rendered-prompt.txt"; prompt=blob(c,prompt_path)
    prompt_observed=hashlib.sha256(prompt).hexdigest().upper()
    if att.get("status")!="VALID_RESPONSE" or prompt_observed!=att.get("renderedPromptSha256"): raise ConsolidationIntegrityError(f"invalid selected attempt/prompt {root}")
    raw=blob(c,raw_path); raw_observed=hashlib.sha256(raw).hexdigest().upper(); raw_expected=att.get("rawResponseSha256")
    if raw_observed!=raw_expected: raise ConsolidationIntegrityError(f"raw response hash failure {root}")
    try: envelope=json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError,json.JSONDecodeError) as e: raise ConsolidationIntegrityError(f"invalid frozen provider envelope {root}: {e}") from e
    candidates=envelope.get("candidates") or []
    if not isinstance(candidates,list) or not candidates: raise ConsolidationIntegrityError(f"missing Gemini candidate {root}")
    parts=candidates[0].get("content",{}).get("parts",[])
    if not isinstance(parts,list) or not all(isinstance(part,dict) for part in parts): raise ConsolidationIntegrityError(f"invalid Gemini parts {root}")
    model_text="".join(part.get("text","") for part in parts).strip()
    if not model_text: raise ConsolidationIntegrityError(f"empty Gemini model output {root}")
    model_bytes=model_text.encode("utf-8"); model_observed=hashlib.sha256(model_bytes).hexdigest().upper(); model_expected=att.get("modelOutputSha256")
    if model_observed!=model_expected: raise ConsolidationIntegrityError(f"model output hash failure {root}")
    output_bytes=blob(c,output_path)
    if output_bytes!=model_bytes or hashlib.sha256(output_bytes).hexdigest().upper()!=model_expected: raise ConsolidationIntegrityError(f"llm-output byte linkage failure {root}")
    try: out=json.loads(model_text)
    except json.JSONDecodeError as e: raise ConsolidationIntegrityError(f"invalid structured model output {root}: {e}") from e
    validate_schema_subset(out,template_evidence["outputSchema"])
    model_check=result(att.get("configurationId")==config["configurationId"] and att.get("modelRequested")==config["modelRequested"],{"observedConfig":att.get("configurationId"),"expectedConfig":config["configurationId"],"observedModel":att.get("modelRequested"),"expectedModel":config["modelRequested"],"sourceTag":config_source["tag"],"sourceCommit":config_source["dereferencedCommit"],"sourcePath":CPATH})
    prompt_check=result(prompt_observed==att.get("renderedPromptSha256") and template_evidence["passed"],{"configurationId":config["configurationId"],"templateId":config["promptTemplate"],"templateShaExpected":template_evidence["templateShaExpected"],"templateShaObserved":template_evidence["templateShaObserved"],"renderedPromptPath":prompt_path,"renderedPromptShaExpected":att.get("renderedPromptSha256"),"renderedPromptShaObserved":prompt_observed,"selectedAttemptPath":f"{root}/attempts/attempt-{no:02d}/attempt.json","sourceTag":config_source["tag"],"sourceCommit":config_source["dereferencedCommit"],"passed":prompt_observed==att.get("renderedPromptSha256") and template_evidence["passed"]})
    llm_provenance=result(True,{"selectedAttempt":no,"namespace":root,"rawResponse":{"path":raw_path,"expectedSha256":raw_expected,"observedSha256":raw_observed,"validationStatus":"PASS"},"parsingRule":{"sourceTag":CTAG,"sourceCommit":CCOMMIT,"sourcePath":PARSER_PATH,"sourceBlobSha":PARSER_BLOB,"chronology":"PRE_EVALUATION"},"modelOutput":{"expectedSha256":model_expected,"observedSha256":model_observed,"validationStatus":"PASS"},"llmOutput":{"path":output_path,"blobSha":sha(c,output_path),"byteEqualityStatus":"PASS"},"schema":{"sourceTag":CTAG,"sourceCommit":CCOMMIT,"sourcePath":OSPATH,"sourceBlobSha":OSBLOB,"validationStatus":"PASS"},"overallStatus":"PASS"})
    evidence={"llmOutputBlobSha":sha(c,output_path),"rawBlobSha":sha(c,raw_path),"renderedPromptBlobSha":sha(c,prompt_path),"firstValid":first,"modelConfig":model_check,"prompt":prompt_check,"llmOutputProvenance":llm_provenance}
    return out,att,evidence
def write_atomic(a,b):
    tmp=[(OUT/"benchmark_v2_results.json.tmp",OUT/"benchmark_v2_results.json",a),(OUT/"benchmark_v2_results.md.tmp",OUT/"benchmark_v2_results.md",b)]
    try:
        for p,_,s in tmp:
            with p.open("w",encoding="utf-8") as f:f.write(s);f.flush();os.fsync(f.fileno())
        for p,q,_ in tmp:os.replace(p,q)
    finally:
        for p,_,_ in tmp:
            if p.exists():p.unlink()
def main(validate_only):
    # Each amendment has precedence only within its declared provenance scope.
    source_registry={}
    proto=authority(PTAG,PCOMMIT,PBLOB,PPATH,"original protocol"); proto.update({"family":"protocol","requiredForPrimaryResults":True}); source_registry["protocol"]=[proto]
    amendment=authority(ATAG,ACOMMIT,ABLOB,APATH,"amendment 01: provenance scope correction"); amendment.update({"family":"amendment","requiredForPrimaryResults":True}); source_registry["amendment"]=[amendment]
    amendment02=authority(ATAG2,ACOMMIT2,ABLOB2,APATH2,"amendment 02: EXP-to-CASE mapping provenance scope correction"); amendment02.update({"family":"amendment_02","requiredForPrimaryResults":True}); source_registry["amendment_02"]=[amendment02]
    config_source,config,template_evidence=normative_config()
    config_source.update({"family":"configuration","requiredForPrimaryResults":True}); source_registry["configuration"]=[config_source]
    source_registry["prompt_template"]=[{**config_source,"family":"prompt_template","purpose":"normative frozen prompt template","requiredPaths":[TPATH]}]
    parser_source=register_source(source_registry,"raw_output_parsing_implementation",CTAG,"raw_response_to_structured_output",[PARSER_PATH])
    if parser_source["dereferencedCommit"]!=CCOMMIT or sha(CCOMMIT,PARSER_PATH)!=PARSER_BLOB: raise ConsolidationIntegrityError("frozen raw-output parser identity failure")
    parser_source.update({"blobSha":PARSER_BLOB,"chronology":"PRE_EVALUATION","sourceType":"EXECUTABLE_IMPLEMENTATION"})
    for family,tag,purpose,paths in GLOBAL_PRIMARY_SOURCE_SPECS: register_source(source_registry,family,tag,purpose,paths)
    case_mapping_index=build_case_mapping_index(source_registry)
    pair_source=register_optional_source(source_registry,"contrastive_pairs",CTAG,"optional predeclared contrastive-pair sources",list(PAIR_PATHS))
    if pair_source["validationStatus"]!="PASS":
        pair_set=set();pair_provenance=result(False,{"availability":"NOT_AVAILABLE","source":pair_source,"reason":{"code":"FROZEN_SOURCE_VALIDATION_FAILED","detail":pair_source["validationFailures"]}},pair_source["validationFailures"])
    else:
        try:pair_sets=[parse_pairs(CCOMMIT,path) for path in PAIR_PATHS]
        except ContrastivePairProvenanceError as e:
            pair_set=set();pair_provenance=result(False,{"availability":"NOT_AVAILABLE","source":pair_source,"reason":{"code":e.code,"path":e.path,"detail":e.detail}},[str(e)])
        else:
            if pair_sets[0]!=pair_sets[1]:
                pair_set=set();pair_provenance=result(False,{"availability":"NOT_AVAILABLE","source":pair_source,"paths":list(PAIR_PATHS),"commit":CCOMMIT,"sets":[sorted(x) for x in pair_sets],"reason":{"code":"PAIR_SOURCE_CONFLICT","detail":"frozen pair declarations disagree"}},["frozen pair declarations disagree"])
            else:
                pair_set=pair_sets[0];pair_provenance=result(True,{"availability":"AVAILABLE","source":pair_source,"paths":list(PAIR_PATHS),"commit":CCOMMIT,"sets":[sorted(x) for x in pair_sets],"reason":None})
    catalog=register_source(source_registry,"catalog","benchmark-v2-catalog","catalog",[],True)
    sources=source_registry; rows=[]
    for n in range(1,31):
        exp=f"EXP-{n:03d}"
        if n in (11,16):
            s,status,path=exclusion(exp);s.update({"family":"evaluation_freezes","requiredForPrimaryResults":True});source_registry.setdefault("evaluation_freezes",[]).append(s)
            case_id,case_mapping=resolve_case_mapping(case_mapping_index,exp)
            status.update({"experimentId":exp,"caseId":case_id,"caseMappingStatus":case_mapping["status"],"includedInPrimaryAnalysis":False,"matchStatus":"NOT_APPLICABLE","authoritativeEvaluationTag":s["tag"],"authoritativeEvaluationCommit":s["dereferencedCommit"],"provenance":{"normativeStatusPath":path,"caseMappingProvenance":case_mapping}});rows.append(status);continue
        tag=etag(n);base=f"docs/benchmark/experiments/{exp}";s=register_source(source_registry,"evaluation_freezes",tag,"normative evaluation",[f"{base}/metadata.json"]);c=s["dereferencedCommit"];case_id,case_mapping=resolve_case_mapping(case_mapping_index,exp)
        case,catalog_evidence=descriptive_attributes(catalog,case_id) if case_id is not None else ({"difficulty":None,"category":None,"targetFamily":None},{"tag":catalog["tag"],"commit":catalog["dereferencedCommit"],"passed":False,"reason":"CASE unavailable from frozen mapping evidence"})
        gs=register_source(source_registry,"ground_truth","benchmark-v2-exp-002-005-ground-truth-recovered" if 2<=n<=5 else tag,"ground truth recovery" if 2<=n<=5 else "ground truth in evaluation freeze",[f"{base}/ground-truth.json"]);gt=j(gs["dereferencedCommit"],f"{base}/ground-truth.json")
        if gt.get("classification") not in ("SHOULD_UPDATE","SHOULD_NOT_UPDATE"):raise ConsolidationIntegrityError(f"bad frozen GT {exp}")
        ns="rerun-01" if n in (17,19,20) else "primary";root=f"{base}/evaluation/{config['configurationId']}"+(f"/reruns/{ns}" if ns!="primary" else "")
        out,att,evidence=validate(c,root,config,config_source,template_evidence);pred="SHOULD_UPDATE" if out["shouldUpdateSnapshot"] else "SHOULD_NOT_UPDATE"
        rows.append({"experimentId":exp,"caseId":case_id,"caseMappingStatus":case_mapping["status"],"finalNormativeStatus":"VALID_EVALUATION","includedInPrimaryAnalysis":True,"exclusionReason":None,"authoritativeEvaluation":{"tag":tag,"commit":c,"path":root},"authoritativeGroundTruth":{"tag":gs["tag"],"commit":gs["dereferencedCommit"],"path":f"{base}/ground-truth.json"},"executionNamespace":ns,"groundTruth":gt["classification"],"llmClassification":pred,"matchStatus":"MATCH" if pred==gt["classification"] else "MISMATCH","confidence":out.get("confidence"),"difficulty":case["difficulty"],"category":case["category"],"targetFamily":case["targetFamily"],"provenance":{"caseMappingProvenance":case_mapping,"catalog":catalog_evidence,"groundTruth":{"tag":gs["tag"],"commit":gs["dereferencedCommit"],"path":f"{base}/ground-truth.json"},"evaluation":{"tag":tag,"commit":c,"path":root},"llmOutput":evidence["llmOutputProvenance"],"modelConfig":evidence["modelConfig"],"prompt":evidence["prompt"],"attemptChain":evidence["firstValid"]}})
    inc=[x for x in rows if x["includedInPrimaryAnalysis"]]
    known_case_ids=[x["caseId"] for x in rows if x.get("caseId") is not None]
    if len(rows)!=30 or len(inc)!=28 or len({x["experimentId"] for x in rows})!=30 or len(known_case_ids)!=len(set(known_case_ids)):raise ConsolidationIntegrityError("dataset integrity failure")
    def case_mapping_passed(row):
        evidence=row.get("provenance",{}).get("caseMappingProvenance",{})
        return evidence.get("passed") is True and evidence.get("status")=="PASS" and evidence.get("caseId")==row.get("caseId") and evidence.get("chronology") in ("BEFORE_LLM_INFERENCE","DURING_TECHNICAL_EXECUTION_BEFORE_LLM") and evidence.get("chronologyValidationStatus")=="PASS" and evidence.get("validationStatus")=="PASS" and evidence.get("conflictStatus")=="NONE"
    included_mapping_failures=[x["experimentId"] for x in inc if not case_mapping_passed(x)]
    primary_mapping_gate=bool(inc) and not included_mapping_failures
    full_catalog_mapping_gate=bool(rows) and all(case_mapping_passed(x) for x in rows)
    def cell(g,p):return [x["experimentId"] for x in inc if x["groundTruth"]==g and x["llmClassification"]==p]
    tp,fp,fn,tn=cell("SHOULD_UPDATE","SHOULD_UPDATE"),cell("SHOULD_NOT_UPDATE","SHOULD_UPDATE"),cell("SHOULD_UPDATE","SHOULD_NOT_UPDATE"),cell("SHOULD_NOT_UPDATE","SHOULD_NOT_UPDATE")
    pu,ru,pn,rn=ratio(len(tp),len(tp)+len(fp),"precision update"),ratio(len(tp),len(tp)+len(fn),"recall update"),ratio(len(tn),len(tn)+len(fn),"precision not update"),ratio(len(tn),len(tn)+len(fp),"recall not update");fu=f1(pu,ru,2*len(tp),2*len(tp)+len(fp)+len(fn),"f1 update");fno=f1(pn,rn,2*len(tn),2*len(tn)+len(fp)+len(fn),"f1 not update")
    if fu["raw"] is None or fno["raw"] is None:macro=ratio(0,0,"macro F1 not applicable")
    else:macro=ratio(fu["raw"]+fno["raw"],2,"macro F1")
    def groups(k):
        d=defaultdict(list)
        for x in inc:d[x[k]].append(x)
        return {a:{"total":len(v),"matches":sum(x["matchStatus"]=="MATCH" for x in v),"mismatches":sum(x["matchStatus"]=="MISMATCH" for x in v),"accuracyRaw":ratio(sum(x["matchStatus"]=="MATCH" for x in v),len(v),"breakdown")["raw"],"accuracyDisplayPercent":ratio(sum(x["matchStatus"]=="MATCH" for x in v),len(v),"breakdown")["displayPercent"],"experiments":[x["experimentId"] for x in v]} for a,v in sorted(d.items())}
    metrics={"accuracy":ratio(len(tp)+len(tn),len(inc),"accuracy"),"precisionShouldUpdate":pu,"recallShouldUpdate":ru,"f1ShouldUpdate":fu,"precisionShouldNotUpdate":pn,"recallShouldNotUpdate":rn,"f1ShouldNotUpdate":fno,"macroF1":macro,"balancedAccuracy":ratio(ru["raw"]+rn["raw"],2,"balanced accuracy") if ru["raw"] is not None and rn["raw"] is not None else ratio(0,0,"balanced accuracy")}
    case_map={x["caseId"]:x for x in inc if case_mapping_passed(x)}
    if pair_provenance["passed"]:
        unresolved=sorted({case for pair in pair_set for case in pair if case not in case_map})
        if unresolved:
            pair_set=set();pair_provenance=result(False,{**pair_provenance["evidence"],"availability":"NOT_AVAILABLE","reason":{"code":"UNRESOLVED_VALIDATED_CASE_MAPPING","detail":unresolved}},[f"unresolved validated CASE mappings: {unresolved}"])
    pairs=[]
    if pair_provenance["passed"]:
        for key in sorted(pair_set):
            members=[case_map[case] for case in key]
            hits=sum(x["matchStatus"]=="MATCH" for x in members);state="PAIR_FULLY_CORRECT" if hits==2 else "PAIR_NONE_CORRECT" if hits==0 else "PAIR_PARTIALLY_CORRECT";pairs.append({"contrastivePair":key,"caseIds":[x["caseId"] for x in members],"experimentIds":[x["experimentId"] for x in members],"memberResults":members,"pairStatus":state})
    model_checks=[x["provenance"]["modelConfig"] for x in inc]; prompt_checks=[x["provenance"]["prompt"] for x in inc]; first_checks=[x["provenance"]["attemptChain"] for x in inc]
    included_llm_checks=[(x["experimentId"],x.get("provenance",{}).get("llmOutput")) for x in inc]
    def llm_provenance_passed(check):return isinstance(check,dict) and check.get("passed") is True and check.get("evidence",{}).get("overallStatus")=="PASS"
    llm_output_failures=[exp for exp,check in included_llm_checks if not llm_provenance_passed(check)]
    llm_output_gate=bool(included_llm_checks) and len(included_llm_checks)==len(inc) and not llm_output_failures
    primary_gate_names=("FROZEN_PRIMARY_ORIGINS_VALID","ONE_SELECTED_EVALUATION_PER_INCLUDED_EXP","GROUND_TRUTH_PROVENANCE_VALID","PRIMARY_EXP_CASE_MAPPING_PROVENANCE_VALID","LLM_OUTPUT_PROVENANCE_VALID","MODEL_CONFIG_CONSISTENCY","PROMPT_PROVENANCE_VALID","FIRST_VALID_POLICY_COMPATIBLE","NO_DUPLICATE_EVALUATION_COUNTING")
    frozen_origins,source_coverage,required_primary_sources=primary_registry_gate(source_registry)
    gates={"FROZEN_PRIMARY_ORIGINS_VALID":frozen_origins,"ONE_SELECTED_EVALUATION_PER_INCLUDED_EXP":len(inc)==28,"GROUND_TRUTH_PROVENANCE_VALID":all(x.get("authoritativeGroundTruth") for x in inc),"PRIMARY_EXP_CASE_MAPPING_PROVENANCE_VALID":primary_mapping_gate,"FULL_CATALOG_CASE_MAPPING_PROVENANCE_COMPLETE":full_catalog_mapping_gate,"LLM_OUTPUT_PROVENANCE_VALID":llm_output_gate,"MODEL_CONFIG_CONSISTENCY":all(x["passed"] for x in model_checks),"PROMPT_PROVENANCE_VALID":all(x["passed"] for x in prompt_checks),"FIRST_VALID_POLICY_COMPATIBLE":all(x["passed"] for x in first_checks),"NO_DUPLICATE_EVALUATION_COUNTING":len({x["experimentId"] for x in inc})==len(inc)}
    if gates["PRIMARY_EXP_CASE_MAPPING_PROVENANCE_VALID"] and included_mapping_failures: raise ConsolidationIntegrityError("individual included CASE mapping failure escaped primary mapping gate")
    if gates["LLM_OUTPUT_PROVENANCE_VALID"] and llm_output_failures: raise ConsolidationIntegrityError("individual LLM output provenance failure escaped global gate")
    gates["PRIMARY_ANALYSIS_DATASET_INTEGRITY"]=all(gates[name] for name in primary_gate_names)
    gates["PRIMARY_RESULTS_REPRODUCIBLE"]=all(gates[name] for name in (*primary_gate_names,"PRIMARY_ANALYSIS_DATASET_INTEGRITY"))
    descriptive_complete=all(x["provenance"]["catalog"].get("passed") for x in inc)
    gates["DESCRIPTIVE_ATTRIBUTE_PROVENANCE_COMPLETE"]=descriptive_complete
    gates["PREDECLARED_CONTRASTIVE_PAIR_PROVENANCE_VALID"]=pair_provenance["passed"]
    if not gates["PRIMARY_RESULTS_REPRODUCIBLE"]:raise ConsolidationIntegrityError("primary integrity gate failure")
    availability={name:{"status":"AVAILABLE_FOR_REPRODUCIBLE_AGGREGATION" if descriptive_complete else "NOT_AVAILABLE_FOR_REPRODUCIBLE_AGGREGATION","coverage":{"complete":descriptive_complete,"includedExperiments":len(inc),"provenanceEvidence":[x["provenance"]["catalog"] for x in inc]}} for name in ("difficulty","category","targetFamily")}
    mapping_summary={"primaryExpCaseMappingProvenanceValid":gates["PRIMARY_EXP_CASE_MAPPING_PROVENANCE_VALID"],"fullCatalogCaseMappingProvenanceComplete":gates["FULL_CATALOG_CASE_MAPPING_PROVENANCE_COMPLETE"],"perExperiment":[{"experimentId":x["experimentId"],"includedInPrimaryAnalysis":x["includedInPrimaryAnalysis"],"caseId":x.get("caseId"),"caseMappingProvenance":x["provenance"]["caseMappingProvenance"]} for x in rows]}
    contrastive_analysis={"provenanceValid":pair_provenance["passed"],"availability":"AVAILABLE" if pair_provenance["passed"] else "NOT_AVAILABLE","reason":pair_provenance["evidence"].get("reason"),"provenance":pair_provenance,"pairs":pairs if pair_provenance["passed"] else None}
    data={"schemaVersion":"2.1.0","benchmark":"benchmark-v2","generatedAt":datetime.now(timezone.utc).isoformat(),"methodology":{"originalProtocol":{**proto,"path":PPATH},"amendment01":{**amendment,"path":APATH},"amendment02":{**amendment02,"path":APATH2},"hierarchy":"original protocol + amendment 01 + amendment 02; amendments govern descriptive/pair and EXP-to-CASE mapping provenance scope"},"protocol":{**proto,"path":PPATH},"amendment":{**amendment,"path":APATH},"amendment02":{**amendment02,"path":APATH2},"sources":sources,"integrityGates":gates,"caseMapping":mapping_summary,"summary":{"catalogExperiments":len(rows),"includedExperiments":len(inc),"excludedExperiments":len(rows)-len(inc),"matches":sum(x["matchStatus"]=="MATCH" for x in inc),"mismatches":sum(x["matchStatus"]=="MISMATCH" for x in inc)},"confusionMatrix":{"TP":{"count":len(tp),"experiments":tp},"FP":{"count":len(fp),"experiments":fp},"FN":{"count":len(fn),"experiments":fn},"TN":{"count":len(tn),"experiments":tn}},"metrics":metrics,"groundTruthBreakdown":groups("groundTruth"),"descriptiveAttributeAvailability":availability,"contrastivePairs":contrastive_analysis,"confidence":{"scope":"descriptive only; not calibrated and not used for scoring or exclusion","available":True},"operational":{},"experiments":rows}
    lines=["# Benchmark V2 — Consolidated Results","","## Methodology provenance","",json.dumps(data["methodology"],ensure_ascii=False),"","## Integrity gates",""]+[f"- {k}: {v}" for k,v in gates.items()]+["","## Dataset","",json.dumps(data["summary"]),"","## Primary result","",json.dumps(metrics),"","## Confusion matrix","",json.dumps(data["confusionMatrix"]),"","## Metrics","",json.dumps(metrics),"","## Ground Truth breakdown","",json.dumps(data["groundTruthBreakdown"]),"","## Descriptive attribute availability","",json.dumps(availability)]
    lines += ["","## Predeclared contrastive pairs",""]+([f"- {' / '.join(p['caseIds'])}: {p['pairStatus']}" for p in pairs] if pair_provenance["passed"] else ["Contrastive-pair analysis is NOT_AVAILABLE because provenance of the predeclared set could not be validated. This does not affect primary metrics."])
    lines += ["","## Confidence — descriptive only","","Not used in scoring, calibration, or exclusion.","","## Operational conditions","","Kept outside scoring.","","## Methodological limitations","","Difficulty, category, and target family are not aggregated when frozen provenance does not provide complete deterministic coverage under Amendment 01. No retrospective imputation is used.","","EXP-to-CASE mapping provenance is complete for every experiment included in the primary analysis. EXP-016 was already excluded by an independent normative status; no sufficient frozen evidence associates it with a CASE, and no retrospective association is inferred."]
    jt=json.dumps(data,ensure_ascii=False,indent=2)+"\n";mt="\n".join(lines)+"\n";json.loads(jt)
    if not validate_only:write_atomic(jt,mt)
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--validate-only",action="store_true")
    try:main(a.parse_args().validate_only)
    except ConsolidationIntegrityError as e:raise SystemExit(f"consolidation failed closed: {e}")
