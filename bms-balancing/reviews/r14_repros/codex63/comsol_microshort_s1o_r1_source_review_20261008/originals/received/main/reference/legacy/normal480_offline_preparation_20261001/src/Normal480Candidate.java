import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;
import com.comsol.model.physics.PhysicsFeature;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;

/** 6.3-native bounded validation. Current distribution initialization and a 480-second transient only.
 * Material literals: current public settings extracted from hashed installed library.
 * The running Java performs no external file reads.
 * Input hash is checked by the submitting MCP client before and after the job.
 * Output: audit tables through stdout, COMSOL-exported Java, and worker-saved MPH.
 */
public class Normal480Candidate {
    static final String LIBRARY = "C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/inputs/battery_lib_63.mph";
    static final String LIBRARY_SHA = "92cfd07d16fcb148ab1de4adbf48a3b9c6f709c2b8f04d9c571e4d702c4473f6";

    static double[] TIMES=null;
    static String stage="entry";
    static void checkShape(String tag,double[][] values,int count) {
        if(values==null||values.length!=count||count==0||values[0]==null||values[0].length==0)throw new IllegalStateException("SHAPE:"+tag);
        int n=values[0].length;
        for(double[] row:values){if(row==null||row.length!=n)throw new IllegalStateException("RAGGED:"+tag);for(double v:row)if(!Double.isFinite(v))throw new IllegalStateException("NONFINITE:"+tag);}
        if(values[0][0]!=0.0)throw new IllegalStateException("TIME_ORIGIN:"+tag);
        for(int i=0;i<n;i++)if(values[0][i]<0||values[0][i]>480||(i>0&&values[0][i]<=values[0][i-1]))throw new IllegalStateException("TIME_ORDER:"+tag);
        if(TIMES==null)TIMES=values[0].clone();else if(!Arrays.equals(values[0],TIMES))throw new IllegalStateException("EXACT_TIMES:"+tag);
    }
    static void units(Model m,String tag,String phase,String[] expected) throws Exception {
        String[] actual=m.result().numerical(tag).getStringArray("unit");
        table("units_"+tag+"_"+phase+".csv",new String[][]{{"tag","phase","expected","actual"},{tag,phase,Arrays.toString(expected),Arrays.toString(actual)}});
        if(!Arrays.equals(expected,actual))throw new IllegalStateException("UNIT:"+tag+":"+phase);
    }
    static String[] evaluatedUnits(String tag,String[] configured) {
        String[] u=configured.clone();
        if("eguard".equals(tag)){u[6]="";u[7]="";u[8]="";}
        if("nglobal".equals(tag))u[10]="";
        if(tag.startsWith("profile")&&!"profiletimes".equals(tag))u[7]="";
        return u;
    }
    static void interpSelection(Model m,String tag,int n) {
        int[] numbers=new int[n];for(int i=0;i<n;i++)numbers[i]=i+1;
        m.result().numerical(tag).set("solnum",numbers);
        m.result().numerical(tag).set("t",new double[0]);
        m.result().numerical(tag).set("timeinterp","off");
        if(!Arrays.equals(numbers,m.result().numerical(tag).getIntArray("solnum"))||m.result().numerical(tag).getDoubleArray("t").length!=0)throw new IllegalStateException("INTERP_SOLNUM");
    }
    static void interpReadback(Model m,String tag,double[] coords,int domain) {
        if(!"daudit".equals(m.result().numerical(tag).getString("data"))||!"off".equals(m.result().numerical(tag).getString("recover"))||!"off".equals(m.result().numerical(tag).getString("timeinterp"))||!"on".equals(m.result().numerical(tag).getString("coorderr"))||m.result().numerical(tag).getDouble("ext")!=0)throw new IllegalStateException("INTERP_MODE");
        if(m.result().numerical(tag).selection().dim()!=1||!Arrays.equals(m.result().numerical(tag).selection().entities(1),new int[]{domain})||!Arrays.deepEquals(m.result().numerical(tag).getDoubleMatrix("coord"),new double[][]{coords}))throw new IllegalStateException("INTERP_COORD_DOMAIN");
    }
    public static void main(String[] args) throws Exception { run(); }

    static String quote(String s) { return "\"" + (s == null ? "" : s.replace("\"", "\"\"")) + "\""; }
    static void table(String file, String[][] rows) throws Exception {
        StringBuilder out = new StringBuilder();
        if (rows != null) for (String[] row : rows) {
            if (row == null) continue;
            for (int i=0; i<row.length; i++) { if (i>0) out.append(','); out.append(quote(row[i])); }
            out.append('\n');
        }
        System.out.println("AUDIT_TABLE_BASE64=" + file + "|" + Base64.getEncoder().encodeToString(out.toString().getBytes(StandardCharsets.UTF_8)));
        System.out.println("AUDIT_FILE=" + file + " rows=" + (rows == null ? 0 : rows.length));
    }

    static void transport(PhysicsFeature f, String electrolyte, String epsl, String factor) {
        f.set("ElectrolyteMaterial", electrolyte);
        f.set("epsl", epsl);
        f.set("minput_temperature_src", "userdef");
        f.set("minput_temperature", "T_init");
        f.set("Dl_mat", "userdef"); f.set("Dl", "D_e");
        f.set("transpNum_mat", "userdef"); f.set("transpNum", "t_plus");
        f.set("IonicCorrModel", "userdef"); f.set("fl", factor);
        f.set("DiffusionCorrModel", "userdef"); f.set("fDl", factor);
        f.set("Migration", "userdef"); f.set("fmob", factor);
    }

    static void electrode(Model m, String tag, int domain, String material, String electrolyte,
                          String epss, String epsl, String factor, String conductivity,
                          String radius, String diffusion, String initial, String rate) {
        m.component("comp1").physics("liion").create(tag, "PorousElectrode", 1);
        PhysicsFeature f=m.component("comp1").physics("liion").feature(tag);
        f.selection().set(new int[]{domain});
        System.out.println(tag + "_DEFAULT_CHILDREN=" + Arrays.toString(f.feature().tags()));
        f.set("ElectrodeMaterial", material);
        transport(f, electrolyte, epsl, factor);
        f.set("epss", epss);
        f.set("sigma_mat", "userdef"); f.set("sigma", new String[]{conductivity,"0","0","0",conductivity,"0","0","0",conductivity});
        f.set("ElectricCorrModel", "userdef"); f.set("fs", factor);
        PhysicsFeature p=f.feature("pin1");
        p.set("minput_temperature_src", "userdef"); p.set("minput_temperature", "T_init");
        p.set("ParticleMaterial", material);
        p.set("cEeqref_mat", "from_mat");
        p.set("csinit", initial);
        p.set("rp", radius); p.set("Ds_mat", "userdef"); p.set("Ds", diffusion);
        p.set("ParticleConcentrationType", "SolveinExtraDimension");
        PhysicsFeature r=f.feature("per1");
        r.set("minput_temperature_src", "userdef"); r.set("minput_temperature", "T_init");
        r.set("Eeq_mat", "from_mat");
        r.set("ElectrodeKinetics", "LithiumInsertion");
        r.set("i0refType", "FromRateConstant"); r.set("k", rate);
        r.set("ActiveSpecificSurfaceAreaType", "ParticleBasedArea");
    }

    static void audit(PhysicsFeature f, String name) throws Exception {
        System.out.println("SELECTION_"+name+"="+Arrays.toString(f.selection().entities()));
        for (String kind : new String[]{"Expression","Weak","Constraint"})
            table("equations_"+name+"_"+kind+".csv", f.featureInfo("info").getInfoTable(kind));
    }

    static void material_mat35(Model m) {
        m.component("comp1").material().create("mat35", "Common");
        m.component("comp1").material("mat35").label("Graphite, LixC6 MCMB (Negative, Li-ion Battery)");
        m.component("comp1").material("mat35").propertyGroup("def").identifier("def");
        m.component("comp1").material("mat35").propertyGroup("def").addInput("temperature");
        m.component("comp1").material("mat35").propertyGroup("def").addInput("concentration");
        m.component("comp1").material("mat35").propertyGroup("def").set("electricconductivity",new String[]{"100[S/m]","0","0","0","100[S/m]","0","0","0","100[S/m]"});
        m.component("comp1").material("mat35").propertyGroup("def").set("diffusion",new String[]{"1.4523e-13*exp(68025.7/8.314*(1/(T_ref/1[K])-1/(T2/1[K])))[m^2/s]","0","0","0","1.4523e-13*exp(68025.7/8.314*(1/(T_ref/1[K])-1/(T2/1[K])))[m^2/s]","0","0","0","1.4523e-13*exp(68025.7/8.314*(1/(T_ref/1[K])-1/(T2/1[K])))[m^2/s]"});
        m.component("comp1").material("mat35").propertyGroup("def").set("thermalconductivity",new String[]{"1[W/(m*K)]","0","0","0","1[W/(m*K)]","0","0","0","1[W/(m*K)]"});
        m.component("comp1").material("mat35").propertyGroup("def").set("heatcapacity","750[J/(kg*K)]");
        m.component("comp1").material("mat35").propertyGroup("def").set("density","2300[kg/m^3]");
        m.component("comp1").material("mat35").propertyGroup("def").set("csmax","31507[mol/m^3]");
        m.component("comp1").material("mat35").propertyGroup("def").set("T_ref","318[K]");
        m.component("comp1").material("mat35").propertyGroup("def").set("T2","min(393.15,max(T,223.15))");
        m.component("comp1").material("mat35").propertyGroup("def").set("youngsmodulus","E_int(c/csmax)");
        m.component("comp1").material("mat35").propertyGroup("def").set("poissonsratio","nu_int(c/csmax)");
        m.component("comp1").material("mat35").propertyGroup("def").func().create("int1", "Interpolation");
        m.component("comp1").material("mat35").propertyGroup("def").func("int1").set("source","table");
        m.component("comp1").material("mat35").propertyGroup("def").func("int1").set("funcname","E_int");
        m.component("comp1").material("mat35").propertyGroup("def").func("int1").set("table",new String[][]{{"0","32.47"},{"0.333","28.56"},{"0.5","58.06"},{"1","108.67"}});
        m.component("comp1").material("mat35").propertyGroup("def").func("int1").set("fununit",new String[]{"GPa"});
        m.component("comp1").material("mat35").propertyGroup("def").func("int1").set("argunit",new String[]{"1"});
        m.component("comp1").material("mat35").propertyGroup("def").func("int1").set("funcinvname","int1_inv");
        m.component("comp1").material("mat35").propertyGroup("def").func().create("int2", "Interpolation");
        m.component("comp1").material("mat35").propertyGroup("def").func("int2").set("source","table");
        m.component("comp1").material("mat35").propertyGroup("def").func("int2").set("funcname","nu_int");
        m.component("comp1").material("mat35").propertyGroup("def").func("int2").set("table",new String[][]{{"0","0.32"},{"0.333","0.39"},{"0.5","0.34"},{"1","0.24"}});
        m.component("comp1").material("mat35").propertyGroup("def").func("int2").set("fununit",new String[]{""});
        m.component("comp1").material("mat35").propertyGroup("def").func("int2").set("funcinvname","int1_inv");
        m.component("comp1").material("mat35").propertyGroup("def").func().create("int3", "Interpolation");
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("source","table");
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("funcname","Eeq");
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("table",new String[][]{{"0","2.781186612"},{"0.01","1.520893224"},{"0.02","0.893922607"},{"0.03","0.581284406"},{"0.04","0.42452844"},{"0.05","0.344895805"},{"0.06","0.303146342"},{"0.07","0.279578072"},{"0.08","0.264093089"},{"0.09","0.251347845"},{"0.1","0.238588379"},{"0.11","0.224803164"},{"0.12","0.210294358"},{"0.13","0.196408586"},{"0.14","0.184624188"},{"0.15","0.175188157"},{"0.16","0.167373311"},{"0.17","0.160452107"},{"0.18","0.154025412"},{"0.19","0.147948522"},{"0.2","0.142214997"},{"0.21","0.13688271"},{"0.22","0.132033114"},{"0.23","0.127747573"},{"0.24","0.124091616"},{"0.25","0.121103387"},{"0.26","0.11878567"},{"0.27","0.117102317"},{"0.28","0.115980205"},{"0.29","0.115317054"},{"0.3","0.114993965"},{"0.31","0.114890105"},{"0.32","0.114886278"},{"0.33","0.114884619"},{"0.34","0.114873068"},{"0.35","0.114824904"},{"0.36","0.114644725"},{"0.37","0.114372614"},{"0.38","0.114017954"},{"0.39","0.11359371"},{"0.4","0.11311133"},{"0.41","0.112575849"},{"0.42","0.111980245"},{"0.43","0.111297682"},{"0.44","0.110470149"},{"0.45","0.109393081"},{"0.46","0.107900592"},{"0.47","0.10576964"},{"0.48","0.102783317"},{"0.49","0.09889031"},{"0.5","0.094391564"},{"0.51","0.089921069"},{"0.52","0.086112415"},{"0.53","0.083265315"},{"0.54","0.081326247"},{"0.55","0.080074892"},{"0.56","0.07928329"},{"0.57","0.078778765"},{"0.58","0.078447703"},{"0.59","0.078220432"},{"0.6","0.078055641"},{"0.61","0.077929111"},{"0.62","0.077826563"},{"0.63","0.077739397"},{"0.64","0.077662227"},{"0.65","0.077591472"},{"0.66","0.077524557"},{"0.67","0.077459463"},{"0.68","0.077394455"},{"0.69","0.077327934"},{"0.7","0.077258337"},{"0.71","0.077184077"},{"0.72","0.077103499"},{"0.73","0.077014851"},{"0.74","0.076916258"},{"0.75","0.07680571"},{"0.76","0.07668104"},{"0.77","0.07653992"},{"0.78","0.076379839"},{"0.79","0.076198086"},{"0.8","0.075991699"},{"0.81","0.075757371"},{"0.82","0.075491288"},{"0.83","0.075188813"},{"0.84","0.07484398"},{"0.85","0.074448647"},{"0.86","0.07399118"},{"0.87","0.073454466"},{"0.88","0.072812991"},{"0.89","0.072028722"},{"0.9","0.071045433"},{"0.91","0.069780996"},{"0.92","0.068116222"},{"0.93","0.065874599"},{"0.94","0.062770873"},{"0.95","0.058253898"},{"0.96","0.051075794"},{"0.97","0.038790069"},{"0.98","0.020172191"}});
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("extrap","linear");
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("fununit",new String[]{"V"});
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("argunit",new String[]{""});
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("defineinv","on");
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("funcinvname","Eeq_inv");
        m.component("comp1").material("mat35").propertyGroup("def").func().create("int4", "Interpolation");
        m.component("comp1").material("mat35").propertyGroup("def").func("int4").set("source","table");
        m.component("comp1").material("mat35").propertyGroup("def").func("int4").set("funcname","dEeqdT");
        m.component("comp1").material("mat35").propertyGroup("def").func("int4").set("table",new String[][]{{"0","3.0e-4"},{"0.17","0"},{"0.24","-6e-5"},{"0.28","-1.6e-4"},{"0.5","-1.6e-4"},{"0.54","-9e-5"},{"0.71","-9e-5"},{"0.85","-1.0e-4"},{"1.0","-1.2e-4"}});
        m.component("comp1").material("mat35").propertyGroup("def").func("int4").set("fununit",new String[]{"V/K"});
        m.component("comp1").material("mat35").propertyGroup("def").func("int4").set("argunit",new String[]{""});
        m.component("comp1").material("mat35").propertyGroup("def").func("int4").set("funcinvname","int2_inv");
        m.component("comp1").material("mat35").propertyGroup().create("ElectrodePotential","ElectrodePotential","Equilibrium potential");
        m.component("comp1").material("mat35").propertyGroup("ElectrodePotential").identifier("eeq");
        m.component("comp1").material("mat35").propertyGroup("ElectrodePotential").addInput("concentration");
        m.component("comp1").material("mat35").propertyGroup("ElectrodePotential").addInput("temperature");
        m.component("comp1").material("mat35").propertyGroup("ElectrodePotential").set("Eeq","def.Eeq(doc)+def.dEeqdT(doc)*(T-298[K])");
        m.component("comp1").material("mat35").propertyGroup("ElectrodePotential").set("dEeqdT","def.dEeqdT(doc)");
        m.component("comp1").material("mat35").propertyGroup("ElectrodePotential").set("cEeqref","def.csmax");
        m.component("comp1").material("mat35").propertyGroup("ElectrodePotential").set("doc","c/cEeqref");
        m.component("comp1").material("mat35").propertyGroup().create("OperationalSOC","OperationalSOC","Operational electrode state of charge");
        m.component("comp1").material("mat35").propertyGroup("OperationalSOC").identifier("opsoc");
        m.component("comp1").material("mat35").propertyGroup("OperationalSOC").set("socmin","def.Eeq_inv(E_max)");
        m.component("comp1").material("mat35").propertyGroup("OperationalSOC").set("socmax","def.Eeq_inv(E_min)");
        m.component("comp1").material("mat35").propertyGroup("OperationalSOC").set("E_max","1[V]");
        m.component("comp1").material("mat35").propertyGroup("OperationalSOC").set("E_min","0.075[V]");
        m.component("comp1").material("mat35").propertyGroup().create("ic","ic","Intercalation strain");
        m.component("comp1").material("mat35").propertyGroup("ic").identifier("is");
        m.component("comp1").material("mat35").propertyGroup("ic").addInput("concentration");
        m.component("comp1").material("mat35").propertyGroup("ic").set("dvol","dVOLdSOL(c/def.csmax)");
        m.component("comp1").material("mat35").propertyGroup("ic").func().create("int1", "Interpolation");
        m.component("comp1").material("mat35").propertyGroup("ic").func("int1").set("source","table");
        m.component("comp1").material("mat35").propertyGroup("ic").func("int1").set("funcname","dVOLdSOL");
        m.component("comp1").material("mat35").propertyGroup("ic").func("int1").set("table",new String[][]{{"0","0"},{"0.006802721088435382","0.12500000000000178"},{"0.06316812439261421","1.2736486486486491"},{"0.11175898931000966","2.523648648648649"},{"0.17978620019436342","3.5709459459459474"},{"0.2400388726919339","4.449324324324325"},{"0.2905733722060252","5.192567567567568"},{"0.3566569484936831","5.66554054054054"},{"0.4188532555879494","5.969594594594595"},{"0.48104956268221566","6.10472972972973"},{"0.5432458697764819","6.173648648648647"},{"0.58600583090379","6.306081081081081"},{"0.6112730806608356","7.726351351351352"},{"0.6443148688046647","8.570945945945946"},{"0.694849368318756","9.449324324324323"},{"0.7414965986394557","10.29391891891892"},{"0.7764820213799805","10.902027027027025"},{"0.8231292517006802","11.543918918918918"},{"0.8542274052478133","12.152027027027026"},{"0.8833819241982507","12.827702702702702"},{"0.9183673469387755","12.996621621621621"},{"0.9494655004859086","13.16554054054054"}});
        m.component("comp1").material("mat35").propertyGroup("ic").func("int1").set("extrap","linear");
        m.component("comp1").material("mat35").propertyGroup("ic").func("int1").set("fununit",new String[]{"%"});
        m.component("comp1").material("mat35").propertyGroup("ic").func("int1").set("argunit",new String[]{"1"});
        m.component("comp1").material("mat35").propertyGroup("ic").func("int1").set("funcinvname","int1_inv");
        m.component("comp1").material("mat35").propertyGroup().create("EquilibriumConcentration","EquilibriumConcentration","Equilibrium concentration");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumConcentration").identifier("Eqconc");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumConcentration").addInput("electricpotential");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumConcentration").set("csEq","def.csmax*def.Eeq_inv(V)");
        m.component("comp1").material("mat35").propertyGroup().create("EquilibriumPotentialWithDOCInput","EquilibriumPotentialWithDOCInput","Equilibrium potential (using degree of conversion as model input)");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumPotentialWithDOCInput").identifier("eeqdoc");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumPotentialWithDOCInput").addInput("degreeofconversion");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumPotentialWithDOCInput").addInput("temperature");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumPotentialWithDOCInput").set("Eeq","def.Eeq(doc)+def.dEeqdT(doc)*(T-298[K])");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumPotentialWithDOCInput").set("dEeqdT","def.dEeqdT(doc)");
        m.component("comp1").material("mat35").propertyGroup().create("EquilibriumDegreeOfConversion","EquilibriumDegreeOfConversion","Equilibrium degree of conversion");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumDegreeOfConversion").identifier("Eqdoc");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumDegreeOfConversion").addInput("electricpotential");
        m.component("comp1").material("mat35").propertyGroup("EquilibriumDegreeOfConversion").set("docEq","def.Eeq_inv(V)");
    }
    static void material_mat50(Model m) {
        m.component("comp1").material().create("mat50", "Common");
        m.component("comp1").material("mat50").label("LiPF6 in 3:7 EC:EMC (Liquid, Li-ion Battery)");
        m.component("comp1").material("mat50").propertyGroup("def").identifier("def");
        m.component("comp1").material("mat50").propertyGroup("def").addInput("concentration");
        m.component("comp1").material("mat50").propertyGroup("def").addInput("temperature");
        m.component("comp1").material("mat50").propertyGroup("def").set("diffusion",new String[]{"DL_int1(c/1[mol/m^3])*exp(16500/8.314*(1/(T_ref/1[K])-1/(T2/1[K])))","0","0","0","DL_int1(c/1[mol/m^3])*exp(16500/8.314*(1/(T_ref/1[K])-1/(T2/1[K])))","0","0","0","DL_int1(c/1[mol/m^3])*exp(16500/8.314*(1/(T_ref/1[K])-1/(T2/1[K])))"});
        m.component("comp1").material("mat50").propertyGroup("def").set("T_ref","298[K]");
        m.component("comp1").material("mat50").propertyGroup("def").set("T2","min(393.15,max(T,223.15))");
        m.component("comp1").material("mat50").propertyGroup("def").func().create("int1", "Interpolation");
        m.component("comp1").material("mat50").propertyGroup("def").func("int1").set("source","table");
        m.component("comp1").material("mat50").propertyGroup("def").func("int1").set("funcname","DL_int1");
        m.component("comp1").material("mat50").propertyGroup("def").func("int1").set("table",new String[][]{{"200","3.9e-10/(1-200*59e-6)"},{"500","4.12e-10/(1-500*59e-6)"},{"800","4e-10/(1-800*59e-6)"},{"1000","3.8e-10/(1-1000*59e-6)"},{"1200","3.50e-10/(1-1200*59e-6)"},{"1600","2.68e-10/(1-1600*59e-6)"},{"2000","1.9e-10/(1-2000*59e-6)"}});
        m.component("comp1").material("mat50").propertyGroup("def").func("int1").set("interp","piecewisecubic");
        m.component("comp1").material("mat50").propertyGroup("def").func("int1").set("fununit",new String[]{"m^2/s"});
        m.component("comp1").material("mat50").propertyGroup("def").func("int1").set("argunit",new String[]{""});
        m.component("comp1").material("mat50").propertyGroup("def").func("int1").set("funcinvname","int1_inv");
        m.component("comp1").material("mat50").propertyGroup().create("ElectrolyteConductivity","ElectrolyteConductivity","Electrolyte conductivity");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").identifier("ionc");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").addInput("concentration");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").addInput("temperature");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").set("sigmal",new String[]{"sigmal_int1(c/1[mol/m^3])*exp(4000/8.314*(1/(T_ref2/1[K])-1/(T3/1[K])))","0","0","0","sigmal_int1(c/1[mol/m^3])*exp(4000/8.314*(1/(T_ref2/1[K])-1/(T3/1[K])))","0","0","0","sigmal_int1(c/1[mol/m^3])*exp(4000/8.314*(1/(T_ref2/1[K])-1/(T3/1[K])))"});
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").set("T_ref2","298[K]");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").set("T3","min(393.15,max(T,223.15))");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func().create("int1", "Interpolation");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func("int1").set("source","table");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func("int1").set("funcname","sigmal_int1");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func("int1").set("table",new String[][]{{"0","1e-6"},{"200","0.455"},{"500","0.783"},{"800","0.935"},{"1000","0.95"},{"1200","0.927"},{"1600","0.78"},{"2000","0.60"},{"2200","0.515"}});
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func("int1").set("interp","piecewisecubic");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func("int1").set("fununit",new String[]{"S/m"});
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func("int1").set("argunit",new String[]{""});
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteConductivity").func("int1").set("funcinvname","int1_inv");
        m.component("comp1").material("mat50").propertyGroup().create("SpeciesProperties","SpeciesProperties","Species properties");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").identifier("SpeciesProperties");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").addInput("concentration");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").addInput("temperature");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").set("transpNum","transpNm_int1(c/1[mol/m^3])");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").set("fcl","actdep_int1(c/1[mol/m^3])*exp(-1000/8.314*(1/(T_ref3/1[K])-1/(T4/1[K])))");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").set("T4","min(393.15,max(T,223.15))");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").set("T_ref3","298[K]");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func().create("int1", "Interpolation");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int1").set("source","table");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int1").set("funcname","transpNm_int1");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int1").set("table",new String[][]{{"200","0.37"},{"500","0.322"},{"800","0.27"},{"1000","0.251"},{"1200","0.248"},{"1600","0.236"},{"2000","0.11"}});
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int1").set("interp","piecewisecubic");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int1").set("fununit",new String[]{""});
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int1").set("argunit",new String[]{""});
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int1").set("funcinvname","int1_inv");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func().create("int2", "Interpolation");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int2").set("source","table");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int2").set("funcname","actdep_int1");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int2").set("table",new String[][]{{"200","0"},{"500","0.29"},{"800","0.695"},{"1000","1"},{"1200","1.32"},{"1600","2.07"},{"2000","2.50"}});
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int2").set("interp","piecewisecubic");
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int2").set("fununit",new String[]{""});
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int2").set("argunit",new String[]{""});
        m.component("comp1").material("mat50").propertyGroup("SpeciesProperties").func("int2").set("funcinvname","int2_inv");
        m.component("comp1").material("mat50").propertyGroup().create("ElectrolyteSaltConcentration","ElectrolyteSaltConcentration","Electrolyte salt concentration");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteSaltConcentration").identifier("cElsalt");
        m.component("comp1").material("mat50").propertyGroup("ElectrolyteSaltConcentration").set("cElsalt","1200[mol/m^3]");
    }
    static void material_mat54(Model m) {
        m.component("comp1").material().create("mat54", "Common");
        m.component("comp1").material("mat54").label("NMC 811, LiNi0.8Mn0.1Co0.1O2 (Positive, Li-ion Battery)");
        m.component("comp1").material("mat54").propertyGroup("def").identifier("def");
        m.component("comp1").material("mat54").propertyGroup("def").addInput("temperature");
        m.component("comp1").material("mat54").propertyGroup("def").set("electricconductivity",new String[]{"0.17[S/m]","0","0","0","0.17[S/m]","0","0","0","0.17[S/m]"});
        m.component("comp1").material("mat54").propertyGroup("def").set("diffusion",new String[]{"5e-13*exp(1200*(1/(T_ref/1[K])-1/(T2/1[K])))[m^2/s]","0","0","0","5e-13*exp(1200*(1/(T_ref/1[K])-1/(T2/1[K])))[m^2/s]","0","0","0","5e-13*exp(1200*(1/(T_ref/1[K])-1/(T2/1[K])))[m^2/s]"});
        m.component("comp1").material("mat54").propertyGroup("def").set("thermalconductivity",new String[]{"1.58[W/(m*K)]","0","0","0","1.58[W/(m*K)]","0","0","0","1.58[W/(m*K)]"});
        m.component("comp1").material("mat54").propertyGroup("def").set("heatcapacity","840.1[J/(kg*K)]");
        m.component("comp1").material("mat54").propertyGroup("def").set("density","4.87[g/cm^3]");
        m.component("comp1").material("mat54").propertyGroup("def").set("csmax","50060[mol/m^3]");
        m.component("comp1").material("mat54").propertyGroup("def").set("T_ref","298[K]");
        m.component("comp1").material("mat54").propertyGroup("def").set("T2","min(393.15,max(T,223.15))");
        m.component("comp1").material("mat54").propertyGroup("def").func().create("int1", "Interpolation");
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("source","table");
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("funcname","Eeq");
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("table",new String[][]{{"0.2228930343076256","4.256817954840526"},{"0.23718770939025557","4.2212385803217725"},{"0.2503742701253948","4.198216215024365"},{"0.2635608308605341","4.184354581468334"},{"0.2767473915956734","4.175555457558853"},{"0.28993395233081265","4.169287588472648"},{"0.3031205130659519","4.163501863162304"},{"0.3163070738010912","4.156631314356272"},{"0.3294936345362305","4.145300935623516"},{"0.3426801952713697","4.130836622347658"},{"0.355866756006509","4.113841054248525"},{"0.3690533167416483","4.09395262349422"},{"0.38223987747678756","4.0746668724597415"},{"0.3954264382119268","4.056104337089057"},{"0.4086129989470661","4.037903409550268"},{"0.4217995596822054","4.021944450569238"},{"0.43498612041734463","4.007287279783036"},{"0.44817268115248393","3.9945104697226936"},{"0.4613592418876232","3.9798050845589046"},{"0.47454580262276247","3.96497916345115"},{"0.4877323633579017","3.9507559220632222"},{"0.500918924093041","3.9348451774597786"},{"0.5141054848281803","3.918090681248576"},{"0.5272920455633195","3.901215649093408"},{"0.5404786062984588","3.884581688826171"},{"0.5536651670335981","3.8661396893994517"},{"0.5668517277687374","3.850108408852042"},{"0.5800382885038766","3.834920879912391"},{"0.593224849239016","3.819612815028774"},{"0.6064114099741551","3.806233325248605"},{"0.6195979707092945","3.795023482459815"},{"0.6327845314444338","3.7852600709986106"},{"0.6459710921795729","3.77646094708913"},{"0.6591576529147123","3.7660948559080984"},{"0.6723442136498515","3.7569341241667216"},{"0.6855307743849908","3.748376072145172"},{"0.6987173351201301","3.7407823076753464"},{"0.7119038958552694","3.7321037197098312"},{"0.7250904565904086","3.724148347408109"},{"0.738277017325548","3.7154697594425943"},{"0.7514635780606872","3.7046215244857006"},{"0.7646501387958264","3.69582240057622"},{"0.7778366995309657","3.686541132890878"},{"0.791023260266105","3.6770187933176044"},{"0.8042098210012443","3.6672553818564"},{"0.8173963817363835","3.6556839312357132"},{"0.8305829424715228","3.643871408727096"},{"0.8437695032066621","3.633505317546064"},{"0.8569560639418013","3.6226570825891704"},{"0.8701426246769406","3.6130142070719313"},{"0.8833291854120799","3.603009723722796"},{"0.8965157461472192","3.592643632541764"},{"0.9097023068823584","3.585049868071939"},{"0.9228888676174977","3.5790230708736646"},{"0.9351335311572699","3.5724538619275457"},{"0.9505178520149323","3.5661257248693574"},{"0.9624485498229155","3.559857855783152"},{"0.9756351105580549","3.5525051632012574"},{"0.9888216712931941","3.541536392300398"},{"0.998240643246865","3.488540755603573"},{"0.9994965061740211","3.3640592684056174"},{"1","3.0"}});
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("extrap","linear");
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("fununit",new String[]{"V"});
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("argunit",new String[]{""});
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("defineinv","on");
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("funcinvname","Eeq_inv");
        m.component("comp1").material("mat54").propertyGroup("def").func().create("int2", "Interpolation");
        m.component("comp1").material("mat54").propertyGroup("def").func("int2").set("source","table");
        m.component("comp1").material("mat54").propertyGroup("def").func("int2").set("funcname","dEeqdT");
        m.component("comp1").material("mat54").propertyGroup("def").func("int2").set("table",new String[][]{{"0.220410330184718","0.014014955374719168"},{"0.23880574126341392","0.017971951837248937"},{"0.2546142976591682","0.024888006339594898"},{"0.27162047196369177","0.034054905194386115"},{"0.282638556724369","0.036404922469418094"},{"0.3020399668464311","0.026993759520293023"},{"0.3142556695158776","0.020431501191878212"},{"0.33365707963793967","0.011727335839959649"},{"0.35521420199578646","0.0148088719318831"},{"0.3681484754104945","0.017914441947786144"},{"0.3861127440420335","0.021513559747933717"},{"0.40838843714514184","0.01892213947907556"},{"0.4213227105598499","0.01702025282904991"},{"0.43856840844612727","0.013603757832495345"},{"0.46156267229449716","0.005230230696620208"},{"0.47449694570920525","-0.0006265898806357695"},{"0.49389835583126734","-0.007070755018626973"},{"0.5161740489343756","-0.004108523109428802"},{"0.5291083223490838","-0.001082689664639258"},{"0.5463540202353612","0.002312976397604097"},{"0.569348284083731","0.004079283221664273"},{"0.582282557498439","0.004952229246388926"},{"0.6009653968752395","0.004819533211418328"},{"0.6239596607236095","-0.006710676178650704"},{"0.6368939341383175","-0.014536990062410493"},{"0.6541396320245949","-0.02419065684384447"},{"0.6771338958729649","-0.029277265326040275"},{"0.6900681692876729","-0.031219020261622682"},{"0.7073138671739503","-0.033690193909531485"},{"0.7303081310223203","-0.03336889094642845"},{"0.7432424044370283","-0.032113209380358915"},{"0.7619252438138289","-0.03159295149409996"},{"0.7849195076621986","-0.03042821280099617"},{"0.7971352103316451","-0.02983057002436801"},{"0.8150994789631842","-0.02874483754190857"},{"0.838093742811554","-0.024193952462184226"},{"0.851028016226262","-0.02144719701629197"},{"0.8689922848578011","-0.01850371317212532"},{"0.8898308364703862","-0.024913854049501444"},{"0.9027651098850944","-0.030147134640649775"},{"0.922885090752418","-0.038671237648857465"},{"0.9430050716197416","-0.05040518062533475"},{"0.958813628015496","-0.06017799045704739"},{"0.9758198023200195","-0.07034189432587595"},{"0.983245033354389","-0.07341413831343596"}});
        m.component("comp1").material("mat54").propertyGroup("def").func("int2").set("fununit",new String[]{"mV/K"});
        m.component("comp1").material("mat54").propertyGroup("def").func("int2").set("argunit",new String[]{""});
        m.component("comp1").material("mat54").propertyGroup("def").func("int2").set("funcinvname","int2_inv");
        m.component("comp1").material("mat54").propertyGroup().create("ElectrodePotential","ElectrodePotential","Equilibrium potential");
        m.component("comp1").material("mat54").propertyGroup("ElectrodePotential").identifier("eeq");
        m.component("comp1").material("mat54").propertyGroup("ElectrodePotential").addInput("concentration");
        m.component("comp1").material("mat54").propertyGroup("ElectrodePotential").addInput("temperature");
        m.component("comp1").material("mat54").propertyGroup("ElectrodePotential").set("Eeq","def.Eeq(doc)+def.dEeqdT(doc)*(T-298[K])");
        m.component("comp1").material("mat54").propertyGroup("ElectrodePotential").set("dEeqdT","def.dEeqdT(doc)");
        m.component("comp1").material("mat54").propertyGroup("ElectrodePotential").set("cEeqref","def.csmax");
        m.component("comp1").material("mat54").propertyGroup("ElectrodePotential").set("doc","c/cEeqref");
        m.component("comp1").material("mat54").propertyGroup().create("OperationalSOC","OperationalSOC","Operational electrode state of charge");
        m.component("comp1").material("mat54").propertyGroup("OperationalSOC").identifier("opsoc");
        m.component("comp1").material("mat54").propertyGroup("OperationalSOC").set("socmax","def.Eeq_inv(E_min)");
        m.component("comp1").material("mat54").propertyGroup("OperationalSOC").set("socmin","def.Eeq_inv(E_max)");
        m.component("comp1").material("mat54").propertyGroup("OperationalSOC").set("E_max","4.25[V]");
        m.component("comp1").material("mat54").propertyGroup("OperationalSOC").set("E_min","3.5[V]");
        m.component("comp1").material("mat54").propertyGroup().create("ic","ic","Intercalation strain");
        m.component("comp1").material("mat54").propertyGroup("ic").identifier("is");
        m.component("comp1").material("mat54").propertyGroup("ic").addInput("concentration");
        m.component("comp1").material("mat54").propertyGroup("ic").set("dvol","dVOLdSOL(c/def.csmax)");
        m.component("comp1").material("mat54").propertyGroup("ic").func().create("int1", "Interpolation");
        m.component("comp1").material("mat54").propertyGroup("ic").func("int1").set("source","table");
        m.component("comp1").material("mat54").propertyGroup("ic").func("int1").set("funcname","dVOLdSOL");
        m.component("comp1").material("mat54").propertyGroup("ic").func("int1").set("table",new String[][]{{"1","0"},{"0.8878314072059823","-0.01908801696712681"},{"0.8558803535010198","-0.09544008483563182"},{"0.8273283480625425","-0.19724284199363806"},{"0.7919782460910945","-0.2905620360551433"},{"0.7627464309993202","-0.3584305408271482"},{"0.7321549966009517","-0.42629904559915177"},{"0.7042828008157715","-0.5026511134676568"},{"0.6709721278042148","-0.5705196182396608"},{"0.6349422161794698","-0.6383881230116648"},{"0.6084296397008837","-0.7147401908801698"},{"0.5791978246091094","-0.8335100742311776"},{"0.5506458191706322","-0.9862142099681872"},{"0.5193745751189666","-1.1049840933191946"},{"0.4894629503738953","-1.2067868504772008"},{"0.45955132562882384","-1.3425238600212097"},{"0.42556084296397","-1.51219512195122"},{"0.39700883752549276","-1.6818663838812302"},{"0.36573759347382717","-1.8515376458112414"},{"0.3358259687287558","-2.106044538706257"},{"0.3099932019034669","-2.496288441145281"},{"0.27464309993201896","-3.1240721102863205"},{"0.2447314751869476","-3.921527041357371"},{"0.213460231135282","-4.820784729586427"},{"0.18218898708361642","-5.669141039236479"},{"0.15091774303195082","-6.534464475079533"}});
        m.component("comp1").material("mat54").propertyGroup("ic").func("int1").set("extrap","linear");
        m.component("comp1").material("mat54").propertyGroup("ic").func("int1").set("fununit",new String[]{"%"});
        m.component("comp1").material("mat54").propertyGroup("ic").func("int1").set("argunit",new String[]{"1"});
        m.component("comp1").material("mat54").propertyGroup("ic").func("int1").set("funcinvname","int1_inv");
        m.component("comp1").material("mat54").propertyGroup().create("EquilibriumConcentration","EquilibriumConcentration","Equilibrium concentration");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumConcentration").identifier("Eqconc");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumConcentration").addInput("electricpotential");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumConcentration").set("csEq","def.csmax*def.Eeq_inv(V)");
        m.component("comp1").material("mat54").propertyGroup().create("EquilibriumPotentialWithDOCInput","EquilibriumPotentialWithDOCInput","Equilibrium potential (using degree of conversion as model input)");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumPotentialWithDOCInput").identifier("eeqdoc");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumPotentialWithDOCInput").addInput("degreeofconversion");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumPotentialWithDOCInput").addInput("temperature");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumPotentialWithDOCInput").set("Eeq","def.Eeq(doc)+def.dEeqdT(doc)*(T-298[K])");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumPotentialWithDOCInput").set("dEeqdT","def.dEeqdT(doc)");
        m.component("comp1").material("mat54").propertyGroup().create("EquilibriumDegreeOfConversion","EquilibriumDegreeOfConversion","Equilibrium degree of conversion");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumDegreeOfConversion").identifier("Eqdoc");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumDegreeOfConversion").addInput("electricpotential");
        m.component("comp1").material("mat54").propertyGroup("EquilibriumDegreeOfConversion").set("docEq","def.Eeq_inv(V)");
    }


    static double[][] evaluate(Model m, String tag, String type, String[] expr, String[] configured, int[] entities) throws Exception {
        m.result().numerical().create(tag,type);m.result().numerical(tag).set("data","daudit");
        if(entities!=null){if(!type.equals("EvalPoint"))m.result().numerical(tag).selection().geom("geom1",1);m.result().numerical(tag).selection().set(entities);}
        m.result().numerical(tag).set("expr",expr);if(configured!=null)m.result().numerical(tag).set("unit",configured);
        m.result().numerical(tag).set("innerinput","all");
        if(!Arrays.equals(expr,m.result().numerical(tag).getStringArray("expr"))||!"daudit".equals(m.result().numerical(tag).getString("data"))||!"all".equals(m.result().numerical(tag).getString("innerinput")))throw new IllegalStateException("NUMERICAL_BINDING:"+tag);
        if(entities!=null){int dim=type.equals("EvalPoint")?0:1;if(m.result().numerical(tag).selection().dim()!=dim||!Arrays.equals(entities,m.result().numerical(tag).selection().entities(dim)))throw new IllegalStateException("NUMERICAL_SELECTION:"+tag);}
        if(configured!=null)units(m,tag,"configured",configured);
        double[][] values=m.result().numerical(tag).getReal();checkShape(tag,values,expr.length);
        if(configured!=null)units(m,tag,"evaluated",evaluatedUnits(tag,configured));
        return values;
    }
    static void numericTable(String file,String[] headers,double[][] data) throws Exception {
        checkShape(file,data,headers.length);
        String[][] rows=new String[data[0].length+1][headers.length];rows[0]=headers;
        for(int col=0;col<data[0].length;col++)for(int row=0;row<headers.length;row++)rows[col+1][row]=Double.toString(data[row][col]);
        table(file,rows);
    }

    // Solver-side electrolyte operators, not postprocessing MinLine nodes.
    static void electrolyteCouplings(Model m) throws Exception {
        for (int k=0;k<=3;k++) {
            String tag=k==0?"minguardall":"minguard"+k;
            int[] domains=k==0?new int[]{1,2,3}:new int[]{k};
            m.component("comp1").cpl().create(tag,"Minimum","geom1");
            m.component("comp1").cpl(tag).selection().geom("geom1",1);
            m.component("comp1").cpl(tag).selection().set(domains);
            m.component("comp1").cpl(tag).set("points","lagrange");
            m.component("comp1").cpl(tag).set("lagrange","5");
            int dim=m.component("comp1").cpl(tag).selection().dim();
            int[] actual=m.component("comp1").cpl(tag).selection().entities(1);
            if(dim!=1 || !Arrays.equals(actual,domains)) throw new IllegalStateException("Electrolyte selection mismatch "+tag);
            System.out.println("ELECTROLYTE_COUPLING="+tag+"|dimension="+dim+"|entities="+Arrays.toString(actual)+"|points="+m.component("comp1").cpl(tag).getString("points")+"|lagrange="+m.component("comp1").cpl(tag).getString("lagrange"));
        }
    }
    static void electrolyteEvidence(Model m,String ocpGuard,String surfaceGuard) throws Exception {
        String[] expr={"t","comp1.minguardall(comp1.cl)","comp1.minguard1(comp1.cl)","comp1.minguard2(comp1.cl)","comp1.minguard3(comp1.cl)","ce_stop_threshold","comp1.minguardall(comp1.cl)<=ce_stop_threshold",ocpGuard,surfaceGuard};
        String[] u={"s","mol/m^3","mol/m^3","mol/m^3","mol/m^3","mol/m^3","1","1","1"};
        double[][] inferred=evaluate(m,"eguard","EvalGlobal",expr,null,null);
        units(m,"eguard","inferred",evaluatedUnits("eguard",u));
        m.result().numerical("eguard").set("unit",u);units(m,"eguard","configured",u);
        double[][] values=m.result().numerical("eguard").getReal();checkShape("eguard",values,9);
        units(m,"eguard","evaluated",evaluatedUnits("eguard",u));
        if(!Arrays.deepEquals(inferred,values))throw new IllegalStateException("GUARD_UNIT_VALUES");
        for(int i:new int[]{6,7,8})for(double flag:values[i])if(flag!=0&&flag!=1)throw new IllegalStateException("GUARD_BOOLEAN");
        numericTable("electrolyte_guard.csv",new String[]{"time_s","ce_min_all_mol_m3","ce_min_d1_mol_m3","ce_min_d2_mol_m3","ce_min_d3_mol_m3","threshold_mol_m3","electrolyte_guard","ocp_guard","surface_guard"},values);
    }

    static void preflightAudit(Model m) throws Exception {
        electrolyteCouplings(m);
        for(int domain:new int[]{1,3}) for(String op:new String[]{"min","max"}) {
            String tag=op+"surf"+domain;
            m.component("comp1").cpl().create(tag,op.equals("min")?"Minimum":"Maximum","geom1");
            m.component("comp1").cpl(tag).selection().geom("geom1",1);
            m.component("comp1").cpl(tag).selection().set(new int[]{domain});
            m.component("comp1").cpl(tag).set("points","lagrange");
            m.component("comp1").cpl(tag).set("lagrange","5");
        }
        String nmin="comp1.minsurf1(comp1.liion.socloc_surface)", nmax="comp1.maxsurf1(comp1.liion.socloc_surface)";
        String pmin="comp1.minsurf3(comp1.liion.socloc_surface)", pmax="comp1.maxsurf3(comp1.liion.socloc_surface)";
        String guard="("+nmin+"<0)||("+nmax+">0.98)||("+pmin+"<0.2228930343076256)||("+pmax+">0.983245033354389)";
        String concentrationGuard="("+nmin+"<=0)||("+nmax+">=1)||("+pmin+"<=0)||("+pmax+">=1)";
        String electrolyteGuard="comp1.minguardall(comp1.cl)<=ce_stop_threshold";
        m.study("std1").createAutoSequences("sol");
        String sol=null,time=null;
        for(String candidate:m.study("std1").getSolverSequences("All")) for(String f:m.sol(candidate).feature().tags())
            if(m.sol(candidate).feature(f).getType().equals("Time")) {
                if(sol!=null) throw new IllegalStateException("Multiple time solvers"); sol=candidate; time=f;
            }
        if(sol==null) throw new IllegalStateException("No time solver");
        m.sol(sol).feature(time).set("initialstepbdfactive","on");
        m.sol(sol).feature(time).set("initialstepbdf",1e-5);
        m.sol(sol).feature(time).set("maxstepconstraintbdf","expr");
        m.sol(sol).feature(time).set("maxstepbdf",0.1);
        m.sol(sol).feature(time).set("maxstepexpressionbdf","if(t<0.1[s],0.000125[s],0.1[s])");
        m.sol(sol).feature(time).set("rtol",1e-6);
        m.sol(sol).feature(time).set("tout","tsteps");
        m.sol(sol).feature(time).set("tstepsstore",1);
        m.sol(sol).feature(time).set("tstepsbdf","strict");
        m.sol(sol).feature(time).set("eventout","on");
        m.sol(sol).feature(time).create("stguard","StopCondition");
        String[] conditions=false ? new String[]{guard,concentrationGuard,"comp1.liion.cdc1.cycle_counter>0.5"}:new String[]{guard,concentrationGuard,electrolyteGuard};
        for(int i=0;i<conditions.length;i++) {
            m.sol(sol).feature(time).feature("stguard").setIndex("stopcondarr",conditions[i],i);
            m.sol(sol).feature(time).feature("stguard").setIndex("stopcondActive","on",i);
            m.sol(sol).feature(time).feature("stguard").setIndex("stopcondterminateon","true",i);
            m.sol(sol).feature(time).feature("stguard").setIndex("stopconddesc",i==0?"OCP surface outside table":i==1?"Invalid surface concentration":"Electrolyte minimum <= threshold",i);
        }
        m.sol(sol).feature(time).feature("stguard").set("storestopcondsol","stepbefore_stepafter");
        String[] observedConditions=m.sol(sol).feature(time).feature("stguard").getStringArray("stopcondarr");
        String[] observedActive=m.sol(sol).feature(time).feature("stguard").getStringArray("stopcondActive");
        String[] observedTerminate=m.sol(sol).feature(time).feature("stguard").getStringArray("stopcondterminateon");
        if(!Arrays.equals(observedConditions,conditions)||!Arrays.equals(observedActive,new String[]{"on","on","on"})||!Arrays.equals(observedTerminate,new String[]{"true","true","true"}))throw new IllegalStateException("GUARD_READBACK");
        String observedStorage=m.sol(sol).feature(time).feature("stguard").getString("storestopcondsol");
        if(!"stepbefore_stepafter".equals(observedStorage)||m.param().evaluate("ce_stop_threshold")!=0.0)throw new IllegalStateException("GUARD_THRESHOLD_STORAGE");
        table("guard_binding.csv",new String[][]{{"electrolyte_expression","stop_storage","active","terminate_on","threshold_SI"},{observedConditions[2],observedStorage,observedActive[2],observedTerminate[2],Double.toString(m.param().evaluate("ce_stop_threshold"))}});
        System.out.println("ELECTROLYTE_THRESHOLD_EXPRESSION="+m.param().get("ce_stop_threshold"));
        System.out.println("ELECTROLYTE_THRESHOLD_SI="+m.param().evaluate("ce_stop_threshold"));
        System.out.println("PREFLIGHT_GUARD="+guard);
        System.out.println("PREFLIGHT_TIME=maxstep_expression=if(t<0.1[s],0.000125[s],0.1[s])|inactive_constant_slot_s=0.1|initialstep_s=1e-5|rtol=1e-6|strict|all accepted steps|eventout|consistency="+m.sol(sol).feature(time).getString("consistent"));
        System.out.println("PREFLIGHT_SOLVE_BEGIN=0..480 seconds; NO full protocol or sweep");
        runtimeSettings(m,sol,time);
        stage="solve";
        m.sol(sol).runAll();
        stage="postprocess";
        System.out.println("PREFLIGHT_SOLVER_RETURNED=true; physical checks separate");
        m.result().dataset().create("daudit","Solution"); m.result().dataset("daudit").set("solution",sol);
        electrolyteEvidence(m,guard,concentrationGuard);
        String[] globalExpr={"t","comp1.intd1(comp1.liion.epss*comp1.liion.cs_average)","comp1.intd3(comp1.liion.epss*comp1.liion.cs_average)",
            "comp1.intd1(comp1.liion.epsl*comp1.cl)+comp1.intd2(comp1.liion.epsl*comp1.cl)+comp1.intd3(comp1.liion.epsl*comp1.cl)",
            "comp1.intd1(comp1.liion.cs_average)/(L_el*cs_Gr_max)","comp1.intd3(comp1.liion.cs_average)/(L_pos*cs_NCM_max)",
            nmin,nmax,pmin,pmax,guard,"comp1.intd1(comp1.liion.ivtot)","comp1.intd3(comp1.liion.ivtot)","-comp1.intd2(comp1.liion.Isx)/L_sep"};
        numericTable("preflight_global.csv",new String[]{"time_s","Li_N_mol_m2","Li_P_mol_m2","Li_electrolyte_mol_m2","xavg_N","xavg_P","xsurf_N_min","xsurf_N_max","xsurf_P_min","xsurf_P_max","ocp_guard","reaction_N_A_m2","reaction_P_A_m2","leak_leftward_A_m2"},
            evaluate(m,"nglobal","EvalGlobal",globalExpr,new String[]{"s","mol/m^2","mol/m^2","mol/m^2","1","1","1","1","1","1","1","A/m^2","A/m^2","A/m^2"},null));
        for(int b:new int[]{1,4}) {
            String mat=b==1?"mat35":"mat54",pce=b==1?"pce1":"pce2";
            String fn=mat+".def.Eeq(liion.socloc_surface)+"+mat+".def.dEeqdT(liion.socloc_surface)*(T_init-298[K])";
            numericTable("preflight_boundary"+b+".csv",new String[]{"time_s","phis_V","phil_V","Eeq_V","eta_V","etamid_V","x_surface","x_particle_average","cs_surface_mol_m3","reaction_input_mol_m3","csmax_mol_m3","direct_Eeq_surface_V","Isx_A_m2"},
                evaluate(m,"point"+b,"EvalPoint",new String[]{"t","phis","phil","liion.Eeq_per1","liion.eta_per1","liion.etamid_per1","liion.socloc_surface","liion.cs_average/liion.csmax","liion.cs_surface","liion."+pce+".per1.minput_concentration","liion.csmax",fn,"liion.Isx"},
                new String[]{"s","V","V","V","V","V","1","1","mol/m^3","mol/m^3","mol/m^3","V","A/m^2"},new int[]{b}));
        }
        for(String type:new String[]{"MinLine","MaxLine"}) numericTable("preflight_"+type+"_ce.csv",new String[]{"time_s","ce_mol_m3"},evaluate(m,type+"ce",type,new String[]{"t","cl"},new String[]{"s","mol/m^3"},new int[]{1,2,3}));
        if(false) {
            numericTable("preflight_cdc.csv",new String[]{"time_s","Icell_A","Ecell_V","CC_CH","CV_CH","CC_DCH","cycle_counter"},
                evaluate(m,"ncdc","EvalGlobal",new String[]{"t","comp1.liion.cdc1.Icell","comp1.liion.cdc1.phis0","comp1.liion.cdc1.CC_CH","comp1.liion.cdc1.CV_CH","comp1.liion.cdc1.CC_DCH","comp1.liion.cdc1.cycle_counter"},new String[]{"s","A","V","1","1","1","1"},null));
            audit(m.component("comp1").physics("liion").feature("cdc1"),"cdc1");
        }
        if(false) {
            // Native function checks at initial stock and the limiting supported charge endpoint.
            String[] xs={"x_Gr_init","(nLi_target-epss_pos*L_pos*cs_NCM_max*0.2228930343076256)/(epss_el*L_el*cs_Gr_max)"};
            for(int k=0;k<xs.length;k++) {
                String xn=xs[k],xp=k==1?"0.2228930343076256":"(nLi_target-epss_el*L_el*cs_Gr_max*("+xn+"))/(epss_pos*L_pos*cs_NCM_max)";
                String en="comp1.mat35.def.Eeq("+xn+")+comp1.mat35.def.dEeqdT("+xn+")*(T_init-298[K])";
                String ep="comp1.mat54.def.Eeq("+xp+")+comp1.mat54.def.dEeqdT("+xp+")*(T_init-298[K])";
                numericTable("preflight_ocv"+k+".csv",new String[]{"time_s","x_N","x_P","Eeq_N_V","Eeq_P_V","OCV_V"},evaluate(m,"nocv"+k,"EvalGlobal",new String[]{"t",xn,xp,en,ep,"("+ep+")-("+en+")"},new String[]{"s","1","1","V","V","V"},null));
            }
        }
        audit(m.component("comp1").physics("liion").feature("pce1").feature("per1"),"pce1_per1");
        audit(m.component("comp1").physics("liion").feature("pce2").feature("per1"),"pce2_per1");
        spatialProfiles(m);
        m.save("axes_generated.java","java");
        System.out.println("PREFLIGHT_EXPORT_OK");
    }

    static Object readSetting(com.comsol.model.PropFeature f,String p) {
        switch(f.getValueType(p)) {
            case "Boolean": return f.getBoolean(p);
            case "BooleanArray": return f.getBooleanArray(p);
            case "BooleanMatrix": return f.getBooleanMatrix(p);
            case "String": return f.getString(p);
            case "StringArray": return f.getStringArray(p);
            case "StringMatrix": return f.getStringMatrix(p);
            case "Int": return f.getInt(p);
            case "IntArray": return f.getIntArray(p);
            case "IntMatrix": return f.getIntMatrix(p);
            case "Double": return f.getDouble(p);
            case "DoubleArray": return f.getDoubleArray(p);
            case "DoubleMatrix": case "DoubleRowMatrix": return f.getDoubleMatrix(p);
            default: throw new IllegalArgumentException(f.getValueType(p));
        }
    }
    static void dumpSettings(com.comsol.model.SolverFeature f,String path) {
        System.out.println("AXES_SOLVER_NODE="+path+"|"+f.getType());
        for(String p:f.properties()) try {
            System.out.println("AXES_SOLVER_PROP="+path+"/"+p+"|"+f.getValueType(p)+"|"+Arrays.deepToString(new Object[]{readSetting(f,p)}));
        } catch(Exception e) { System.out.println("AXES_SOLVER_PROP_UNREAD="+path+"/"+p+"|"+e); }
        for(String child:f.feature().tags()) dumpSettings(f.feature(child),path+"/"+child);
    }
    static void runtimeSettings(Model m,String sol,String time) throws Exception {
        // Read back actual settings before the solve. No settings changed here.
        String[][] settings={
            {"key","actual_value"},
            {"solution_tag",sol},{"time_tag",time},
            {"study_tlist",m.study("std1").feature("time").getString("tlist")},
            {"geometry_length_unit",m.component("comp1").geom("geom1").lengthUnit()},
            {"geometry_dimension",Integer.toString(m.component("comp1").geom("geom1").getSDim())},
            {"rtol",Double.toString(m.sol(sol).feature(time).getDouble("rtol"))},
            {"initialstepbdf",Double.toString(m.sol(sol).feature(time).getDouble("initialstepbdf"))},
            {"initialstepbdfactive",m.sol(sol).feature(time).getString("initialstepbdfactive")},
            {"maxstepconstraintbdf",m.sol(sol).feature(time).getString("maxstepconstraintbdf")},
            {"maxstepexpressionbdf",m.sol(sol).feature(time).getString("maxstepexpressionbdf")},
            {"maxstepbdf",Double.toString(m.sol(sol).feature(time).getDouble("maxstepbdf"))},
            {"tstepsbdf",m.sol(sol).feature(time).getString("tstepsbdf")},
            {"tout",m.sol(sol).feature(time).getString("tout")},
            {"consistent",m.sol(sol).feature(time).getString("consistent")},
            {"atolglobalmethod",m.sol(sol).feature(time).getString("atolglobalmethod")},
            {"atolglobalvaluemethod",m.sol(sol).feature(time).getString("atolglobalvaluemethod")},
            {"atolglobalfactor",Double.toString(m.sol(sol).feature(time).getDouble("atolglobalfactor"))},
            {"atolglobal",Double.toString(m.sol(sol).feature(time).getDouble("atolglobal"))},
            {"eventtol",Double.toString(m.sol(sol).feature(time).getDouble("eventtol"))},
            {"electrolyte_positive_check","SOLVER_MINIMUM_GUARD_PLUS_POSTPROCESSING; step-end sampled only"},
            {"profile_time_interpolation","off; all stored solnum; no t property set"},
            {"profile_spatial_evaluation","domain-selected FE Interp; recover off; ext 0; 241 common coordinates"}
        };
        table("axes_runtime_settings.csv",settings);
        for(String f:m.sol(sol).feature().tags()) if(m.sol(sol).feature(f).getType().equals("Time")||m.sol(sol).feature(f).getType().equals("Variables")) dumpSettings(m.sol(sol).feature(f),sol+"/"+f);
        for(int d=1;d<=3;d++) System.out.println("AXES_PHYSICAL_MESH_DOMAIN="+d+"|numelem="+m.component("comp1").mesh("mesh1").feature("edg1").feature("dis"+d).getString("numelem"));
        for(String pce:new String[]{"pce1","pce2"}) {
            PhysicsFeature pin=m.component("comp1").physics("liion").feature(pce).feature("pin1");
            System.out.println("AXES_PARTICLE="+pce+"|Nel="+pin.getString("Nel")+"|Nord="+pin.getString("Nord")+"|Distribution="+pin.getString("Distribution"));
        }
    }
    static void spatialProfiles(Model m) throws Exception {
        for(String mesh:m.component("comp1").mesh().tags()) {
            System.out.println("AXES_ACTUAL_MESH="+mesh+"|edges="+m.component("comp1").mesh(mesh).getNumElem("edg")+"|vertices="+m.component("comp1").mesh(mesh).getNumVertex());
            System.out.println("AXES_MESH_ELEMENT_DOMAINS="+mesh+"|"+Arrays.toString(m.component("comp1").mesh(mesh).getElemEntity("edg")));
        }
        double ln=m.param().evaluate("L_el"),ls=m.param().evaluate("L_sep"),lp=m.param().evaluate("L_pos");
        double[][] times=evaluate(m,"profiletimes","EvalGlobal",new String[]{"t"},new String[]{"s"},null);
        for(int domain:new int[]{1,3}) {
            String electrode=domain==1?"N":"P",tag="profile"+electrode;
            double start=domain==1?0:ln+ls,length=domain==1?ln:lp;
            double[] coordinates=new double[241];
            for(int j=0;j<coordinates.length;j++) coordinates[j]=start+length*j/240.0;
            coordinates[0]=start; coordinates[240]=start+length;
            m.result().numerical().create(tag,"Interp");
            m.result().numerical(tag).set("data","daudit");
            m.result().numerical(tag).selection().geom("geom1",1);
            m.result().numerical(tag).selection().set(new int[]{domain});
            m.result().numerical(tag).set("coord",new double[][]{coordinates});
            m.result().numerical(tag).set("ext",0.0);
            m.result().numerical(tag).set("recover","off");
            m.result().numerical(tag).set("timeinterp","off");
            m.result().numerical(tag).set("coorderr","on");
            m.result().numerical(tag).set("expr",new String[]{"t","x","liion.socloc_surface","liion.cs_average/liion.csmax","liion.Eeq_per1","liion.etamid_per1","phil","dom"});
            m.result().numerical(tag).set("unit",new String[]{"s","m","1","1","V","V","V","1"});
            System.out.println("AXES_PROFILE_UNIT="+electrode+"|"+m.result().numerical(tag).getValueType("unit")+"|"+Arrays.toString(m.result().numerical(tag).getStringArray("unit")));
            interpSelection(m,tag,times[0].length);interpReadback(m,tag,coordinates,domain);
            String[] profileUnits={"s","m","1","1","V","V","V","1"};units(m,tag,"configured",profileUnits);
            double[][][] data=m.result().numerical(tag).getData();
            interpReadback(m,tag,coordinates,domain);units(m,tag,"evaluated",evaluatedUnits(tag,profileUnits));
            if(data.length!=8 || data[0].length!=times[0].length) throw new IllegalStateException("Profile expression/time shape mismatch "+electrode);
            String[][] rows=new String[times[0].length*coordinates.length+1][8];
            rows[0]=new String[]{"time_s","coordinate_m","x_surface","x_particle_average","Eeq_V","etaMid_V","phil_V","domain_id"};
            for(int ti=0;ti<times[0].length;ti++) {
                for(int e=0;e<8;e++) if(data[e][ti].length!=coordinates.length) throw new IllegalStateException("Profile coordinate shape mismatch "+electrode);
                for(int j=0;j<coordinates.length;j++) {
                    if(data[0][ti][j]!=times[0][ti]) throw new IllegalStateException("Profile time mismatch "+electrode);
                    if(Math.abs(data[1][ti][j]-coordinates[j])>1e-15 || Math.abs(data[7][ti][j]-domain)>1e-9) throw new IllegalStateException("Profile coordinate/domain mismatch "+electrode);
                    for(int e=0;e<8;e++) {
                        if(!Double.isFinite(data[e][ti][j])) throw new IllegalStateException("Nonfinite profile "+electrode+" expression "+e+" time "+ti+" point "+j);
                        rows[1+ti*coordinates.length+j][e]=Double.toString(data[e][ti][j]);
                    }
                }
            }
            table("axes_profile_"+electrode+".csv",rows);
            System.out.println("AXES_PROFILE="+electrode+"|time_count="+times[0].length+"|coordinate_count="+coordinates.length+"|timeinterp=off|FE_spatial_interp=true|domain="+domain);
        }
    }

    public static Model run() throws Exception {
        try {
        stage="model_generation";
        System.out.println("MATERIAL_INPUT_EXPECTED_SHA256=" + LIBRARY_SHA);
        if (!ModelUtil.checkoutLicense("BATTERYDESIGN")) throw new IllegalStateException("Battery checkout failed");
        Model m=ModelUtil.create("Model");
        m.label("Normal480Candidate - fresh common dense time grid, 480 seconds only");
        m.param().set("ce_stop_threshold","0[mol/m^3]");
        String[][] params={
            {"L_el","52[um]"},{"L_sep","25[um]"},{"L_pos","44[um]"},
            {"A_c","1[m^2]"},{"A_cell","1.53938[cm^2]"},
            {"LAM_PE","0.0296398242"},{"LAM_NE","0.0257219788"},{"LLI","0.0439355"},
            {"C_lit0_ref1","0.003765381[A*h]"},{"eps_binder_el","0.1"},
            {"epss_el_0","0.63122"},{"epss_pos_0","0.58803"},
            {"epss_el","epss_el_0*(1-LAM_NE)"},{"epss_pos","epss_pos_0*(1-LAM_PE)"},
            {"epsl_el","1-eps_binder_el-epss_el"},{"epsl_pos","1-eps_binder_el-epss_pos"},{"epsl_sep","0.45"},
            {"epss_short","1-epsl_sep"},{"b_sep","1.5"},{"b_PE_brugg","2.2"},
            {"cs_Gr_max","31507[mol/m^3]"},{"cs_NCM_max","50707.7[mol/m^3]"},
            {"rp_Gr","7.5[um]"},{"rp_NCM","10[um]"},{"D_g","7.1e-15[m^2/s]"},{"D_NCM","1e-13[m^2/s]"},
            {"k_g","2.12e-10[m/s]"},{"k_NCM","9.8e-10[m/s]"},{"K_gr","100[S/m]"},{"K_NCM","0.17[S/m]"},
            {"F_ref","96485.33212[C/mol]"},{"T_init","298.15[K]"},{"c_e_init","1200[mol/m^3]"},
            {"D_e","7.5e-11[m^2/s]"},{"t_plus","0.363"},
            {"x_NCM_0","0.927"},{"x_Gr_0","0.01172068149"},{"x_Gr_init","x_Gr_0"},
            {"nLi_0","epss_pos_0*L_pos*cs_NCM_max*x_NCM_0+epss_el_0*L_el*cs_Gr_max*x_Gr_0"},
            {"dLi_LLI","C_lit0_ref1*LLI/F_ref/A_cell"},{"nLi_target","nLi_0-dLi_LLI"},
            {"x_NCM_init","(nLi_target-epss_el*L_el*cs_Gr_max*x_Gr_init)/(epss_pos*L_pos*cs_NCM_max)"},
            {"x_NCM_max","0.927"},{"x_NCM_min","0.215"},
            {"Q_areal","epss_pos_0*L_pos*cs_NCM_max*(x_NCM_max-x_NCM_min)*F_ref"},
            {"Q_el_proposal","Q_areal/3600[s/h]"},{"i_1C","Q_areal/1[h]"},{"C_rate","0.1"},
            {"i_app","C_rate*i_1C"},{"sigma_short","1e-20[S/m]"}
        };
        for (String[] p:params) m.param().set(p[0],p[1]);
        m.component().create("comp1", true);
        m.component("comp1").geom().create("geom1",1);
        m.component("comp1").geom("geom1").create("i1","Interval");
        m.component("comp1").geom("geom1").feature("i1").set("specify","len");
        m.component("comp1").geom("geom1").feature("i1").set("len",new String[]{"L_el","L_sep","L_pos"});
        m.component("comp1").geom("geom1").run();
        material_mat35(m); material_mat50(m); material_mat54(m);

        // Diagnostic clones: original OCP table numbers are unchanged; prohibit extrapolation.
        m.component("comp1").material("mat35").propertyGroup("def").func("int3").set("extrap","none");
        m.component("comp1").material("mat35").propertyGroup("def").func("int4").set("extrap","none");
        m.component("comp1").material("mat54").propertyGroup("def").func("int1").set("extrap","none");
        m.component("comp1").material("mat54").propertyGroup("def").func("int2").set("extrap","none");
        System.out.println("MATERIALS_REBUILT_FROM_EMBEDDED_PUBLIC_SETTINGS=true");
        String graphite=null,electrolyte=null,nmc=null;
        for (String tag:m.component("comp1").material().tags()) {
            String label=m.component("comp1").material(tag).label();
            System.out.println("MATERIAL="+tag+"|"+label);
            if (label.startsWith("Graphite, LixC6 MCMB")) graphite=tag;
            if (label.startsWith("LiPF6 in 3:7 EC:EMC")) electrolyte=tag;
            if (label.startsWith("NMC 811,")) nmc=tag;
        }
        if (graphite==null || electrolyte==null || nmc==null) throw new IllegalStateException("Expected materials not found");
        m.component("comp1").material(graphite).selection().set(new int[]{1});
        m.component("comp1").material(electrolyte).selection().set(new int[]{2});
        m.component("comp1").material(nmc).selection().set(new int[]{3});
        System.out.println("NMC_LIBRARY_CMAX="+m.component("comp1").material(nmc).propertyGroup("def").getString("csmax"));
        m.component("comp1").material(graphite).propertyGroup("def").set("csmax","cs_Gr_max");
        m.component("comp1").material(nmc).propertyGroup("def").set("csmax","cs_NCM_max");
        m.component("comp1").physics().create("liion","LithiumIonBatteryMPH","geom1");
        m.component("comp1").physics("liion").prop("Ac").set("Ac","A_c");
        m.component("comp1").physics("liion").prop("CellSettings").set("CellSOCandInitialChargeInventory","0");
        // socicd1 is a mandatory default node; CellSettings=0 selects explicit particle initial concentrations.
        m.component("comp1").physics("liion").feature("init1").set("cl","c_e_init");
        electrode(m,"pce1",1,graphite,electrolyte,"epss_el","epsl_el","epsl_el^2.5","K_gr","rp_Gr","D_g","x_Gr_init*cs_Gr_max","k_g");
        electrode(m,"pce2",3,nmc,electrolyte,"epss_pos","epsl_pos","epsl_pos^b_PE_brugg","K_NCM","rp_NCM","D_NCM","x_NCM_init*cs_NCM_max","k_NCM");
        m.component("comp1").physics("liion").create("pcb1","PorousConductiveBinder",1);
        PhysicsFeature binder=m.component("comp1").physics("liion").feature("pcb1");
        binder.selection().set(new int[]{2});
        transport(binder,electrolyte,"epsl_sep","epsl_sep^b_sep");
        binder.set("epss","epss_short");
        binder.set("ElectricCorrModel","NoCorr"); binder.set("sigma_mat","userdef");
        binder.set("sigma",new String[]{"sigma_short","0","0","0","sigma_short","0","0","0","sigma_short"});
        m.component("comp1").physics("liion").create("egnd1","ElectricGround",0);
        m.component("comp1").physics("liion").feature("egnd1").selection().set(new int[]{1});
        m.component("comp1").physics("liion").create("ecd1","ElectrodeNormalCurrentDensity",0);
        m.component("comp1").physics("liion").feature("ecd1").selection().set(new int[]{4});
        m.component("comp1").physics("liion").feature("ecd1").set("nis_type","NormalElectrodeCurrentDensity");
        m.component("comp1").physics("liion").feature("ecd1").set("nis","i_app");

        m.component("comp1").physics("liion").feature("pce1").feature("pin1").set("Nel","320");
        m.component("comp1").physics("liion").feature("pce2").feature("pin1").set("Nel","320");
        for (int domain=1;domain<=3;domain++) {
            String tag="intd"+domain;
            m.component("comp1").cpl().create(tag,"Integration");
            m.component("comp1").cpl(tag).selection().geom("geom1",1);
            m.component("comp1").cpl(tag).selection().set(new int[]{domain});
        }
        m.component("comp1").mesh().create("mesh1");
        m.component("comp1").mesh("mesh1").create("edg1","Edge");
        for (int domain=1;domain<=3;domain++) {
            String dist="dis"+domain;
            m.component("comp1").mesh("mesh1").feature("edg1").create(dist,"Distribution");
            m.component("comp1").mesh("mesh1").feature("edg1").feature(dist).selection().set(new int[]{domain});
            m.component("comp1").mesh("mesh1").feature("edg1").feature(dist).set("numelem",domain==2 ? 60 : 120);
        }
        m.component("comp1").mesh("mesh1").run();
        m.study().create("std1");
        m.study("std1").create("cdi","CurrentDistributionInitialization");
        m.study("std1").create("time","Transient");
        m.study("std1").feature("time").set("tunit","s");
        m.study("std1").feature("time").set("tlist","0 0.0001 0.0002 0.0005 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.11 0.12 0.13 0.14 0.15 0.16 0.17 0.18 0.19 0.2 0.21 0.22 0.23 0.24 0.25 0.26 0.27 0.28 0.29 0.3 0.31 0.32 0.33 0.34 0.35 0.36 0.37 0.38 0.39 0.4 0.41 0.42 0.43 0.44 0.45 0.46 0.47 0.48 0.49 0.5 0.51 0.52 0.53 0.54 0.55 0.56 0.57 0.58 0.59 0.6 0.61 0.62 0.63 0.64 0.65 0.66 0.67 0.68 0.69 0.7 0.71 0.72 0.73 0.74 0.75 0.76 0.77 0.78 0.79 0.8 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.9 0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99 1 1.05 1.1 1.15 1.2 1.25 1.3 1.35 1.4 1.45 1.5 1.55 1.6 1.65 1.7 1.75 1.8 1.85 1.9 1.95 2 2.05 2.1 2.15 2.2 2.25 2.3 2.35 2.4 2.45 2.5 2.55 2.6 2.65 2.7 2.75 2.8 2.85 2.9 2.95 3 3.05 3.1 3.15 3.2 3.25 3.3 3.35 3.4 3.45 3.5 3.55 3.6 3.65 3.7 3.75 3.8 3.85 3.9 3.95 4 4.05 4.1 4.15 4.2 4.25 4.3 4.35 4.4 4.45 4.5 4.55 4.6 4.65 4.7 4.75 4.8 4.85 4.9 4.95 5 5.1 5.2 5.3 5.4 5.5 5.6 5.7 5.8 5.9 6 6.1 6.2 6.3 6.4 6.5 6.6 6.7 6.8 6.9 7 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 7.9 8 8.1 8.2 8.3 8.4 8.5 8.6 8.7 8.8 8.9 9 9.1 9.2 9.3 9.4 9.5 9.6 9.7 9.8 9.9 10 10.1 10.2 10.3 10.4 10.5 10.6 10.7 10.8 10.9 11 11.1 11.2 11.3 11.4 11.5 11.6 11.7 11.8 11.9 12 12.1 12.2 12.3 12.4 12.5 12.6 12.7 12.8 12.9 13 13.1 13.2 13.3 13.4 13.5 13.6 13.7 13.8 13.9 14 14.1 14.2 14.3 14.4 14.5 14.6 14.7 14.8 14.9 15 15.1 15.2 15.3 15.4 15.5 15.6 15.7 15.8 15.9 16 16.1 16.2 16.3 16.4 16.5 16.6 16.7 16.8 16.9 17 17.1 17.2 17.3 17.4 17.5 17.6 17.7 17.8 17.9 18 18.1 18.2 18.3 18.4 18.5 18.6 18.7 18.8 18.9 19 19.1 19.2 19.3 19.4 19.5 19.6 19.7 19.8 19.9 20 20.1 20.2 20.3 20.4 20.5 20.6 20.7 20.8 20.9 21 21.1 21.2 21.3 21.4 21.5 21.6 21.7 21.8 21.9 22 22.1 22.2 22.3 22.4 22.5 22.6 22.7 22.8 22.9 23 23.1 23.2 23.3 23.4 23.5 23.6 23.7 23.8 23.9 24 24.1 24.2 24.3 24.4 24.5 24.6 24.7 24.8 24.9 25 25.1 25.2 25.3 25.4 25.5 25.6 25.7 25.8 25.9 26 26.1 26.2 26.3 26.4 26.5 26.6 26.7 26.8 26.9 27 27.1 27.2 27.3 27.4 27.5 27.6 27.7 27.8 27.9 28 28.1 28.2 28.3 28.4 28.5 28.6 28.7 28.8 28.9 29 29.1 29.2 29.3 29.4 29.5 29.6 29.7 29.8 29.9 30 30.1 30.2 30.3 30.4 30.5 30.6 30.7 30.8 30.9 31 31.1 31.2 31.3 31.4 31.5 31.6 31.7 31.8 31.9 32 32.1 32.2 32.3 32.4 32.5 32.6 32.7 32.8 32.9 33 33.1 33.2 33.3 33.4 33.5 33.6 33.7 33.8 33.9 34 34.1 34.2 34.3 34.4 34.5 34.6 34.7 34.8 34.9 35 35.1 35.2 35.3 35.4 35.5 35.6 35.7 35.8 35.9 36 36.1 36.2 36.3 36.4 36.5 36.6 36.7 36.8 36.9 37 37.1 37.2 37.3 37.4 37.5 37.6 37.7 37.8 37.9 38 38.1 38.2 38.3 38.4 38.5 38.6 38.7 38.8 38.9 39 39.1 39.2 39.3 39.4 39.5 39.6 39.7 39.8 39.9 40 40.1 40.2 40.3 40.4 40.5 40.6 40.7 40.8 40.9 41 41.1 41.2 41.3 41.4 41.5 41.6 41.7 41.8 41.9 42 42.1 42.2 42.3 42.4 42.5 42.6 42.7 42.8 42.9 43 43.1 43.2 43.3 43.4 43.5 43.6 43.7 43.8 43.9 44 44.1 44.2 44.3 44.4 44.5 44.6 44.7 44.8 44.9 45 45.1 45.2 45.3 45.4 45.5 45.6 45.7 45.8 45.9 46 46.1 46.2 46.3 46.4 46.5 46.6 46.7 46.8 46.9 47 47.1 47.2 47.3 47.4 47.5 47.6 47.7 47.8 47.9 48 48.1 48.2 48.3 48.4 48.5 48.6 48.7 48.8 48.9 49 49.1 49.2 49.3 49.4 49.5 49.6 49.7 49.8 49.9 50 50.1 50.2 50.3 50.4 50.5 50.6 50.7 50.8 50.9 51 51.1 51.2 51.3 51.4 51.5 51.6 51.7 51.8 51.9 52 52.1 52.2 52.3 52.4 52.5 52.6 52.7 52.8 52.9 53 53.1 53.2 53.3 53.4 53.5 53.6 53.7 53.8 53.9 54 54.1 54.2 54.3 54.4 54.5 54.6 54.7 54.8 54.9 55 55.1 55.2 55.3 55.4 55.5 55.6 55.7 55.8 55.9 56 56.1 56.2 56.3 56.4 56.5 56.6 56.7 56.8 56.9 57 57.1 57.2 57.3 57.4 57.5 57.6 57.7 57.8 57.9 58 58.1 58.2 58.3 58.4 58.5 58.6 58.7 58.8 58.9 59 59.1 59.2 59.3 59.4 59.5 59.6 59.7 59.8 59.9 60 60.1 60.2 60.3 60.4 60.5 60.6 60.7 60.8 60.9 61 61.1 61.2 61.3 61.4 61.5 61.6 61.7 61.8 61.9 62 62.1 62.2 62.3 62.4 62.5 62.6 62.7 62.8 62.9 63 63.1 63.2 63.3 63.4 63.5 63.6 63.7 63.8 63.9 64 64.1 64.2 64.3 64.4 64.5 64.6 64.7 64.8 64.9 65 65.1 65.2 65.3 65.4 65.5 65.6 65.7 65.8 65.9 66 66.1 66.2 66.3 66.4 66.5 66.6 66.7 66.8 66.9 67 67.1 67.2 67.3 67.4 67.5 67.6 67.7 67.8 67.9 68 68.1 68.2 68.3 68.4 68.5 68.6 68.7 68.8 68.9 69 69.1 69.2 69.3 69.4 69.5 69.6 69.7 69.8 69.9 70 70.1 70.2 70.3 70.4 70.5 70.6 70.7 70.8 70.9 71 71.1 71.2 71.3 71.4 71.5 71.6 71.7 71.8 71.9 72 72.1 72.2 72.3 72.4 72.5 72.6 72.7 72.8 72.9 73 73.1 73.2 73.3 73.4 73.5 73.6 73.7 73.8 73.9 74 74.1 74.2 74.3 74.4 74.5 74.6 74.7 74.8 74.9 75 75.1 75.2 75.3 75.4 75.5 75.6 75.7 75.8 75.9 76 76.1 76.2 76.3 76.4 76.5 76.6 76.7 76.8 76.9 77 77.1 77.2 77.3 77.4 77.5 77.6 77.7 77.8 77.9 78 78.1 78.2 78.3 78.4 78.5 78.6 78.7 78.8 78.9 79 79.1 79.2 79.3 79.4 79.5 79.6 79.7 79.8 79.9 80 80.1 80.2 80.3 80.4 80.5 80.6 80.7 80.8 80.9 81 81.1 81.2 81.3 81.4 81.5 81.6 81.7 81.8 81.9 82 82.1 82.2 82.3 82.4 82.5 82.6 82.7 82.8 82.9 83 83.1 83.2 83.3 83.4 83.5 83.6 83.7 83.8 83.9 84 84.1 84.2 84.3 84.4 84.5 84.6 84.7 84.8 84.9 85 85.1 85.2 85.3 85.4 85.5 85.6 85.7 85.8 85.9 86 86.1 86.2 86.3 86.4 86.5 86.6 86.7 86.8 86.9 87 87.1 87.2 87.3 87.4 87.5 87.6 87.7 87.8 87.9 88 88.1 88.2 88.3 88.4 88.5 88.6 88.7 88.8 88.9 89 89.1 89.2 89.3 89.4 89.5 89.6 89.7 89.8 89.9 90 90.1 90.2 90.3 90.4 90.5 90.6 90.7 90.8 90.9 91 91.1 91.2 91.3 91.4 91.5 91.6 91.7 91.8 91.9 92 92.1 92.2 92.3 92.4 92.5 92.6 92.7 92.8 92.9 93 93.1 93.2 93.3 93.4 93.5 93.6 93.7 93.8 93.9 94 94.1 94.2 94.3 94.4 94.5 94.6 94.7 94.8 94.9 95 95.1 95.2 95.3 95.4 95.5 95.6 95.7 95.8 95.9 96 96.1 96.2 96.3 96.4 96.5 96.6 96.7 96.8 96.9 97 97.1 97.2 97.3 97.4 97.5 97.6 97.7 97.8 97.9 98 98.1 98.2 98.3 98.4 98.5 98.6 98.7 98.8 98.9 99 99.1 99.2 99.3 99.4 99.5 99.6 99.7 99.8 99.9 100 100.1 100.2 100.3 100.4 100.5 100.6 100.7 100.8 100.9 101 101.1 101.2 101.3 101.4 101.5 101.6 101.7 101.8 101.9 102 102.1 102.2 102.3 102.4 102.5 102.6 102.7 102.8 102.9 103 103.1 103.2 103.3 103.4 103.5 103.6 103.7 103.8 103.9 104 104.1 104.2 104.3 104.4 104.5 104.6 104.7 104.8 104.9 105 105.1 105.2 105.3 105.4 105.5 105.6 105.7 105.8 105.9 106 106.1 106.2 106.3 106.4 106.5 106.6 106.7 106.8 106.9 107 107.1 107.2 107.3 107.4 107.5 107.6 107.7 107.8 107.9 108 108.1 108.2 108.3 108.4 108.5 108.6 108.7 108.8 108.9 109 109.1 109.2 109.3 109.4 109.5 109.6 109.7 109.8 109.9 110 110.1 110.2 110.3 110.4 110.5 110.6 110.7 110.8 110.9 111 111.1 111.2 111.3 111.4 111.5 111.6 111.7 111.8 111.9 112 112.1 112.2 112.3 112.4 112.5 112.6 112.7 112.8 112.9 113 113.1 113.2 113.3 113.4 113.5 113.6 113.7 113.8 113.9 114 114.1 114.2 114.3 114.4 114.5 114.6 114.7 114.8 114.9 115 115.1 115.2 115.3 115.4 115.5 115.6 115.7 115.8 115.9 116 116.1 116.2 116.3 116.4 116.5 116.6 116.7 116.8 116.9 117 117.1 117.2 117.3 117.4 117.5 117.6 117.7 117.8 117.9 118 118.1 118.2 118.3 118.4 118.5 118.6 118.7 118.8 118.9 119 119.1 119.2 119.3 119.4 119.5 119.6 119.7 119.8 119.9 120 120.1 120.2 120.3 120.4 120.5 120.6 120.7 120.8 120.9 121 121.1 121.2 121.3 121.4 121.5 121.6 121.7 121.8 121.9 122 122.1 122.2 122.3 122.4 122.5 122.6 122.7 122.8 122.9 123 123.1 123.2 123.3 123.4 123.5 123.6 123.7 123.8 123.9 124 124.1 124.2 124.3 124.4 124.5 124.6 124.7 124.8 124.9 125 125.1 125.2 125.3 125.4 125.5 125.6 125.7 125.8 125.9 126 126.1 126.2 126.3 126.4 126.5 126.6 126.7 126.8 126.9 127 127.1 127.2 127.3 127.4 127.5 127.6 127.7 127.8 127.9 128 128.1 128.2 128.3 128.4 128.5 128.6 128.7 128.8 128.9 129 129.1 129.2 129.3 129.4 129.5 129.6 129.7 129.8 129.9 130 130.1 130.2 130.3 130.4 130.5 130.6 130.7 130.8 130.9 131 131.1 131.2 131.3 131.4 131.5 131.6 131.7 131.8 131.9 132 132.1 132.2 132.3 132.4 132.5 132.6 132.7 132.8 132.9 133 133.1 133.2 133.3 133.4 133.5 133.6 133.7 133.8 133.9 134 134.1 134.2 134.3 134.4 134.5 134.6 134.7 134.8 134.9 135 135.1 135.2 135.3 135.4 135.5 135.6 135.7 135.8 135.9 136 136.1 136.2 136.3 136.4 136.5 136.6 136.7 136.8 136.9 137 137.1 137.2 137.3 137.4 137.5 137.6 137.7 137.8 137.9 138 138.1 138.2 138.3 138.4 138.5 138.6 138.7 138.8 138.9 139 139.1 139.2 139.3 139.4 139.5 139.6 139.7 139.8 139.9 140 140.1 140.2 140.3 140.4 140.5 140.6 140.7 140.8 140.9 141 141.1 141.2 141.3 141.4 141.5 141.6 141.7 141.8 141.9 142 142.1 142.2 142.3 142.4 142.5 142.6 142.7 142.8 142.9 143 143.1 143.2 143.3 143.4 143.5 143.6 143.7 143.8 143.9 144 144.1 144.2 144.3 144.4 144.5 144.6 144.7 144.8 144.9 145 145.1 145.2 145.3 145.4 145.5 145.6 145.7 145.8 145.9 146 146.1 146.2 146.3 146.4 146.5 146.6 146.7 146.8 146.9 147 147.1 147.2 147.3 147.4 147.5 147.6 147.7 147.8 147.9 148 148.1 148.2 148.3 148.4 148.5 148.6 148.7 148.8 148.9 149 149.1 149.2 149.3 149.4 149.5 149.6 149.7 149.8 149.9 150 150.1 150.2 150.3 150.4 150.5 150.6 150.7 150.8 150.9 151 151.1 151.2 151.3 151.4 151.5 151.6 151.7 151.8 151.9 152 152.1 152.2 152.3 152.4 152.5 152.6 152.7 152.8 152.9 153 153.1 153.2 153.3 153.4 153.5 153.6 153.7 153.8 153.9 154 154.1 154.2 154.3 154.4 154.5 154.6 154.7 154.8 154.9 155 155.1 155.2 155.3 155.4 155.5 155.6 155.7 155.8 155.9 156 156.1 156.2 156.3 156.4 156.5 156.6 156.7 156.8 156.9 157 157.1 157.2 157.3 157.4 157.5 157.6 157.7 157.8 157.9 158 158.1 158.2 158.3 158.4 158.5 158.6 158.7 158.8 158.9 159 159.1 159.2 159.3 159.4 159.5 159.6 159.7 159.8 159.9 160 160.1 160.2 160.3 160.4 160.5 160.6 160.7 160.8 160.9 161 161.1 161.2 161.3 161.4 161.5 161.6 161.7 161.8 161.9 162 162.1 162.2 162.3 162.4 162.5 162.6 162.7 162.8 162.9 163 163.1 163.2 163.3 163.4 163.5 163.6 163.7 163.8 163.9 164 164.1 164.2 164.3 164.4 164.5 164.6 164.7 164.8 164.9 165 165.1 165.2 165.3 165.4 165.5 165.6 165.7 165.8 165.9 166 166.1 166.2 166.3 166.4 166.5 166.6 166.7 166.8 166.9 167 167.1 167.2 167.3 167.4 167.5 167.6 167.7 167.8 167.9 168 168.1 168.2 168.3 168.4 168.5 168.6 168.7 168.8 168.9 169 169.1 169.2 169.3 169.4 169.5 169.6 169.7 169.8 169.9 170 170.1 170.2 170.3 170.4 170.5 170.6 170.7 170.8 170.9 171 171.1 171.2 171.3 171.4 171.5 171.6 171.7 171.8 171.9 172 172.1 172.2 172.3 172.4 172.5 172.6 172.7 172.8 172.9 173 173.1 173.2 173.3 173.4 173.5 173.6 173.7 173.8 173.9 174 174.1 174.2 174.3 174.4 174.5 174.6 174.7 174.8 174.9 175 175.1 175.2 175.3 175.4 175.5 175.6 175.7 175.8 175.9 176 176.1 176.2 176.3 176.4 176.5 176.6 176.7 176.8 176.9 177 177.1 177.2 177.3 177.4 177.5 177.6 177.7 177.8 177.9 178 178.1 178.2 178.3 178.4 178.5 178.6 178.7 178.8 178.9 179 179.1 179.2 179.3 179.4 179.5 179.6 179.7 179.8 179.9 180 180.1 180.2 180.3 180.4 180.5 180.6 180.7 180.8 180.9 181 181.1 181.2 181.3 181.4 181.5 181.6 181.7 181.8 181.9 182 182.1 182.2 182.3 182.4 182.5 182.6 182.7 182.8 182.9 183 183.1 183.2 183.3 183.4 183.5 183.6 183.7 183.8 183.9 184 184.1 184.2 184.3 184.4 184.5 184.6 184.7 184.8 184.9 185 185.1 185.2 185.3 185.4 185.5 185.6 185.7 185.8 185.9 186 186.1 186.2 186.3 186.4 186.5 186.6 186.7 186.8 186.9 187 187.1 187.2 187.3 187.4 187.5 187.6 187.7 187.8 187.9 188 188.1 188.2 188.3 188.4 188.5 188.6 188.7 188.8 188.9 189 189.1 189.2 189.3 189.4 189.5 189.6 189.7 189.8 189.9 190 190.1 190.2 190.3 190.4 190.5 190.6 190.7 190.8 190.9 191 191.1 191.2 191.3 191.4 191.5 191.6 191.7 191.8 191.9 192 192.1 192.2 192.3 192.4 192.5 192.6 192.7 192.8 192.9 193 193.1 193.2 193.3 193.4 193.5 193.6 193.7 193.8 193.9 194 194.1 194.2 194.3 194.4 194.5 194.6 194.7 194.8 194.9 195 195.1 195.2 195.3 195.4 195.5 195.6 195.7 195.8 195.9 196 196.1 196.2 196.3 196.4 196.5 196.6 196.7 196.8 196.9 197 197.1 197.2 197.3 197.4 197.5 197.6 197.7 197.8 197.9 198 198.1 198.2 198.3 198.4 198.5 198.6 198.7 198.8 198.9 199 199.1 199.2 199.3 199.4 199.5 199.6 199.7 199.8 199.9 200 200.1 200.2 200.3 200.4 200.5 200.6 200.7 200.8 200.9 201 201.1 201.2 201.3 201.4 201.5 201.6 201.7 201.8 201.9 202 202.1 202.2 202.3 202.4 202.5 202.6 202.7 202.8 202.9 203 203.1 203.2 203.3 203.4 203.5 203.6 203.7 203.8 203.9 204 204.1 204.2 204.3 204.4 204.5 204.6 204.7 204.8 204.9 205 205.1 205.2 205.3 205.4 205.5 205.6 205.7 205.8 205.9 206 206.1 206.2 206.3 206.4 206.5 206.6 206.7 206.8 206.9 207 207.1 207.2 207.3 207.4 207.5 207.6 207.7 207.8 207.9 208 208.1 208.2 208.3 208.4 208.5 208.6 208.7 208.8 208.9 209 209.1 209.2 209.3 209.4 209.5 209.6 209.7 209.8 209.9 210 210.1 210.2 210.3 210.4 210.5 210.6 210.7 210.8 210.9 211 211.1 211.2 211.3 211.4 211.5 211.6 211.7 211.8 211.9 212 212.1 212.2 212.3 212.4 212.5 212.6 212.7 212.8 212.9 213 213.1 213.2 213.3 213.4 213.5 213.6 213.7 213.8 213.9 214 214.1 214.2 214.3 214.4 214.5 214.6 214.7 214.8 214.9 215 215.1 215.2 215.3 215.4 215.5 215.6 215.7 215.8 215.9 216 216.1 216.2 216.3 216.4 216.5 216.6 216.7 216.8 216.9 217 217.1 217.2 217.3 217.4 217.5 217.6 217.7 217.8 217.9 218 218.1 218.2 218.3 218.4 218.5 218.6 218.7 218.8 218.9 219 219.1 219.2 219.3 219.4 219.5 219.6 219.7 219.8 219.9 220 220.1 220.2 220.3 220.4 220.5 220.6 220.7 220.8 220.9 221 221.1 221.2 221.3 221.4 221.5 221.6 221.7 221.8 221.9 222 222.1 222.2 222.3 222.4 222.5 222.6 222.7 222.8 222.9 223 223.1 223.2 223.3 223.4 223.5 223.6 223.7 223.8 223.9 224 224.1 224.2 224.3 224.4 224.5 224.6 224.7 224.8 224.9 225 225.1 225.2 225.3 225.4 225.5 225.6 225.7 225.8 225.9 226 226.1 226.2 226.3 226.4 226.5 226.6 226.7 226.8 226.9 227 227.1 227.2 227.3 227.4 227.5 227.6 227.7 227.8 227.9 228 228.1 228.2 228.3 228.4 228.5 228.6 228.7 228.8 228.9 229 229.1 229.2 229.3 229.4 229.5 229.6 229.7 229.8 229.9 230 230.1 230.2 230.3 230.4 230.5 230.6 230.7 230.8 230.9 231 231.1 231.2 231.3 231.4 231.5 231.6 231.7 231.8 231.9 232 232.1 232.2 232.3 232.4 232.5 232.6 232.7 232.8 232.9 233 233.1 233.2 233.3 233.4 233.5 233.6 233.7 233.8 233.9 234 234.1 234.2 234.3 234.4 234.5 234.6 234.7 234.8 234.9 235 235.1 235.2 235.3 235.4 235.5 235.6 235.7 235.8 235.9 236 236.1 236.2 236.3 236.4 236.5 236.6 236.7 236.8 236.9 237 237.1 237.2 237.3 237.4 237.5 237.6 237.7 237.8 237.9 238 238.1 238.2 238.3 238.4 238.5 238.6 238.7 238.8 238.9 239 239.1 239.2 239.3 239.4 239.5 239.6 239.7 239.8 239.9 240 240.1 240.2 240.3 240.4 240.5 240.6 240.7 240.8 240.9 241 241.1 241.2 241.3 241.4 241.5 241.6 241.7 241.8 241.9 242 242.1 242.2 242.3 242.4 242.5 242.6 242.7 242.8 242.9 243 243.1 243.2 243.3 243.4 243.5 243.6 243.7 243.8 243.9 244 244.1 244.2 244.3 244.4 244.5 244.6 244.7 244.8 244.9 245 245.1 245.2 245.3 245.4 245.5 245.6 245.7 245.8 245.9 246 246.1 246.2 246.3 246.4 246.5 246.6 246.7 246.8 246.9 247 247.1 247.2 247.3 247.4 247.5 247.6 247.7 247.8 247.9 248 248.1 248.2 248.3 248.4 248.5 248.6 248.7 248.8 248.9 249 249.1 249.2 249.3 249.4 249.5 249.6 249.7 249.8 249.9 250 250.1 250.2 250.3 250.4 250.5 250.6 250.7 250.8 250.9 251 251.1 251.2 251.3 251.4 251.5 251.6 251.7 251.8 251.9 252 252.1 252.2 252.3 252.4 252.5 252.6 252.7 252.8 252.9 253 253.1 253.2 253.3 253.4 253.5 253.6 253.7 253.8 253.9 254 254.1 254.2 254.3 254.4 254.5 254.6 254.7 254.8 254.9 255 255.1 255.2 255.3 255.4 255.5 255.6 255.7 255.8 255.9 256 256.1 256.2 256.3 256.4 256.5 256.6 256.7 256.8 256.9 257 257.1 257.2 257.3 257.4 257.5 257.6 257.7 257.8 257.9 258 258.1 258.2 258.3 258.4 258.5 258.6 258.7 258.8 258.9 259 259.1 259.2 259.3 259.4 259.5 259.6 259.7 259.8 259.9 260 260.1 260.2 260.3 260.4 260.5 260.6 260.7 260.8 260.9 261 261.1 261.2 261.3 261.4 261.5 261.6 261.7 261.8 261.9 262 262.1 262.2 262.3 262.4 262.5 262.6 262.7 262.8 262.9 263 263.1 263.2 263.3 263.4 263.5 263.6 263.7 263.8 263.9 264 264.1 264.2 264.3 264.4 264.5 264.6 264.7 264.8 264.9 265 265.1 265.2 265.3 265.4 265.5 265.6 265.7 265.8 265.9 266 266.1 266.2 266.3 266.4 266.5 266.6 266.7 266.8 266.9 267 267.1 267.2 267.3 267.4 267.5 267.6 267.7 267.8 267.9 268 268.1 268.2 268.3 268.4 268.5 268.6 268.7 268.8 268.9 269 269.1 269.2 269.3 269.4 269.5 269.6 269.7 269.8 269.9 270 270.1 270.2 270.3 270.4 270.5 270.6 270.7 270.8 270.9 271 271.1 271.2 271.3 271.4 271.5 271.6 271.7 271.8 271.9 272 272.1 272.2 272.3 272.4 272.5 272.6 272.7 272.8 272.9 273 273.1 273.2 273.3 273.4 273.5 273.6 273.7 273.8 273.9 274 274.1 274.2 274.3 274.4 274.5 274.6 274.7 274.8 274.9 275 275.1 275.2 275.3 275.4 275.5 275.6 275.7 275.8 275.9 276 276.1 276.2 276.3 276.4 276.5 276.6 276.7 276.8 276.9 277 277.1 277.2 277.3 277.4 277.5 277.6 277.7 277.8 277.9 278 278.1 278.2 278.3 278.4 278.5 278.6 278.7 278.8 278.9 279 279.1 279.2 279.3 279.4 279.5 279.6 279.7 279.8 279.9 280 280.1 280.2 280.3 280.4 280.5 280.6 280.7 280.8 280.9 281 281.1 281.2 281.3 281.4 281.5 281.6 281.7 281.8 281.9 282 282.1 282.2 282.3 282.4 282.5 282.6 282.7 282.8 282.9 283 283.1 283.2 283.3 283.4 283.5 283.6 283.7 283.8 283.9 284 284.1 284.2 284.3 284.4 284.5 284.6 284.7 284.8 284.9 285 285.1 285.2 285.3 285.4 285.5 285.6 285.7 285.8 285.9 286 286.1 286.2 286.3 286.4 286.5 286.6 286.7 286.8 286.9 287 287.1 287.2 287.3 287.4 287.5 287.6 287.7 287.8 287.9 288 288.1 288.2 288.3 288.4 288.5 288.6 288.7 288.8 288.9 289 289.1 289.2 289.3 289.4 289.5 289.6 289.7 289.8 289.9 290 290.1 290.2 290.3 290.4 290.5 290.6 290.7 290.8 290.9 291 291.1 291.2 291.3 291.4 291.5 291.6 291.7 291.8 291.9 292 292.1 292.2 292.3 292.4 292.5 292.6 292.7 292.8 292.9 293 293.1 293.2 293.3 293.4 293.5 293.6 293.7 293.8 293.9 294 294.1 294.2 294.3 294.4 294.5 294.6 294.7 294.8 294.9 295 295.1 295.2 295.3 295.4 295.5 295.6 295.7 295.8 295.9 296 296.1 296.2 296.3 296.4 296.5 296.6 296.7 296.8 296.9 297 297.1 297.2 297.3 297.4 297.5 297.6 297.7 297.8 297.9 298 298.1 298.2 298.3 298.4 298.5 298.6 298.7 298.8 298.9 299 299.1 299.2 299.3 299.4 299.5 299.6 299.7 299.8 299.9 300 300.1 300.2 300.3 300.4 300.5 300.6 300.7 300.8 300.9 301 301.1 301.2 301.3 301.4 301.5 301.6 301.7 301.8 301.9 302 302.1 302.2 302.3 302.4 302.5 302.6 302.7 302.8 302.9 303 303.1 303.2 303.3 303.4 303.5 303.6 303.7 303.8 303.9 304 304.1 304.2 304.3 304.4 304.5 304.6 304.7 304.8 304.9 305 305.1 305.2 305.3 305.4 305.5 305.6 305.7 305.8 305.9 306 306.1 306.2 306.3 306.4 306.5 306.6 306.7 306.8 306.9 307 307.1 307.2 307.3 307.4 307.5 307.6 307.7 307.8 307.9 308 308.1 308.2 308.3 308.4 308.5 308.6 308.7 308.8 308.9 309 309.1 309.2 309.3 309.4 309.5 309.6 309.7 309.8 309.9 310 310.1 310.2 310.3 310.4 310.5 310.6 310.7 310.8 310.9 311 311.1 311.2 311.3 311.4 311.5 311.6 311.7 311.8 311.9 312 312.1 312.2 312.3 312.4 312.5 312.6 312.7 312.8 312.9 313 313.1 313.2 313.3 313.4 313.5 313.6 313.7 313.8 313.9 314 314.1 314.2 314.3 314.4 314.5 314.6 314.7 314.8 314.9 315 315.1 315.2 315.3 315.4 315.5 315.6 315.7 315.8 315.9 316 316.1 316.2 316.3 316.4 316.5 316.6 316.7 316.8 316.9 317 317.1 317.2 317.3 317.4 317.5 317.6 317.7 317.8 317.9 318 318.1 318.2 318.3 318.4 318.5 318.6 318.7 318.8 318.9 319 319.1 319.2 319.3 319.4 319.5 319.6 319.7 319.8 319.9 320 320.1 320.2 320.3 320.4 320.5 320.6 320.7 320.8 320.9 321 321.1 321.2 321.3 321.4 321.5 321.6 321.7 321.8 321.9 322 322.1 322.2 322.3 322.4 322.5 322.6 322.7 322.8 322.9 323 323.1 323.2 323.3 323.4 323.5 323.6 323.7 323.8 323.9 324 324.1 324.2 324.3 324.4 324.5 324.6 324.7 324.8 324.9 325 325.1 325.2 325.3 325.4 325.5 325.6 325.7 325.8 325.9 326 326.1 326.2 326.3 326.4 326.5 326.6 326.7 326.8 326.9 327 327.1 327.2 327.3 327.4 327.5 327.6 327.7 327.8 327.9 328 328.1 328.2 328.3 328.4 328.5 328.6 328.7 328.8 328.9 329 329.1 329.2 329.3 329.4 329.5 329.6 329.7 329.8 329.9 330 330.1 330.2 330.3 330.4 330.5 330.6 330.7 330.8 330.9 331 331.1 331.2 331.3 331.4 331.5 331.6 331.7 331.8 331.9 332 332.1 332.2 332.3 332.4 332.5 332.6 332.7 332.8 332.9 333 333.1 333.2 333.3 333.4 333.5 333.6 333.7 333.8 333.9 334 334.1 334.2 334.3 334.4 334.5 334.6 334.7 334.8 334.9 335 335.1 335.2 335.3 335.4 335.5 335.6 335.7 335.8 335.9 336 336.1 336.2 336.3 336.4 336.5 336.6 336.7 336.8 336.9 337 337.1 337.2 337.3 337.4 337.5 337.6 337.7 337.8 337.9 338 338.1 338.2 338.3 338.4 338.5 338.6 338.7 338.8 338.9 339 339.1 339.2 339.3 339.4 339.5 339.6 339.7 339.8 339.9 340 340.1 340.2 340.3 340.4 340.5 340.6 340.7 340.8 340.9 341 341.1 341.2 341.3 341.4 341.5 341.6 341.7 341.8 341.9 342 342.1 342.2 342.3 342.4 342.5 342.6 342.7 342.8 342.9 343 343.1 343.2 343.3 343.4 343.5 343.6 343.7 343.8 343.9 344 344.1 344.2 344.3 344.4 344.5 344.6 344.7 344.8 344.9 345 345.1 345.2 345.3 345.4 345.5 345.6 345.7 345.8 345.9 346 346.1 346.2 346.3 346.4 346.5 346.6 346.7 346.8 346.9 347 347.1 347.2 347.3 347.4 347.5 347.6 347.7 347.8 347.9 348 348.1 348.2 348.3 348.4 348.5 348.6 348.7 348.8 348.9 349 349.1 349.2 349.3 349.4 349.5 349.6 349.7 349.8 349.9 350 350.1 350.2 350.3 350.4 350.5 350.6 350.7 350.8 350.9 351 351.1 351.2 351.3 351.4 351.5 351.6 351.7 351.8 351.9 352 352.1 352.2 352.3 352.4 352.5 352.6 352.7 352.8 352.9 353 353.1 353.2 353.3 353.4 353.5 353.6 353.7 353.8 353.9 354 354.1 354.2 354.3 354.4 354.5 354.6 354.7 354.8 354.9 355 355.1 355.2 355.3 355.4 355.5 355.6 355.7 355.8 355.9 356 356.1 356.2 356.3 356.4 356.5 356.6 356.7 356.8 356.9 357 357.1 357.2 357.3 357.4 357.5 357.6 357.7 357.8 357.9 358 358.1 358.2 358.3 358.4 358.5 358.6 358.7 358.8 358.9 359 359.1 359.2 359.3 359.4 359.5 359.6 359.7 359.8 359.9 360 360.1 360.2 360.3 360.4 360.5 360.6 360.7 360.8 360.9 361 361.1 361.2 361.3 361.4 361.5 361.6 361.7 361.8 361.9 362 362.1 362.2 362.3 362.4 362.5 362.6 362.7 362.8 362.9 363 363.1 363.2 363.3 363.4 363.5 363.6 363.7 363.8 363.9 364 364.1 364.2 364.3 364.4 364.5 364.6 364.7 364.8 364.9 365 365.1 365.2 365.3 365.4 365.5 365.6 365.7 365.8 365.9 366 366.1 366.2 366.3 366.4 366.5 366.6 366.7 366.8 366.9 367 367.1 367.2 367.3 367.4 367.5 367.6 367.7 367.8 367.9 368 368.1 368.2 368.3 368.4 368.5 368.6 368.7 368.8 368.9 369 369.1 369.2 369.3 369.4 369.5 369.6 369.7 369.8 369.9 370 370.1 370.2 370.3 370.4 370.5 370.6 370.7 370.8 370.9 371 371.1 371.2 371.3 371.4 371.5 371.6 371.7 371.8 371.9 372 372.1 372.2 372.3 372.4 372.5 372.6 372.7 372.8 372.9 373 373.1 373.2 373.3 373.4 373.5 373.6 373.7 373.8 373.9 374 374.1 374.2 374.3 374.4 374.5 374.6 374.7 374.8 374.9 375 375.1 375.2 375.3 375.4 375.5 375.6 375.7 375.8 375.9 376 376.1 376.2 376.3 376.4 376.5 376.6 376.7 376.8 376.9 377 377.1 377.2 377.3 377.4 377.5 377.6 377.7 377.8 377.9 378 378.1 378.2 378.3 378.4 378.5 378.6 378.7 378.8 378.9 379 379.1 379.2 379.3 379.4 379.5 379.6 379.7 379.8 379.9 380 380.1 380.2 380.3 380.4 380.5 380.6 380.7 380.8 380.9 381 381.1 381.2 381.3 381.4 381.5 381.6 381.7 381.8 381.9 382 382.1 382.2 382.3 382.4 382.5 382.6 382.7 382.8 382.9 383 383.1 383.2 383.3 383.4 383.5 383.6 383.7 383.8 383.9 384 384.1 384.2 384.3 384.4 384.5 384.6 384.7 384.8 384.9 385 385.1 385.2 385.3 385.4 385.5 385.6 385.7 385.8 385.9 386 386.1 386.2 386.3 386.4 386.5 386.6 386.7 386.8 386.9 387 387.1 387.2 387.3 387.4 387.5 387.6 387.7 387.8 387.9 388 388.1 388.2 388.3 388.4 388.5 388.6 388.7 388.8 388.9 389 389.1 389.2 389.3 389.4 389.5 389.6 389.7 389.8 389.9 390 390.1 390.2 390.3 390.4 390.5 390.6 390.7 390.8 390.9 391 391.1 391.2 391.3 391.4 391.5 391.6 391.7 391.8 391.9 392 392.1 392.2 392.3 392.4 392.5 392.6 392.7 392.8 392.9 393 393.1 393.2 393.3 393.4 393.5 393.6 393.7 393.8 393.9 394 394.1 394.2 394.3 394.4 394.5 394.6 394.7 394.8 394.9 395 395.1 395.2 395.3 395.4 395.5 395.6 395.7 395.8 395.9 396 396.1 396.2 396.3 396.4 396.5 396.6 396.7 396.8 396.9 397 397.1 397.2 397.3 397.4 397.5 397.6 397.7 397.8 397.9 398 398.1 398.2 398.3 398.4 398.5 398.6 398.7 398.8 398.9 399 399.1 399.2 399.3 399.4 399.5 399.6 399.7 399.8 399.9 400 400.1 400.2 400.3 400.4 400.5 400.6 400.7 400.8 400.9 401 401.1 401.2 401.3 401.4 401.5 401.6 401.7 401.8 401.9 402 402.1 402.2 402.3 402.4 402.5 402.6 402.7 402.8 402.9 403 403.1 403.2 403.3 403.4 403.5 403.6 403.7 403.8 403.9 404 404.1 404.2 404.3 404.4 404.5 404.6 404.7 404.8 404.9 405 405.1 405.2 405.3 405.4 405.5 405.6 405.7 405.8 405.9 406 406.1 406.2 406.3 406.4 406.5 406.6 406.7 406.8 406.9 407 407.1 407.2 407.3 407.4 407.5 407.6 407.7 407.8 407.9 408 408.1 408.2 408.3 408.4 408.5 408.6 408.7 408.8 408.9 409 409.1 409.2 409.3 409.4 409.5 409.6 409.7 409.8 409.9 410 410.1 410.2 410.3 410.4 410.5 410.6 410.7 410.8 410.9 411 411.1 411.2 411.3 411.4 411.5 411.6 411.7 411.8 411.9 412 412.1 412.2 412.3 412.4 412.5 412.6 412.7 412.8 412.9 413 413.1 413.2 413.3 413.4 413.5 413.6 413.7 413.8 413.9 414 414.1 414.2 414.3 414.4 414.5 414.6 414.7 414.8 414.9 415 415.1 415.2 415.3 415.4 415.5 415.6 415.7 415.8 415.9 416 416.1 416.2 416.3 416.4 416.5 416.6 416.7 416.8 416.9 417 417.1 417.2 417.3 417.4 417.5 417.6 417.7 417.8 417.9 418 418.1 418.2 418.3 418.4 418.5 418.6 418.7 418.8 418.9 419 419.1 419.2 419.3 419.4 419.5 419.6 419.7 419.8 419.9 420 420.1 420.2 420.3 420.4 420.5 420.6 420.7 420.8 420.9 421 421.1 421.2 421.3 421.4 421.5 421.6 421.7 421.8 421.9 422 422.1 422.2 422.3 422.4 422.5 422.6 422.7 422.8 422.9 423 423.1 423.2 423.3 423.4 423.5 423.6 423.7 423.8 423.9 424 424.1 424.2 424.3 424.4 424.5 424.6 424.7 424.8 424.9 425 425.1 425.2 425.3 425.4 425.5 425.6 425.7 425.8 425.9 426 426.1 426.2 426.3 426.4 426.5 426.6 426.7 426.8 426.9 427 427.1 427.2 427.3 427.4 427.5 427.6 427.7 427.8 427.9 428 428.1 428.2 428.3 428.4 428.5 428.6 428.7 428.8 428.9 429 429.1 429.2 429.3 429.4 429.5 429.6 429.7 429.8 429.9 430 430.1 430.2 430.3 430.4 430.5 430.6 430.7 430.8 430.9 431 431.1 431.2 431.3 431.4 431.5 431.6 431.7 431.8 431.9 432 432.1 432.2 432.3 432.4 432.5 432.6 432.7 432.8 432.9 433 433.1 433.2 433.3 433.4 433.5 433.6 433.7 433.8 433.9 434 434.1 434.2 434.3 434.4 434.5 434.6 434.7 434.8 434.9 435 435.1 435.2 435.3 435.4 435.5 435.6 435.7 435.8 435.9 436 436.1 436.2 436.3 436.4 436.5 436.6 436.7 436.8 436.9 437 437.1 437.2 437.3 437.4 437.5 437.6 437.7 437.8 437.9 438 438.1 438.2 438.3 438.4 438.5 438.6 438.7 438.8 438.9 439 439.1 439.2 439.3 439.4 439.5 439.6 439.7 439.8 439.9 440 440.1 440.2 440.3 440.4 440.5 440.6 440.7 440.8 440.9 441 441.1 441.2 441.3 441.4 441.5 441.6 441.7 441.8 441.9 442 442.1 442.2 442.3 442.4 442.5 442.6 442.7 442.8 442.9 443 443.1 443.2 443.3 443.4 443.5 443.6 443.7 443.8 443.9 444 444.1 444.2 444.3 444.4 444.5 444.6 444.7 444.8 444.9 445 445.1 445.2 445.3 445.4 445.5 445.6 445.7 445.8 445.9 446 446.1 446.2 446.3 446.4 446.5 446.6 446.7 446.8 446.9 447 447.1 447.2 447.3 447.4 447.5 447.6 447.7 447.8 447.9 448 448.1 448.2 448.3 448.4 448.5 448.6 448.7 448.8 448.9 449 449.1 449.2 449.3 449.4 449.5 449.6 449.7 449.8 449.9 450 450.1 450.2 450.3 450.4 450.5 450.6 450.7 450.8 450.9 451 451.1 451.2 451.3 451.4 451.5 451.6 451.7 451.8 451.9 452 452.1 452.2 452.3 452.4 452.5 452.6 452.7 452.8 452.9 453 453.1 453.2 453.3 453.4 453.5 453.6 453.7 453.8 453.9 454 454.1 454.2 454.3 454.4 454.5 454.6 454.7 454.8 454.9 455 455.1 455.2 455.3 455.4 455.5 455.6 455.7 455.8 455.9 456 456.1 456.2 456.3 456.4 456.5 456.6 456.7 456.8 456.9 457 457.1 457.2 457.3 457.4 457.5 457.6 457.7 457.8 457.9 458 458.1 458.2 458.3 458.4 458.5 458.6 458.7 458.8 458.9 459 459.1 459.2 459.3 459.4 459.5 459.6 459.7 459.8 459.9 460 460.1 460.2 460.3 460.4 460.5 460.6 460.7 460.8 460.9 461 461.1 461.2 461.3 461.4 461.5 461.6 461.7 461.8 461.9 462 462.1 462.2 462.3 462.4 462.5 462.6 462.7 462.8 462.9 463 463.1 463.2 463.3 463.4 463.5 463.6 463.7 463.8 463.9 464 464.1 464.2 464.3 464.4 464.5 464.6 464.7 464.8 464.9 465 465.1 465.2 465.3 465.4 465.5 465.6 465.7 465.8 465.9 466 466.1 466.2 466.3 466.4 466.5 466.6 466.7 466.8 466.9 467 467.1 467.2 467.3 467.4 467.5 467.6 467.7 467.8 467.9 468 468.1 468.2 468.3 468.4 468.5 468.6 468.7 468.8 468.9 469 469.1 469.2 469.3 469.4 469.5 469.6 469.7 469.8 469.9 470 470.1 470.2 470.3 470.4 470.5 470.6 470.7 470.8 470.9 471 471.1 471.2 471.3 471.4 471.5 471.6 471.7 471.8 471.9 472 472.1 472.2 472.3 472.4 472.5 472.6 472.7 472.8 472.9 473 473.1 473.2 473.3 473.4 473.5 473.6 473.7 473.8 473.9 474 474.1 474.2 474.3 474.4 474.5 474.6 474.7 474.8 474.9 475 475.1 475.2 475.3 475.4 475.5 475.6 475.7 475.8 475.9 476 476.1 476.2 476.3 476.4 476.5 476.6 476.7 476.8 476.9 477 477.1 477.2 477.3 477.4 477.5 477.6 477.7 477.8 477.9 478 478.1 478.2 478.3 478.4 478.5 478.6 478.7 478.8 478.9 479 479.1 479.2 479.3 479.4 479.5 479.6 479.7 479.8 479.9 480");
        m.study("std1").feature("time").set("rtol","1e-5");
        for (String name:new String[]{"epss_el","epss_pos","epss_short","nLi_target","x_NCM_init","Q_areal","Q_el_proposal","i_1C","A_c"})
            System.out.println("PARAM="+name+"|"+m.param().evaluate(name)+"|"+m.param().evaluateUnit(name));
        preflightAudit(m);
        stage="complete";System.out.println("NORMAL480_PRODUCER_COMPLETE");
        return m;
        } catch(Exception primary) {
            try {table("producer_failure.csv",new String[][]{{"stage","type","message"},{stage,primary.getClass().getName(),primary.toString()}});}
            catch(Exception reporting) {primary.addSuppressed(reporting);}
            primary.printStackTrace(System.err);throw primary;
        }
    }
}
