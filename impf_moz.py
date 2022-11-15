from climada.entity.impact_funcs import ImpactFunc, ImpactFuncSet
import numpy as np

class ImpFuncsCIFloodMoz():

    def __init__(self):
        self.tag = 'FL'
        self.road = self.step_impf()
        self.power_line = self.step_impf()
        self.power_plant = self.step_impf()
        self.health_level1 = self.health_level_1_impf()
        self.health_level_2_4 = self.health_level_2_4_impf()

    def health_level_1_impf(self):
        step_impf = ImpactFunc()
        step_impf.id = 1
        step_impf.haz_type = 'FL'
        step_impf.name = 'Step function flood'
        step_impf.intensity_unit = ''
        step_impf.intensity = np.array([0, 1])
        step_impf.mdd = np.array([0, 0.81])
        step_impf.paa = np.sort(np.linspace(1, 1, num=2))
        step_impf.check()
        return step_impf

    def health_level_2_4_impf(self):
        step_impf = ImpactFunc()
        step_impf.id = 2
        step_impf.haz_type = 'FL'
        step_impf.name = 'Step function flood'
        step_impf.intensity_unit = ''
        step_impf.intensity = np.array([0, 1])
        step_impf.mdd = np.array([0, 0.65])
        step_impf.paa = np.sort(np.linspace(1, 1, num=2))
        step_impf.check()
        return step_impf

    def step_impf(self):
        step_impf = ImpactFunc()
        step_impf.id = 1
        step_impf.haz_type = 'FL'
        step_impf.name = 'Step function flood'
        step_impf.intensity_unit = ''
        step_impf.intensity = np.array([0, 0.95, 0.955, 1])
        step_impf.mdd = np.array([0, 0, 1, 1])
        step_impf.paa = np.sort(np.linspace(1, 1, num=4))
        step_impf.check()
        return step_impf


class ImpFuncsCIWindMoz():

    def __init__(self):
        self.tag = 'TC'
        self.road = self.road_impf()
        self.power_line = self.pl_impf()
        self.power_plant = self.no_impf()
        self.people = self.people_impf()
        self.health = self.health_level_2_4_impf()

    def health_level_1_4_impf(self):
        impf_health_1_4 = ImpactFunc()
        impf_health_1_4.id = 2
        impf_health_1_4.haz_type = 'FL'
        impf_health_1_4.name = 'Step function flood'
        impf_health_1_4.intensity_unit = 'm/s'
        impf_health_1_4.intensity = np.array([12, 18, 20, 40, 50, 60, 70, 90])
        impf_health_1_4.mdd = np.array([0, 0.03, 0.3, 0.5, 0.6, 0.61, 0.61, 0.61])
        impf_health_1_4.paa = np.ones(impf_health_1_4.intensity.shape)
        impf_health_1_4.check()
        return impf_health_1_4

    def road_impf(self):
        # Road adapted from Koks et al. 2019 (tree blowdown on road > 42 m/s)
        impf_road = ImpactFunc()
        impf_road.id = 2
        impf_road.haz_type = 'TC'
        impf_road.name = 'Loss func. for roads from tree blowdown'
        impf_road.intensity_unit = 'm/s'
        # impf_road.intensity = np.array([0, 30, 35, 42, 48, 120])
        impf_road.intensity = np.array([0, 20, 30, 40, 50, 120])
        impf_road.mdd = np.array([0, 0, 0, 50, 100, 100]) / 100
        impf_road.paa = np.sort(np.linspace(1, 1, num=6))
        impf_road.check()
        return impf_road

    def p_fail_pl(self, v_eval, v_crit=30, v_coll=60):
        """
        adapted from  https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7801854
        and Vulnerability Assessment for Power Transmission Lines under Typhoon
        Weather Based on a Cascading Failure State Transition Diagram
        """
        p_fail = []
        for v in v_eval:
            p = 0
            if (v > v_crit) & (v < v_coll):
                p = np.exp(0.6931 * (v - v_crit) / v_crit) - 1
            elif v > v_coll:
                p = 1
            p_fail.append(p)
        return p_fail

    def pl_impf(self, v_crit=30, v_coll=60):
        # Power line
        v_eval = np.linspace(0, 120, num=120)
        p_fail_powerlines = self.p_fail_pl(v_eval, v_crit=v_crit, v_coll=v_coll)
        impf_prob = ImpactFunc()
        impf_prob.id = 1
        impf_prob.tag = 'PL_Prob'
        impf_prob.haz_type = 'TC'
        impf_prob.name = 'power line failure prob'
        impf_prob.intensity_unit = 'm/s'
        impf_prob.intensity = np.array(v_eval)
        impf_prob.mdd = np.array(p_fail_powerlines)
        impf_prob.paa = np.sort(np.linspace(1, 1, num=120))
        impf_prob.check()
        return impf_prob

    def people_impf(self):
        # Mapping of wind field >= hurricane scale 1 (33 m/s)
        impf_ppl = ImpactFunc()
        impf_ppl.id = 7
        impf_ppl.haz_type = 'TC'
        impf_ppl.name = 'People - Windfield Mapping >= TC'
        impf_ppl.intensity_unit = 'm/s'
        impf_ppl.intensity = np.array([0, 32, 33, 80, 100, 120, 140, 160])
        impf_ppl.mdd = np.array([0, 0, 100, 100, 100, 100, 100, 100]) / 100
        impf_ppl.paa = np.sort(np.linspace(1, 1, num=8))
        impf_ppl.check()
        return impf_ppl