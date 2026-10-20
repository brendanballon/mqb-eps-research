// Read-only function and data-reference survey of the refined database.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import java.io.PrintWriter;

public class ExportTorqueSurvey1061 extends GhidraScript {
    public void run() throws Exception {
        DecompInterface dec = new DecompInterface();
        try (PrintWriter out = new PrintWriter(getScriptArgs()[0]);
             PrintWriter refs = new PrintWriter(getScriptArgs()[1])) {
            out.println("input_sha256="+currentProgram.getExecutableSHA256());
            refs.println("input_sha256="+currentProgram.getExecutableSHA256());
            dec.openProgram(currentProgram);
            var functions = currentProgram.getFunctionManager().getFunctions(true);
            while (functions.hasNext() && !monitor.isCancelled()) {
                var f = functions.next();
                out.println("FUNCTION "+f.getEntryPoint()+" body="+f.getBody());
                var result = dec.decompileFunction(f, 10, monitor);
                out.println("completed="+result.decompileCompleted()+" error="+result.getErrorMessage());
                if (result.getDecompiledFunction()!=null) out.println(result.getDecompiledFunction().getC());
                var instructions = currentProgram.getListing().getInstructions(f.getBody(),true);
                while (instructions.hasNext()) {
                    var ins = instructions.next();
                    for (var ref : ins.getReferencesFrom()) {
                        if (!ref.getReferenceType().isFlow()) refs.println(f.getEntryPoint()+"\t"+ins.getAddress()+"\t"+ref.getToAddress()+"\t"+ref.getReferenceType()+"\t"+ins);
                    }
                }
            }
        } finally { dec.dispose(); }
    }
}
