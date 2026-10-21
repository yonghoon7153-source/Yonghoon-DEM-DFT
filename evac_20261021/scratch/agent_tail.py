import json, sys, os
base = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/tasks/"
for aid in sys.argv[1:]:
    p = os.path.realpath(base + aid + ".output")
    lines = open(p, encoding="utf-8").read().splitlines()
    n_tool = 0; last_ts = None; texts = []; tools = []
    for ln in lines:
        try: d = json.loads(ln)
        except Exception: continue
        last_ts = d.get("timestamp", last_ts)
        m = d.get("message") or {}
        if d.get("type") == "assistant":
            for c in m.get("content", []) if isinstance(m.get("content"), list) else []:
                if c.get("type") == "tool_use":
                    n_tool += 1
                    inp = c.get("input", {})
                    s = inp.get("command") or inp.get("file_path") or inp.get("description") or str(inp)[:120]
                    tools.append((d.get("timestamp","")[11:19], c.get("name"), str(s).replace("\n"," ")[:150]))
                elif c.get("type") == "text" and c.get("text","").strip():
                    texts.append((d.get("timestamp","")[11:19], c["text"].strip().replace("\n"," ")[:300]))
    print(f"=== {aid}  lines={len(lines)} tool_calls={n_tool} last_ts={last_ts}")
    for t in tools[-6:]: print("  T", t)
    for t in texts[-2:]: print("  X", t)
