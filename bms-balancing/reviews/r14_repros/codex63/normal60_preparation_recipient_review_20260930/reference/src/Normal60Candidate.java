import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;
import com.comsol.model.physics.PhysicsFeature;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;

/** 6.3-native bounded validation. Current distribution initialization and a 60-second transient only.
 * Material literals: current public settings extracted from hashed installed library.
 * The running Java performs no external file reads.
 * Input hash is checked by the submitting MCP client before and after the job.
 * Output: audit tables through stdout, COMSOL-exported Java, and worker-saved MPH.
 */
public class Normal60Candidate {
    static final String LIBRARY = "C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/inputs/battery_lib_63.mph";
    static final String LIBRARY_SHA = "92cfd07d16fcb148ab1de4adbf48a3b9c6f709c2b8f04d9c571e4d702c4473f6";

    static double[] TIMES=null;
    static String stage="entry";
    static void checkShape(String tag,double[][] values,int count) {
        if(values==null||values.length!=count||count==0||values[0]==null||values[0].length==0)throw new IllegalStateException("SHAPE:"+tag);
        int n=values[0].length;
        for(double[] row:values){if(row==null||row.length!=n)throw new IllegalStateException("RAGGED:"+tag);for(double v:row)if(!Double.isFinite(v))throw new IllegalStateException("NONFINITE:"+tag);}
        if(values[0][0]!=0.0)throw new IllegalStateException("TIME_ORIGIN:"+tag);
        for(int i=0;i<n;i++)if(values[0][i]<0||values[0][i]>60||(i>0&&values[0][i]<=values[0][i-1]))throw new IllegalStateException("TIME_ORDER:"+tag);
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
        System.out.println("PREFLIGHT_SOLVE_BEGIN=0..60 seconds; NO full protocol or sweep");
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
        m.label("Normal60Candidate - fresh common dense time grid, 60 seconds only");
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
        m.study("std1").feature("time").set("tlist","0 0.0001 0.0002 0.0005 0.001 0.002 0.005 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.11 0.12 0.13 0.14 0.15 0.16 0.17 0.18 0.19 0.2 0.21 0.22 0.23 0.24 0.25 0.26 0.27 0.28 0.29 0.3 0.31 0.32 0.33 0.34 0.35 0.36 0.37 0.38 0.39 0.4 0.41 0.42 0.43 0.44 0.45 0.46 0.47 0.48 0.49 0.5 0.51 0.52 0.53 0.54 0.55 0.56 0.57 0.58 0.59 0.6 0.61 0.62 0.63 0.64 0.65 0.66 0.67 0.68 0.69 0.7 0.71 0.72 0.73 0.74 0.75 0.76 0.77 0.78 0.79 0.8 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.9 0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99 1 1.05 1.1 1.15 1.2 1.25 1.3 1.35 1.4 1.45 1.5 1.55 1.6 1.65 1.7 1.75 1.8 1.85 1.9 1.95 2 2.05 2.1 2.15 2.2 2.25 2.3 2.35 2.4 2.45 2.5 2.55 2.6 2.65 2.7 2.75 2.8 2.85 2.9 2.95 3 3.05 3.1 3.15 3.2 3.25 3.3 3.35 3.4 3.45 3.5 3.55 3.6 3.65 3.7 3.75 3.8 3.85 3.9 3.95 4 4.05 4.1 4.15 4.2 4.25 4.3 4.35 4.4 4.45 4.5 4.55 4.6 4.65 4.7 4.75 4.8 4.85 4.9 4.95 5 5.1 5.2 5.3 5.4 5.5 5.6 5.7 5.8 5.9 6 6.1 6.2 6.3 6.4 6.5 6.6 6.7 6.8 6.9 7 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 7.9 8 8.1 8.2 8.3 8.4 8.5 8.6 8.7 8.8 8.9 9 9.1 9.2 9.3 9.4 9.5 9.6 9.7 9.8 9.9 10 10.1 10.2 10.3 10.4 10.5 10.6 10.7 10.8 10.9 11 11.1 11.2 11.3 11.4 11.5 11.6 11.7 11.8 11.9 12 12.1 12.2 12.3 12.4 12.5 12.6 12.7 12.8 12.9 13 13.1 13.2 13.3 13.4 13.5 13.6 13.7 13.8 13.9 14 14.1 14.2 14.3 14.4 14.5 14.6 14.7 14.8 14.9 15 15.1 15.2 15.3 15.4 15.5 15.6 15.7 15.8 15.9 16 16.1 16.2 16.3 16.4 16.5 16.6 16.7 16.8 16.9 17 17.1 17.2 17.3 17.4 17.5 17.6 17.7 17.8 17.9 18 18.1 18.2 18.3 18.4 18.5 18.6 18.7 18.8 18.9 19 19.1 19.2 19.3 19.4 19.5 19.6 19.7 19.8 19.9 20 20.1 20.2 20.3 20.4 20.5 20.6 20.7 20.8 20.9 21 21.1 21.2 21.3 21.4 21.5 21.6 21.7 21.8 21.9 22 22.1 22.2 22.3 22.4 22.5 22.6 22.7 22.8 22.9 23 23.1 23.2 23.3 23.4 23.5 23.6 23.7 23.8 23.9 24 24.1 24.2 24.3 24.4 24.5 24.6 24.7 24.8 24.9 25 25.1 25.2 25.3 25.4 25.5 25.6 25.7 25.8 25.9 26 26.1 26.2 26.3 26.4 26.5 26.6 26.7 26.8 26.9 27 27.1 27.2 27.3 27.4 27.5 27.6 27.7 27.8 27.9 28 28.1 28.2 28.3 28.4 28.5 28.6 28.7 28.8 28.9 29 29.1 29.2 29.3 29.4 29.5 29.6 29.7 29.8 29.9 30 30.1 30.2 30.3 30.4 30.5 30.6 30.7 30.8 30.9 31 31.1 31.2 31.3 31.4 31.5 31.6 31.7 31.8 31.9 32 32.1 32.2 32.3 32.4 32.5 32.6 32.7 32.8 32.9 33 33.1 33.2 33.3 33.4 33.5 33.6 33.7 33.8 33.9 34 34.1 34.2 34.3 34.4 34.5 34.6 34.7 34.8 34.9 35 35.1 35.2 35.3 35.4 35.5 35.6 35.7 35.8 35.9 36 36.1 36.2 36.3 36.4 36.5 36.6 36.7 36.8 36.9 37 37.1 37.2 37.3 37.4 37.5 37.6 37.7 37.8 37.9 38 38.1 38.2 38.3 38.4 38.5 38.6 38.7 38.8 38.9 39 39.1 39.2 39.3 39.4 39.5 39.6 39.7 39.8 39.9 40 40.1 40.2 40.3 40.4 40.5 40.6 40.7 40.8 40.9 41 41.1 41.2 41.3 41.4 41.5 41.6 41.7 41.8 41.9 42 42.1 42.2 42.3 42.4 42.5 42.6 42.7 42.8 42.9 43 43.1 43.2 43.3 43.4 43.5 43.6 43.7 43.8 43.9 44 44.1 44.2 44.3 44.4 44.5 44.6 44.7 44.8 44.9 45 45.1 45.2 45.3 45.4 45.5 45.6 45.7 45.8 45.9 46 46.1 46.2 46.3 46.4 46.5 46.6 46.7 46.8 46.9 47 47.1 47.2 47.3 47.4 47.5 47.6 47.7 47.8 47.9 48 48.1 48.2 48.3 48.4 48.5 48.6 48.7 48.8 48.9 49 49.1 49.2 49.3 49.4 49.5 49.6 49.7 49.8 49.9 50 50.1 50.2 50.3 50.4 50.5 50.6 50.7 50.8 50.9 51 51.1 51.2 51.3 51.4 51.5 51.6 51.7 51.8 51.9 52 52.1 52.2 52.3 52.4 52.5 52.6 52.7 52.8 52.9 53 53.1 53.2 53.3 53.4 53.5 53.6 53.7 53.8 53.9 54 54.1 54.2 54.3 54.4 54.5 54.6 54.7 54.8 54.9 55 55.1 55.2 55.3 55.4 55.5 55.6 55.7 55.8 55.9 56 56.1 56.2 56.3 56.4 56.5 56.6 56.7 56.8 56.9 57 57.1 57.2 57.3 57.4 57.5 57.6 57.7 57.8 57.9 58 58.1 58.2 58.3 58.4 58.5 58.6 58.7 58.8 58.9 59 59.1 59.2 59.3 59.4 59.5 59.6 59.7 59.8 59.9 60");
        m.study("std1").feature("time").set("rtol","1e-5");
        for (String name:new String[]{"epss_el","epss_pos","epss_short","nLi_target","x_NCM_init","Q_areal","Q_el_proposal","i_1C","A_c"})
            System.out.println("PARAM="+name+"|"+m.param().evaluate(name)+"|"+m.param().evaluateUnit(name));
        preflightAudit(m);
        stage="complete";System.out.println("NORMAL60_PRODUCER_COMPLETE");
        return m;
        } catch(Exception primary) {
            try {table("producer_failure.csv",new String[][]{{"stage","type","message"},{stage,primary.getClass().getName(),primary.toString()}});}
            catch(Exception reporting) {primary.addSuppressed(reporting);}
            primary.printStackTrace(System.err);throw primary;
        }
    }
}
