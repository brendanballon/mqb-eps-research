// Seed bounded code candidates supported by the static map.
import ghidra.app.script.GhidraScript;

public class SeedMapped1061 extends GhidraScript {
    public void run() throws Exception {
        for (long address : new long[]{0x9030, 0xf078, 0x10000}) {
            disassemble(toAddr(address));
            createFunction(toAddr(address), null);
        }
        for (long address = 0x2000; address < 0x20c8; address += 4) {
            long pointer = Integer.toUnsignedLong(getInt(toAddr(address)));
            if (pointer >= 0x2000 && pointer < 0x80000) {
                disassemble(toAddr(pointer));
                createFunction(toAddr(pointer), null);
            }
        }
    }
}
