import sys
import json
from client import SimulatedAnnealingOptimizer

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-simulated-annealing-metropolis-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "minimize_energy",
                    "description": "Optimize multi-variable continuous function using Simulated Annealing with Metropolis criterion",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "initial_state": {"type": "array", "items": {"type": "number"}},
                            "target_optimum": {"type": "array", "items": {"type": "number"}}
                        },
                        "required": ["initial_state"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "minimize_energy":
            init_st = args.get("initial_state", [0.0])
            target = args.get("target_optimum") or [1.0] * len(init_st)
            sa = SimulatedAnnealingOptimizer()
            cost_fn = lambda p: sum((p[i] - target[i])**2 for i in range(len(init_st)))
            data = sa.optimize(cost_fn, init_st)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
