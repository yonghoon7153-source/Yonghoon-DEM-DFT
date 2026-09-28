import java.util.*;
public class GuardHarness {
static double[] TIMES=null;static String stage="fixture";static boolean reportFail=false;
static void table(String name,String[][] rows)throws Exception {if(reportFail)throw new IllegalStateException("REPORT_FAILURE");}
static class Sel {int dim=1;int[] ids={1};void geom(String g,int d){dim=d;}void set(int[] a){ids=a;}int dim(){return dim;}int[] entities(int d){return ids;}}
static class Model {
 Map<String,Object> p=new HashMap<>();Sel sel=new Sel();boolean evaluated=false,badBoolean=false,badUnits=false,differentSecond=false;int calls=0;
 Model result(){return this;}Model numerical(){return this;}Model numerical(String t){p.put("tag",t);return this;}void create(String t,String type){p.put("tag",t);evaluated=false;calls=0;if(type.equals("EvalPoint"))sel.dim=0;}
 Sel selection(){return sel;}void set(String k,Object v){p.put(k,v);if(k.equals("unit"))evaluated=false;}
 String getString(String k){return (String)p.get(k);}int[] getIntArray(String k){return (int[])p.get(k);}double[] getDoubleArray(String k){return (double[])p.get(k);}double[][] getDoubleMatrix(String k){return (double[][])p.get(k);}double getDouble(String k){return ((Number)p.get(k)).doubleValue();}
 String[] getStringArray(String k){if(!k.equals("unit"))return (String[])p.get(k);if(badUnits)return new String[]{"BAD"};String[] u=(String[])p.get("unit");if(u==null)u=new String[]{"s","mol/m^3","mol/m^3","mol/m^3","mol/m^3","mol/m^3","1","1","1"};return evaluated?evaluatedUnits((String)p.get("tag"),u):u;}
 double[][] getReal(){evaluated=true;calls++;double[][] a=new double[9][3];a[0]=new double[]{0,.0001,.0002};for(int i=1;i<6;i++)a[i]=new double[]{1200,1199,1197};a[6]=new double[]{0,0,badBoolean?2:1};if(differentSecond&&calls==2)a[1][2]++;return a;}
}
interface Run {void go()throws Exception;}
static void need(boolean v,String m){if(!v)throw new AssertionError(m);}
static void negative(String reason,Run r)throws Exception{try{r.go();}catch(IllegalStateException e){need(e.getMessage().contains(reason),e.toString());return;}throw new AssertionError("EXPECTED:"+reason);}
    static void checkShape(String tag,double[][] values,int count) {
        if(values==null||values.length!=count||count==0||values[0]==null||values[0].length==0)throw new IllegalStateException("SHAPE:"+tag);
        int n=values[0].length;
        for(double[] row:values){if(row==null||row.length!=n)throw new IllegalStateException("RAGGED:"+tag);for(double v:row)if(!Double.isFinite(v))throw new IllegalStateException("NONFINITE:"+tag);}
        if(values[0][0]!=0.0)throw new IllegalStateException("TIME_ORIGIN:"+tag);
        for(int i=0;i<n;i++)if(values[0][i]<0||values[0][i]>5||(i>0&&values[0][i]<=values[0][i-1]))throw new IllegalStateException("TIME_ORDER:"+tag);
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
static void catchProbe(Exception e)throws Exception {try{throw e;} catch(Exception primary) {
            try {table("producer_failure.csv",new String[][]{{"stage","type","message"},{stage,primary.getClass().getName(),primary.toString()}});}
            catch(Exception reporting) {primary.addSuppressed(reporting);}
            primary.printStackTrace(System.err);throw primary;
        } }
public static void main(String[] args)throws Exception {
 TIMES=null;checkShape("ok",new double[][]{{0,.0001,.0002},{1,2,3}},2);numericTable("ok.csv",new String[]{"t","v"},new double[][]{{0,.0001,.0002},{1,2,3}});System.out.println("J01|PASS");
 negative("RAGGED",()->checkShape("bad",new double[][]{{0,.0001},{1}},2));negative("NONFINITE",()->checkShape("bad",new double[][]{{0,.0001},{1,Double.NaN}},2));negative("EXACT_TIMES",()->checkShape("bad",new double[][]{{0,.0001},{1,2}},2));System.out.println("J02|PASS");
 String[] u={"s","m","1","1","V","V","V","1"};need(evaluatedUnits("profileN",u)[7].equals("")&&u[7].equals("1"),"UNIT_MUTATION");Model m=new Model();m.p.put("unit",u);units(m,"profileN","configured",u);m.badUnits=true;negative("UNIT",()->units(m,"profileN","configured",u));System.out.println("J03|PASS");
 TIMES=null;electrolyteEvidence(new Model(),"ocp","surface");Model wrong=new Model();wrong.badBoolean=true;negative("GUARD_BOOLEAN",()->electrolyteEvidence(wrong,"ocp","surface"));Model changed=new Model();changed.differentSecond=true;negative("GUARD_UNIT_VALUES",()->electrolyteEvidence(changed,"ocp","surface"));System.out.println("J04|PASS");
 Model ip=new Model();interpSelection(ip,"profileN",3);need(Arrays.equals(ip.getIntArray("solnum"),new int[]{1,2,3}),"SOLNUM");double[] co={0,1};ip.set("data","daudit");ip.set("recover","off");ip.set("coorderr","on");ip.set("ext",0.0);ip.set("coord",new double[][]{co});interpReadback(ip,"profileN",co,1);ip.set("timeinterp","on");negative("INTERP_MODE",()->interpReadback(ip,"profileN",co,1));System.out.println("J05|PASS");
 Exception primary=new IllegalStateException("PRIMARY");reportFail=true;try{catchProbe(primary);}catch(Exception got){need(got==primary&&got.getSuppressed().length==1&&got.getSuppressed()[0].getMessage().equals("REPORT_FAILURE"),"PRIMARY_PRESERVATION");}System.out.println("J06|PASS");
}
}
