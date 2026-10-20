// Export startup and suspicious data-region evidence from the existing database.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.program.model.listing.Function;
import java.io.PrintWriter;
import java.util.HashSet;

public class InvestigateMapped1061 extends GhidraScript {
    public void run() throws Exception {
        try (PrintWriter out = new PrintWriter(getScriptArgs()[0])) {
            out.println("input_sha256=" + currentProgram.getExecutableSHA256());
            var funcs = currentProgram.getFunctionManager().getFunctions(true);
            try (PrintWriter inv = new PrintWriter(getScriptArgs()[1])) {
                inv.println("entry\tmax_address\tbody_bytes\tinstructions\tname");
                while (funcs.hasNext()) {
                    var f = funcs.next(); int count = 0;
                    var iterator = currentProgram.getListing().getInstructions(f.getBody(),true);
                    while (iterator.hasNext()) { iterator.next(); count++; }
                    inv.println(f.getEntryPoint()+"\t"+f.getBody().getMaxAddress()+"\t"+f.getBody().getNumAddresses()+"\t"+count+"\t"+f.getName());
                }
            }
            for (long[] range : new long[][]{{0x10000,0x10200},{0x558c0,0x55980}}) {
                out.println("LISTING " + Long.toHexString(range[0]));
                var iterator = currentProgram.getListing().getInstructions(toAddr(range[0]),true);
                while(iterator.hasNext()) { var i=iterator.next(); if(i.getAddress().getOffset()>range[1])break;out.println(i.getAddress()+" "+i); }
            }
            out.println("DATA_REGION_REFERENCES");
            var refiter = currentProgram.getReferenceManager().getReferenceDestinationIterator(toAddr(0x55000),true);
            while (refiter.hasNext()) {
                var dst=refiter.next(); if(dst.getOffset()>0x5e100)break;
                for(var ref:getReferencesTo(dst))out.println(ref+" instruction="+getInstructionAt(ref.getFromAddress()));
            }
            DecompInterface decompiler=new DecompInterface();
            try {
                decompiler.openProgram(currentProgram); HashSet<String> done=new HashSet<>();
                for (long addr:new long[]{0x10000,0x10084,0x55900,0x9030,0x951c}) {
                    Function f=getFunctionContaining(toAddr(addr));
                    if(f==null){out.println("NO_FUNCTION "+Long.toHexString(addr));continue;}
                    if(!done.add(f.getEntryPoint().toString()))continue;
                    out.println("FUNCTION "+f.getEntryPoint()+" BODY "+f.getBody());
                    if(f.getBody().getNumAddresses()>6000){out.println("SKIP oversized candidate");continue;}
                    var result=decompiler.decompileFunction(f,20,monitor);
                    out.println("completed="+result.decompileCompleted()+" error="+result.getErrorMessage());
                    if(result.getDecompiledFunction()!=null)out.println(result.getDecompiledFunction().getC());
                }
            } finally {decompiler.dispose();}
        }
    }
}
