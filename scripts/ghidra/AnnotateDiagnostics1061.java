// Type verified records and export the diagnostic access-mask consumers.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.data.*;
import ghidra.program.model.symbol.SourceType;
import java.io.PrintWriter;
import java.util.TreeSet;

public class AnnotateDiagnostics1061 extends GhidraScript {
    private void bytes(long start,long end) throws Exception {
        createData(toAddr(start),new ArrayDataType(ByteDataType.dataType,(int)(end-start),1));
    }
    public void run() throws Exception {
        clearListing(toAddr(0x55606),toAddr(0x7ffff));
        bytes(0x55606,0x57a20);
        StructureDataType row=new StructureDataType("DiagnosticAccessConstantRow",0);
        row.add(UnsignedIntegerDataType.dataType,"comparison_constant",null);
        row.add(ByteDataType.dataType,"access_mask",null);
        row.add(new ArrayDataType(ByteDataType.dataType,3,1),"zero_padding",null);
        createData(toAddr(0x57a20),new ArrayDataType(row,5,8));
        createLabel(toAddr(0x57a20),"diagnostic_access_constant_rows",true);
        bytes(0x57a48,0x582fc);
        StructureDataType descriptor=new StructureDataType("DiagnosticServiceDescriptor",0);
        descriptor.add(UnsignedIntegerDataType.dataType,"service_identifier",null);
        descriptor.add(new PointerDataType(VoidDataType.dataType,4),"handler_address",null);
        descriptor.add(UnsignedIntegerDataType.dataType,"descriptor_flags",null);
        createData(toAddr(0x582fc),descriptor);
        createLabel(toAddr(0x582fc),"diagnostic_service_27_descriptor",true);
        bytes(0x58308,0x80000);
        for(Object[] item:new Object[][]{{0x30006L,"diagnostic_service_27_dispatch"},{0x2fd96L,"diagnostic_service_27_state_machine"},{0x2fd2aL,"diagnostic_constant_transform"},{0x13cd2L,"startup_initialize_memory"}}) {
            var f=getFunctionAt(toAddr((long)item[0]));if(f!=null)f.setName((String)item[1],SourceType.USER_DEFINED);
        }
        createLabel(toAddr(0xfedfaf85L),"diagnostic_access_mask",true);
        try(PrintWriter out=new PrintWriter(getScriptArgs()[0])) {
            out.println("input_sha256="+currentProgram.getExecutableSHA256());
            out.println("Manual names describe verified static roles, not observed execution.");
            out.println("TABLE "+getDataAt(toAddr(0x57a20)).getDataType());
            out.println("SERVICE "+getDataAt(toAddr(0x582fc)));
            TreeSet<String> owners=new TreeSet<>();
            for(var ref:getReferencesTo(toAddr(0xfedfaf85L))) {
                var f=getFunctionContaining(ref.getFromAddress());
                out.println(ref+" instruction="+getInstructionAt(ref.getFromAddress())+" function="+(f==null?"unknown":f.getEntryPoint()));
                if(f!=null)owners.add(f.getEntryPoint().toString());
            }
            out.println("MASK_OWNER_FUNCTIONS "+owners);
        }
    }
}
