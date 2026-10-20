// Test decompilation with offset coordinates and a provisional V850 profile.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.PrintWriter;

public class ProbeFunction extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        Address entry = toAddr(0x78);
        disassemble(entry);
        Function function = createFunction(entry, "candidate_offset_78");
        if (function == null) function = getFunctionAt(entry);
        if (function == null) throw new Exception("No function created");
        DecompInterface decompiler = new DecompInterface();
        try (PrintWriter out = new PrintWriter(args[0])) {
            out.println("language=" + currentProgram.getLanguageID());
            out.println("input_sha256=" + currentProgram.getExecutableSHA256());
            out.println("base=" + currentProgram.getImageBase());
            out.println("entry_file_offset=0x78");
            out.println("Provisional static probe. Offset coordinates are not a verified runtime mapping.");
            out.println("body=" + function.getBody());
            var instructions = currentProgram.getListing().getInstructions(function.getBody(), true);
            while (instructions.hasNext()) {
                var ins = instructions.next();
                out.println(ins.getAddress() + " " + ins);
            }
            decompiler.openProgram(currentProgram);
            DecompileResults result = decompiler.decompileFunction(function, 30, monitor);
            out.println("completed=" + result.decompileCompleted());
            out.println("error=" + result.getErrorMessage());
            if (result.getDecompiledFunction() != null) out.println(result.getDecompiledFunction().getC());
        } finally {
            decompiler.dispose();
        }
    }
}
