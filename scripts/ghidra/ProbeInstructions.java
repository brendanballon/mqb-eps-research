// Decode bounded samples under an explicitly hypothetical language.
import ghidra.app.script.GhidraScript;
import ghidra.app.util.PseudoDisassembler;
import ghidra.app.util.PseudoInstruction;
import ghidra.program.model.address.Address;
import java.io.PrintWriter;

public class ProbeInstructions extends GhidraScript {
    public void run() throws Exception {
        String[] args = getScriptArgs();
        try (PrintWriter out = new PrintWriter(args[0])) {
            out.println("language=" + currentProgram.getLanguageID());
            out.println("base=" + currentProgram.getImageBase());
            out.println("Mapping is an offset coordinate system. CPU and load addresses remain hypotheses.");
            PseudoDisassembler decoder = new PseudoDisassembler(currentProgram);
            String[] samples = args.length > 1 ? args[1].split(",") :
                new String[]{"82", "100", "200", "400", "1000"};
            for (String sample : samples) {
                Address pos = toAddr(Long.parseLong(sample, 16));
                out.println("SAMPLE file-offset=0x" + sample);
                for (int i = 0; i < 32; i++) {
                    try {
                        PseudoInstruction ins = decoder.disassemble(pos);
                        if (ins == null) { out.println(pos + " INVALID"); break; }
                        out.println(pos + " " + ins.toString());
                        pos = pos.add(ins.getLength());
                    } catch (Exception error) {
                        out.println(pos + " INVALID " + error.getClass().getSimpleName());
                        break;
                    }
                }
            }
        }
    }
}
