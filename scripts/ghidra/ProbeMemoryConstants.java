// Candidate memory constants. Raw aligned decoding is not code discovery.
import ghidra.app.script.GhidraScript;
import ghidra.app.util.PseudoDisassembler;
import java.io.PrintWriter;

public class ProbeMemoryConstants extends GhidraScript {
    public void run() throws Exception {
        var decoder = new PseudoDisassembler(currentProgram);
        try (var out = new PrintWriter(getScriptArgs()[0])) {
            out.println("sha256=" + currentProgram.getExecutableSHA256());
            out.println("language=" + currentProgram.getLanguageID());
            out.println("Halfword-aligned raw candidate scan. Includes data and overlapping decodes.");
            for (long offset = 0x2000; offset < 0x7fff8; offset += 2) {
                try {
                    var instruction = decoder.disassemble(toAddr(offset));
                    if (instruction == null || !instruction.getMnemonicString().equals("mov")) continue;
                    String text = instruction.toString();
                    if (!text.matches("mov 0xf[fFeE][0-9a-fA-F]{6},.*")) continue;
                    out.println("CANDIDATE " + instruction.getAddress() + " " + text);
                    var next = instruction.getAddress().add(instruction.getLength());
                    for (int i = 0; i < 4; i++) {
                        var follow = decoder.disassemble(next);
                        if (follow == null) break;
                        out.println("  " + next + " " + follow);
                        next = next.add(follow.getLength());
                    }
                } catch (Exception ignored) {}
            }
        }
    }
}
