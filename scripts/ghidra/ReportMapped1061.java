// Retain mapped bytes, focused references, and one corroborating decompilation.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.program.model.listing.Function;
import java.io.PrintWriter;

public class ReportMapped1061 extends GhidraScript {
    public void run() throws Exception {
        try (PrintWriter out = new PrintWriter(getScriptArgs()[0])) {
            out.println("language=" + currentProgram.getLanguageID());
            out.println("input_sha256=" + currentProgram.getExecutableSHA256());
            out.println("program_image_base=" + currentProgram.getImageBase());
            out.println("Corroborated static working map. No hardware execution or complete flash dump.");
            for (var block : currentProgram.getMemory().getBlocks())
                out.println("BLOCK " + block.getStart() + " " + block.getEnd() + " bytes=" + block.getSize());
            out.println("functions=" + currentProgram.getFunctionManager().getFunctionCount());
            for (long value : new long[]{0xfb48, 0x57a20}) {
                var address = toAddr(value);
                out.println("BYTES " + address + " " + ghidra.util.NumericUtilities.convertBytesToString(getBytes(address, 40)));
                var refs = getReferencesTo(address);
                out.println("REFS " + address + " count=" + refs.length);
                for (var ref : refs) {
                    Function owner = getFunctionContaining(ref.getFromAddress());
                    out.println(ref + " function=" + (owner == null ? "unknown" : owner.getEntryPoint()));
                }
            }
            out.println("NEAR_TABLE_REFS inclusive=0x57a00..0x57a60");
            for (long value = 0x57a00; value <= 0x57a60; value++) {
                for (var ref : getReferencesTo(toAddr(value))) {
                    Function owner = getFunctionContaining(ref.getFromAddress());
                    out.println(ref + " instruction=" + getInstructionAt(ref.getFromAddress()) +
                        " function=" + (owner == null ? "unknown" : owner.getEntryPoint()));
                }
            }
            DecompInterface decompiler = new DecompInterface();
            try {
                decompiler.openProgram(currentProgram);
                var function = getFunctionAt(toAddr(0xf078));
                if (function != null) {
                    var result = decompiler.decompileFunction(function, 30, monitor);
                    out.println("DECOMPILE " + function.getEntryPoint() + " completed=" + result.decompileCompleted());
                    out.println("error=" + result.getErrorMessage());
                    if (result.getDecompiledFunction() != null) out.println(result.getDecompiledFunction().getC());
                }
            } finally { decompiler.dispose(); }
        }
    }
}
