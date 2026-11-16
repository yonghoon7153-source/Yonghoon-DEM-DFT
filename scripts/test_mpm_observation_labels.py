"""Text/diagnostic changes only; never imports the MPM solver."""
import ast,contextlib,hashlib,io,json,os,unittest
from pathlib import Path
ROOT=Path(os.environ.get('MPM_OBSERVATION_ROOT',Path(__file__).resolve().parents[1]))
FILES=('viz_mpm_morphology.py','mpm2d_morphology.py','mpm3d_compaction.py')
def source(name):return (ROOT/'scripts'/name).read_text(encoding='utf8')
def signature(text):
    class Normalize(ast.NodeTransformer):
        def visit_Constant(self,node):return ast.Constant(value='<TEXT>') if isinstance(node.value,str) else node
        def visit_Assign(self,node):
            if any(isinstance(t,ast.Name) and t.id.startswith('_por_') and t.id.endswith('_obs') for t in node.targets):return None
            return self.generic_visit(node)
        def visit_If(self,node):
            if isinstance(node.test,ast.Name) and node.test.id=='_por_clipped_obs':return None
            return self.generic_visit(node)
        def visit_Expr(self,node):
            if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='print':return None
            return self.generic_visit(node)
    tree=Normalize().visit(ast.parse(text));return hashlib.sha256(ast.dump(tree,include_attributes=False).encode()).hexdigest()
def keys(text):
    out=[]
    for n in ast.walk(ast.parse(text)):
        if isinstance(n,ast.Dict):out.extend(k.value for k in n.keys if isinstance(k,ast.Constant) and isinstance(k.value,str))
        if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and isinstance(n.slice.value,str):out.append(n.slice.value)
    return hashlib.sha256(json.dumps(out).encode()).hexdigest()
class Observations(unittest.TestCase):
    def test_01_viz_names(self):
        s=source(FILES[0]);self.assertIn("'cumulative deformation ∫‖D‖dt'",s);self.assertIn("'cumulative plastic correction Σdg'",s)
        self.assertNotIn('total strain ε (vs seed)',s)
    def test_02_two_dimensional_name(self):
        s=source(FILES[1]);self.assertIn('SE cumulative plastic correction Σdg',s);self.assertNotIn('accumulated plastic strain Σdg',s)
    def test_03_restart_memory_statement(self):
        s=source(FILES[2]);self.assertNotIn('pristine/no memory',s);self.assertIn('elastic reference; x and accumulated history retained',s)
    def test_04_clipping_observation_preserves_reported_float(self):
        tree=ast.parse(source(FILES[2]));nodes=[]
        for n in ast.walk(tree):
            if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('por','_por_raw_pct_obs','_por_clipped_obs') for t in n.targets):nodes.append(n)
            if isinstance(n,ast.If) and isinstance(n.test,ast.Name) and n.test.id=='_por_clipped_obs':nodes.append(n)
        # Select the one original frame por assignment and the three adjacent diagnostics.
        nodes=sorted(nodes,key=lambda n:n.lineno)
        self.assertEqual(len(nodes),4,'missing or duplicate observation statements')
        code=compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'diagnostic','exec')
        for solid in (0.0,0.5,1.0,1.0000000000000002,1.25,2.0):
            ns=dict(solid_vol=solid,area=1.,height=1.,frame=17);log=io.StringIO()
            with contextlib.redirect_stdout(log):exec(code,ns)
            expected=max(0.,1.-solid/(1.*1.))*100.
            self.assertEqual(ns['por'].hex(),expected.hex());self.assertEqual(ns['_por_clipped_obs'],solid>1)
            if solid>1:
                self.assertIn('clipped=True',log.getvalue());self.assertIn(format((1.-solid)*100.,'.17g'),log.getvalue())
            else:self.assertEqual(log.getvalue(),'')
    def test_05_calculation_ast_unchanged(self):
        baseline=json.loads((ROOT/'docs/reviews/mpm_observation_labels_20261116/baseline_contract.json').read_bytes())
        for f in FILES:
            with self.subTest(file=f):self.assertEqual(signature(source(f)),baseline[f]['calculation_ast'])
    def test_06_existing_output_keys_unchanged(self):
        baseline=json.loads((ROOT/'docs/reviews/mpm_observation_labels_20261116/baseline_contract.json').read_bytes())
        for f in FILES:
            with self.subTest(file=f):self.assertEqual(keys(source(f)),baseline[f]['dict_and_subscript_keys'])
    def test_07_am_panel_denominator(self):
        s=source(FILES[0]);self.assertGreaterEqual(s.count('raster area: AM'),3)
        self.assertIn('without --scaffold, AM geometry is not represented',s)
        self.assertIn("am_f = 100.0 * ((lab == 1) | (lab == 2)).mean()",s)
    def test_08_web_explanation_matches(self):
        s=(ROOT/'webapp/static/explain/mpm_basics_20261116.html').read_text(encoding='utf8')
        q=s[s.index('id="q23"'):s.index('id="q27"')]
        self.assertIn('cumulative deformation',q);self.assertIn('cumulative plastic correction',q)
        self.assertNotIn('고칠 것',q);self.assertNotIn('scripts/ 동결이 풀린 뒤',q)
        self.assertIn('래스터 면적',q);self.assertIn('--scaffold',q);self.assertIn('raw_pct',q)
        self.assertNotIn('그 단면의 물질점 장부',q)
if __name__=='__main__':unittest.main()
