**COMSOL 6.3 — 동일 좌표의 전극 표면 프로파일과 설정 기록 API**

2026-09-13. 설치 공식 문서·completion XML과 공개 6.3 문서를 읽어 확인했다. 아래 코드는 실행하지 않았다. 이번 독립 조사에서는 COMSOL 실행·원본 모델 열기·기존 소스/설정 변경을 하지 않았다. 적용 범위는 0.1C, sigma=1e-20 S/m, 5초의 새 300/40·300/80·600/40 진단이다.

**선택: 전극별 Numerical Interp**

`Interp`는 Solution dataset에서 선택한 domain의 유한요소 해를 임의 좌표에서 평가한다. 좌표는 `double[spaceDimension][point]`, 결과 `getData()`는 `double[expression][solutionIndex][point]`이다. `solnum` 기본값은 모든 저장 해다. `t`를 지정하지 않고 `timeinterp=off`로 기록하면 별도 시간 보간을 요청하지 않는다. Source: [Interp 6.3](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_results.52.075.html), [NumericalFeature 반환형](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/api/com/comsol/model/NumericalFeature.html).

웹 속성 표의 `unit:String`와 달리 설치 `C:/Program Files/COMSOL/COMSOL63/Multiphysics/data/completion/numerical.xml`은 Interp의 `unit:StringArray`, `timeinterp:String` 기본 `off`, `solnum:IntArray`, `t:DoubleArray`를 명시한다. 런타임 `getValueType("unit")`와 값도 함께 기록한다. `innerinput`은 이 API 전용 노드의 설치 속성 목록에 없으므로 사용하지 않는다.

Solution dataset은 `edim`을 무시하고 selection 차원으로 평가 위치를 정한다. 따라서 `selection().geom("geom1",1)`와 domain 1 또는 3 선택이 핵심이다. 각 전극 241개 좌표를 별도의 노드/CSV에 넣는다. 총 물리 격자 300에서는 전극별 120 요소, 600에서는 240 요소이므로 이 좌표는 300의 요소 중간점과 600의 vertex를 함께 포함한다. 이를 **공통 좌표의 공간 FE 보간**으로 표기하며 모든 점을 모든 격자의 원래 절점이라고 부르지 않는다.

```java
// daudit must already refer to the solved Solution dataset.
double ln=m.param().evaluate("L_el"), ls=m.param().evaluate("L_sep");
double lp=m.param().evaluate("L_pos");
System.out.println("GEOMETRY_LENGTH_UNIT="+
    m.component("comp1").geom("geom1").lengthUnit());
System.out.println("GEOMETRY_SPACE_DIM="+
    m.component("comp1").geom("geom1").getSDim());

for (int domain : new int[]{1,3}) {
    double left=domain==1 ? 0 : ln+ls;
    double right=domain==1 ? ln : ln+ls+lp;
    double[] xp=new double[241];
    for(int j=0;j<xp.length;j++) xp[j]=left+(right-left)*j/240.0;
    xp[0]=left; xp[240]=right;
    String tag="surfaceProfile"+domain;
    m.result().numerical().create(tag,"Interp");
    com.comsol.model.NumericalFeature n=m.result().numerical(tag);
    n.set("data","daudit");
    n.selection().geom("geom1",1);
    n.selection().set(new int[]{domain});
    n.set("coord",new double[][]{xp});
    n.set("ext",0.0);
    n.set("recover","off");
    n.set("coorderr","on");
    n.set("matherr","on");
    n.set("timeinterp","off");
    // Do not set t. solnum remains its all-solutions default.
    n.set("expr",new String[]{"t","x","liion.socloc_surface",
        "liion.cs_average/liion.csmax","liion.Eeq_per1",
        "liion.etamid_per1","phil","dom"});
    n.set("unit",new String[]{"s","m","1","1","V","V","V","1"});
    System.out.println(tag+" UNIT_TYPE="+n.getValueType("unit")+
        " UNIT="+java.util.Arrays.toString(n.getStringArray("unit")));
    double[][][] v=n.getData();
    // v[0][s][j]=time_s, v[1][s][j]=coordinate_m.
    // Export v[0..6][s][j] to this domain's CSV. v[7] checks the domain.
    if(v.length!=8 || v[0].length==0) throw new IllegalStateException("Profile shape");
    for(int e=0;e<8;e++) {
        if(v[e].length!=v[0].length) throw new IllegalStateException("Profile time shape");
        for(int s=0;s<v[e].length;s++) {
            if(v[e][s].length!=241) throw new IllegalStateException("Profile point shape");
            for(int j=0;j<241;j++)
                if(!Double.isFinite(v[e][s][j])) throw new IllegalStateException("Profile nonfinite");
        }
    }
    for(int s=0;s<v[0].length;s++) for(int j=0;j<241;j++) {
        if(Math.abs(v[1][s][j]-xp[j])>1e-12)
            throw new IllegalStateException("Profile coordinate mismatch");
        if(Math.abs(v[7][s][j]-domain)>1e-9)
            throw new IllegalStateException("Profile domain mismatch");
        if(Math.abs(v[0][s][j]-v[0][s][0])>1e-12)
            throw new IllegalStateException("Profile time mismatch");
    }
}
```

CSV列 순서는 `time_s,coordinate_m,x_surface,x_particle_average,Eeq_V,etaMid_V,phil_V`이며 domain은 파일명/metadata로 구분한다. 정렬은 저장 해 index 우선, 좌표 index 차순이다. `dom`은 내부 검증용 여덟 번째 식이며 요청 CSV에는 기록하지 않아도 된다. `getCoordinates()`도 제공되지만 내보내기 좌표는 단위를 m로 명시한 `x` 식을 사용하여 단위·순서를 검증한다. Geometry getter의 공식 근거는 [GeomSequence](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/api/com/comsol/model/GeomSequence.html)와 상속된 [GeomInfo](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/api/com/comsol/model/GeomInfo.html)이다.

경계 좌표에서는 domain 선택을 유지하여 separator 쪽과 합치지 않는다. 위 `dom`, finite, 좌표 검사가 실패하면 기록을 미완으로 취급하고 좌표를 몰래 이동하거나 domain을 합쳐 평균하지 않는다. `coorderr=on`은 모든 점이 밖일 때의 오류를 보장하므로 개별 값 검사가 여전히 필요하다. 출력 시간은 실제 저장된 global/collector CSV 및 요청 dense 공통 시각과 대조하여 누락·보간·순서 혼동을 검출한다.

**대안과 배열 주의사항**

API `Eval`도 domain별 `getData()/getCoordinates()`를 제공한다. 사용한다면 `pattern=lagrange`, `refine=1`, `smooth=none`, `recover=off`를 명시하고 반환 좌표와 element index를 함께 검사한다. 중복 element vertex를 임의로 평균해서는 안 된다. [Eval API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_results.52.047.html).

`CutPoint1D`는 `method=coords`, `pointx:StringArray`, `snapping=none`, `data=Solution dataset`으로 가능하다. 그러나 `EvalPoint.getReal()`는 API 전용 3차원 배열과 다르며 다점·다식 배열을 별도로 해석해야 한다. 여기서는 좌표·해 번호 배열 계약과 domain 선택이 더 직접적인 Interp를 사용한다. [CutPoint1D API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_results.52.039.html), [수치 결과 취득](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_results.52.007.html).

**솔버·격자 실제 설정을 읽는 공개 API**

Time과 Variables 및 그 자식에 아래 `dumpTree`를 적용한다. 자동 생성 tag `t1/v1`를 가정하지 말고 `getType()`을 확인한다. 타입 표와 completion이 다를 수 있으므로 `getValueType`를 우선한다. `READ_ERROR`는 해당 설정의 미확인 기록이다. [PropFeature](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/api/com/comsol/model/PropFeature.html), [SolverFeature](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/api/com/comsol/model/SolverFeature.html).

```java
static Object readValue(com.comsol.model.PropFeature f,String p) {
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
static void dumpProps(com.comsol.model.PropFeature f,String path) {
    for(String p:f.properties()) try {
        System.out.println(path+"/"+p+" type="+f.getValueType(p)+" value="+
            java.util.Arrays.deepToString(new Object[]{readValue(f,p)}));
    } catch(Exception e) { System.out.println(path+"/"+p+" READ_ERROR="+e); }
}
static void dumpTree(com.comsol.model.SolverFeature f,String path) {
    System.out.println(path+" type="+f.getType());
    dumpProps(f,path);
    for(String child:f.feature().tags()) dumpTree(f.feature(child),path+"/"+child);
}
```

Time의 `atol*`, `rtol`, BDF step 설정을 기록하고, Variables/Field/State의 `scalemethod`, `scaleval`, `resscalemethod`, `resscaleval`도 기록한다. `auto/parent`일 때 저장 scaleval은 실제 런타임 자동 scale의 증거가 아니므로 native solver 로그를 함께 남긴다. [Time](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.50.html), [Variables](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.56.html).

```java
for(String mt:m.mesh().tags()) {
    com.comsol.model.MeshSequence ms=m.mesh(mt);
    System.out.println("MESH="+mt+" EDGES="+ms.getNumElem("edg")+
        " VERTICES="+ms.getNumVertex());
    System.out.println("MESH_ENTITY="+mt+" "+
        java.util.Arrays.toString(ms.getElemEntity("edg")));
}
for(String pe:new String[]{"pce1","pce2"})
    dumpProps(m.component("comp1").physics("liion").feature(pe).feature("pin1"),pe+"/pin1");
```

`getNumElem("edg")`는 실제 1D 선요소 수이며 `getElemEntity("edg")`는 요소별 domain mapping이다. 0D 경계 요소를 포함할 수 있는 전체 개수와 구별한다. pin1의 `Nel/Nord/Distribution/ParticleConcentrationType/FastAssembly`는 설정값이고 실제 radial mesh 개수와 별도로 기록한다. 이전 모델에서 extra-dimension mesh tag는 `liion_pce1_pin1_xdim`, `liion_pce2_pin1_xdim`이었으나 새 모델은 열거 결과로 확인한다. [MeshSequence](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/api/com/comsol/model/MeshSequence.html). `Nel/Distribution/Nord`의 설치 필드는 `data/completion/physics.xml:20557`에 있다.
