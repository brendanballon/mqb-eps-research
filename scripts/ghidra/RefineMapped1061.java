// Keep the observed constant region out of automatic instruction discovery.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.data.ArrayDataType;
import ghidra.program.model.data.ByteDataType;
import java.math.BigInteger;

public class RefineMapped1061 extends GhidraScript {
    public void run() throws Exception {
        createData(toAddr(0x55606),new ArrayDataType(ByteDataType.dataType,0x80000-0x55606,1));
        currentProgram.getMemory().split(currentProgram.getMemory().getBlock(toAddr(0x2000)),toAddr(0x55606));
        var constants=currentProgram.getMemory().getBlock(toAddr(0x55606));
        constants.setName("FLASH_CONSTANTS_CANDIDATE");constants.setExecute(false);constants.setWrite(false);
        var flash=currentProgram.getMemory().getBlock(toAddr(0x2000));flash.setName("FLASH_MIXED_CODE");flash.setWrite(false);
        currentProgram.getMemory().createUninitializedBlock("RAM_OBSERVED_STARTUP_RANGE",toAddr(0xfedf6000L),0xa000,false);
        var ram=currentProgram.getMemory().getBlock(toAddr(0xfedf6000L));ram.setRead(true);ram.setWrite(true);ram.setExecute(false);
        var context=currentProgram.getProgramContext();
        for(long start:new long[]{0xf078,0x10000}) {
            long end=start==0xf078?0xf900:0x55605;
            context.setValue(currentProgram.getRegister("tp"),toAddr(start),toAddr(end),new BigInteger("5d800",16));
            context.setValue(currentProgram.getRegister("gp"),toAddr(start),toAddr(end),new BigInteger("fee01000",16));
        }
        for(long addr:new long[]{0x9030,0xf078,0x10000}){disassemble(toAddr(addr));createFunction(toAddr(addr),null);}
        for(long addr=0x2000;addr<0x20c8;addr+=4){long ptr=Integer.toUnsignedLong(getInt(toAddr(addr)));if(ptr>=0x2000&&ptr<0x55606){disassemble(toAddr(ptr));createFunction(toAddr(ptr),null);}}
    }
}
