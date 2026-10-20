// Export table-relative operands and startup consumers without reanalysis.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import java.io.PrintWriter;
import java.util.LinkedHashSet;

public class ExportFocused1061 extends GhidraScript {
    public void run() throws Exception {
        try (PrintWriter out = new PrintWriter(getScriptArgs()[0])) {
            out.println("input_sha256="+currentProgram.getExecutableSHA256());
            var iterator=currentProgram.getListing().getInstructions(true);
            LinkedHashSet<Long> targets=new LinkedHashSet<>();
            for(long addr:new long[]{0x13cd2,0x141b6})targets.add(addr);
            while(iterator.hasNext()) {
                var ins=iterator.next();String text=ins.toString();
                if(ins.getAddress().getOffset()<0x55900 && (text.contains("tp") || text.contains("0x57a") || text.contains("0x5de") || text.contains("0x7a20"))) {
                    var f=getFunctionContaining(ins.getAddress());
                    out.println(ins.getAddress()+" "+text+" owner="+(f==null?"unknown":f.getEntryPoint()));
                    if(text.contains("0x5de") && f!=null)targets.add(f.getEntryPoint().getOffset());
                }
            }
            DecompInterface dec=new DecompInterface();
            try {
                dec.openProgram(currentProgram);
                for(long addr:targets) {
                    var f=getFunctionContaining(toAddr(addr));if(f==null)continue;
                    out.println("FUNCTION "+f.getEntryPoint()+" body="+f.getBody());
                    var inst=currentProgram.getListing().getInstructions(f.getBody(),true);
                    while(inst.hasNext()){var i=inst.next();out.println(i.getAddress()+" "+i);}
                    var result=dec.decompileFunction(f,30,monitor);
                    out.println("completed="+result.decompileCompleted()+" error="+result.getErrorMessage());
                    if(result.getDecompiledFunction()!=null)out.println(result.getDecompiledFunction().getC());
                }
            } finally {dec.dispose();}
        }
    }
}
