// Export selected functions and exact incoming references from a saved database.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import java.io.PrintWriter;
import java.util.HashSet;

public class ExportFunctions1061 extends GhidraScript {
    public void run() throws Exception {
        String[] args=getScriptArgs();
        DecompInterface dec=new DecompInterface();
        try(PrintWriter out=new PrintWriter(args[0])) {
            out.println("input_sha256="+currentProgram.getExecutableSHA256());
            dec.openProgram(currentProgram);HashSet<String> done=new HashSet<>();
            for(String hex:args[1].split(",")) {
                var address=toAddr(Long.parseLong(hex,16));
                out.println("SELECT "+address);
                for(var ref:getReferencesTo(address))out.println("REF "+ref+" instruction="+getInstructionAt(ref.getFromAddress()));
                var f=getFunctionContaining(address);if(f==null){out.println("NO_FUNCTION");continue;}
                if(!done.add(f.getEntryPoint().toString()))continue;
                out.println("FUNCTION "+f.getEntryPoint()+" body="+f.getBody());
                var iterator=currentProgram.getListing().getInstructions(f.getBody(),true);
                while(iterator.hasNext()){var ins=iterator.next();out.println(ins.getAddress()+" "+ins);}
                var result=dec.decompileFunction(f,30,monitor);
                out.println("completed="+result.decompileCompleted()+" error="+result.getErrorMessage());
                if(result.getDecompiledFunction()!=null)out.println(result.getDecompiledFunction().getC());
            }
        } finally {dec.dispose();}
    }
}
