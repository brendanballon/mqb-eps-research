// Read register writes and calibration references without changing the database.
import ghidra.app.script.GhidraScript;
import ghidra.app.util.PseudoDisassembler;
import java.io.PrintWriter;

public class ExportCalibrationContext1061 extends GhidraScript {
    public void run() throws Exception {
        try (PrintWriter out = new PrintWriter(getScriptArgs()[0])) {
            out.println("input_sha256=" + currentProgram.getExecutableSHA256());
            var tp = currentProgram.getRegister("tp");
            var listing = currentProgram.getListing();
            var iterator = listing.getInstructions(true);
            while (iterator.hasNext()) {
                var ins = iterator.next();
                if (ins.getAddress().getOffset() >= 0x55606) break;
                for (var result : ins.getResultObjects()) {
                    if (tp.equals(result)) {
                        out.println("TP_WRITE " + ins.getAddress() + " " + ins);
                    }
                }
                for (var ref : ins.getReferencesFrom()) {
                    long target = ref.getToAddress().getOffset();
                    if ((target >= 0x60000 && target < 0x61000) ||
                        (target >= 0xfa0012c0L && target < 0xfa001310L)) {
                        out.println("REF " + ins.getAddress() + " " + ref + " " + ins);
                    }
                }
            }
            for (long value : new long[]{0x100c0,0x20bf4,0x463e2,0x479d4,0x479de,0x4805a,0x1dc7c}) {
                var address = toAddr(value);
                out.println("CONTEXT " + address + " tp=" + currentProgram.getProgramContext().getValue(tp,address,false));
            }
            var decoder = new PseudoDisassembler(currentProgram);
            for (long[] range : new long[][]{{0x912a,0x9230},{0x48040,0x48088}}) {
                var pos = toAddr(range[0]);
                out.println("BOUNDED_DECODE " + pos + " end=" + toAddr(range[1]));
                while (pos.getOffset() < range[1]) {
                    var ins = decoder.disassemble(pos);
                    if (ins == null) { out.println("INVALID " + pos); break; }
                    out.println(pos + " " + ins);
                    pos = pos.add(ins.getLength());
                }
            }
        }
    }
}
