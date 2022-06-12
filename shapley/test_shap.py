import unittest

# from x_shapley import x_shapley
from shapley import shapley

class test_shapley(unittest.TestCase):
    # shap = shapley()
    def setUp(self):
        self.shap = shapley()
        

    def tearDown(self):
        pass
    
    def test_contain_str(self):
        st1 = ["a"]
        st2 = ["a","b","c"]
        self.assertEqual(self.shap.contain_str(st1,st2) , True)
        st1 = ["a1"]
        st2 = ["a1","a2","a3"]
        self.assertEqual(self.shap.contain_str(st1,st2) , True)
        st1 = ["a4"]
        st2 = ["a1","a2","a3"]
        self.assertEqual(self.shap.contain_str(st1,st2) , False)
        st1 = ["a1","b1"]
        st2 = ["a1","b2"]
        self.assertEqual(self.shap.contain_str(st1,st2) , False)
        st1 = ["Alice","Bob","Chen"]
        st2 = ["Alice","Bob"]
        self.assertEqual(self.shap.contain_str(st1,st2) , False)
        st2 = ["Alice","Bob","Chen"]
        st1 = ["Alice","Bob"]
        self.assertEqual(self.shap.contain_str(st1,st2) , True)

    def test_fix_abc(self):
        
        abc = {"": 0,"a1": 0,"b1": 0,"c1": 100,"a1b1": 300,"a1c1": 200,"b1c1": 100,"a1b1c1": 500}
        agents = ["a1","b1","c1"]
        res = self.shap.fix_abc(abc, agents)
        res_true = {'': 0, 'a1': 0, 'b1': 0, 'c1': 100, 'a1b1': 300, 'a1c1': 200, 'b1c1': 100, 'a1b1c1': 500}
        self.assertEqual(res , res_true)
        abc = {"": 0,"a1": 1}
        agents = ["a1"]
        res = self.shap.fix_abc(abc, agents)
        res_true = {'': 0, 'a1': 1}
        self.assertEqual(res , res_true)
        abc = {"": 0,"a": 100,"b": 150,"c": 250,"ba": 200,"ca": 250,"bc": 300,"cab": 370}
        agents = ["a", "b", "c"]
        res = self.shap.fix_abc(abc, agents)
        res_true = {'': 0, 'a': 100, 'b': 150, 'c': 250, 'ab': 200, 'ac': 250, 'bc': 300, 'abc': 370}
        self.assertEqual(res , res_true)
        abc = {"": 0,"a": 100,"b": 150,"c": 250,"ba": 200,"ca": 250,"bc": 300,"cab": 370}
        agents = ["b", "a", "c"]
        res = self.shap.fix_abc(abc, agents)
        res_true = {'': 0, 'b': 150, 'a': 100, 'c': 250, 'ba': 200, 'bc': 300, 'ac': 250, 'bac': 370}
        self.assertEqual(res , res_true)
        abc = {"ChenAlice": 250,"BobAlice": 200,"Alice": 100, "": 0,"Bob": 150,"ChenBobAlice": 370,"Chen": 250,"BobChen": 300}
        agents = ["Alice", "Bob", "Chen"]
        res = self.shap.fix_abc(abc, agents)
        res_true = {'': 0, 'Alice': 100, 'Bob': 150, 'Chen': 250, 'AliceBob': 200, 'AliceChen': 250, 'BobChen': 300, 'AliceBobChen': 370}
        self.assertEqual(res , res_true)

    def test_get_cost_from_permo(self):
        abc = {"": 0,"a": 10}
        agent = "a"
        permo = ("a")
        res = self.shap.get_cost_from_permo(agent, permo, abc)
        self.assertEqual(res , 10)

        abc = {"": 0,"a": 10, "b":10,"ab": 15}
        agent = "a"
        permo = ("b","a")
        res = self.shap.get_cost_from_permo(agent, permo, abc)
        self.assertEqual(res , 5)

        abc = {"": 0,"a": 0,"b": 0,"c": 100,"ab": 300,"ac": 200,"bc": 100,"abc": 500}
        agent = "a"
        permo = ("a","b","c")
        res = self.shap.get_cost_from_permo(agent, permo, abc)
        self.assertEqual(res , 0)
        agent = "c"
        permo = ("a","b","c")
        res = self.shap.get_cost_from_permo(agent, permo, abc)
        self.assertEqual(res , 200)

        abc = {'': 0, 'a1': 100, 'B2': 150, 'c1': 250, 'a1B2': 200, 'a1c1': 250, 'B2c1': 300, 'a1B2c1': 370}
        agent = "B2"
        permo = ("a1","B2","c1")
        res = self.shap.get_cost_from_permo(agent, permo, abc)
        self.assertEqual(res , 100)

    def test_values_just_avg(self):
        abc = {'': 0, 'a': 10}
        agents = ["a"]
        res = self.shap.values(abc, agents)
        res_true = {'a': 10.0}
        self.assertEqual(res , res_true)

        abc = {"": 0,"a1": 10,"a2": 10, "a1a2": 15}
        agents = ["a1","a2"]
        res = self.shap.values(abc, agents)
        res_true = {'a1': 7.5, 'a2': 7.5}
        self.assertEqual(res , res_true)

        abc = {"": 0,"a": 10,"b": 10, "c": 15, "ab": 20, "ac": 15, "bc": 20, "abc": 20}
        agents = ["a", "b", "c"]
        res = self.shap.values(abc, agents)
        res_true = {'a': 5, 'b': 7.5, 'c':7.5}
        self.assertEqual(res , res_true)

        abc = {'': 0, 'a1': 100, 'B2': 150, 'c1': 250, 'a1B2': 200, 'a1c1': 250, 'B2c1': 300, 'a1B2c1': 370}
        agents = ["a1", "B2", "c1"]
        res = self.shap.values(abc, agents)
        res_true = {'a1': 65.0, 'B2': 115.0, 'c1': 190.0}
        self.assertEqual(res , res_true)

        abc = {"": 0,"a": 0,"b": 0,"c": 100,"ab": 300,"ac": 200,"bc": 100,"abc": 500}
        agents = ["a","b","c"]
        res = self.shap.values(abc, agents)
        res_true = {'a': 200.0, 'b': 150.0, 'c': 150.0}
        self.assertEqual(res , res_true)

        abc = {"": 0, "a": 100, "b": 100, "c": 100, "d": 100,
         "ab": 200, "ac": 200, "ad": 200, "bc": 200, "bd": 200, "cd": 200,
          "abc": 300, "abd": 300, "acd": 300, "bcd": 300, "abcd": 400, }
        agents = ["a","b","c","d"]
        res = self.shap.values(abc, agents)
        res_true = {'a': 100.0, 'b': 100.0, 'c': 100.0,'d':100.0}
        self.assertEqual(res , res_true)

        abc = {"": 0, "a": 50, "b": 50, "c": 100, "d": 100,
         "ab": 100, "ac": 100, "ad": 150, "bc": 150, "bd": 100, "cd": 200,
          "abc": 150, "abd": 150, "acd": 200, "bcd": 200, "abcd": 250}
        agents = ["a","b","c","d"]
        res = self.shap.values(abc, agents)
        res_true = {'a': 37.5, 'b': 37.5, 'c': 87.5,'d':87.5}
        self.assertEqual(res , res_true)


    def test_values_all_permo(self):
        self.maxDiff = 40000 # to show a high print error
        abc = {'': 0, 'a': 10}
        agents = ["a"]
        res = self.shap.values(abc, agents,just_avg=False)
        res_true = {'a': {'AVG': 10.0, ('a',): 10}}
        self.assertEqual(res , res_true)

        abc = {"": 0,"a1": 100,"a2": 100, "a1a2": 150}
        agents = ["a1","a2"]
        res = self.shap.values(abc, agents,just_avg=False)
        res_true = {'a1': {'AVG': 75, ('a1', 'a2'): 100, ('a2', 'a1'): 50}, 'a2': {'AVG': 75, ('a1', 'a2'): 50, ('a2', 'a1'): 100}}
        self.assertEqual(res , res_true)

        abc = {"": 0,"a": 100,"b": 100, "c": 150, "ab": 200, "ac": 150, "bc": 200, "abc": 200}
        agents = ["a", "b", "c"]
        res = self.shap.values(abc, agents, just_avg=False)
        res_true = {'a': {'AVG': 50.0, ('a', 'b', 'c'): 100, ('a', 'c', 'b'): 100, ('b', 'a', 'c'): 100, ('b', 'c', 'a'): 0, ('c', 'a', 'b'): 0, ('c', 'b', 'a'): 0},
                    'b': {'AVG': 75.0, ('a', 'b', 'c'): 100, ('a', 'c', 'b'): 50, ('b', 'a', 'c'): 100, ('b', 'c', 'a'): 100, ('c', 'a', 'b'): 50, ('c', 'b', 'a'): 50},
                    'c': {'AVG': 75.0, ('a', 'b', 'c'): 0, ('a', 'c', 'b'): 50, ('b', 'a', 'c'): 0, ('b', 'c', 'a'): 100, ('c', 'a', 'b'): 150, ('c', 'b', 'a'): 150}}
        self.assertEqual(res , res_true)


        abc = {"": 0,"a": 0,"b": 0, "c": 100, "ab": 300, "ac": 200, "bc": 100, "abc": 500}
        agents = ["a", "b", "c"]
        res = self.shap.values(abc, agents, just_avg=False)
        res_true = {'a': {'AVG': 200.0, ('a', 'b', 'c'): 0, ('a', 'c', 'b'): 0, ('b', 'a', 'c'): 300, ('b', 'c', 'a'): 400, ('c', 'a', 'b'): 100, ('c', 'b', 'a'): 400},
                    'b': {'AVG': 150.0, ('a', 'b', 'c'): 300, ('a', 'c', 'b'): 300, ('b', 'a', 'c'): 0, ('b', 'c', 'a'): 0, ('c', 'a', 'b'): 300, ('c', 'b', 'a'): 0},
                    'c': {'AVG': 150.0, ('a', 'b', 'c'): 200, ('a', 'c', 'b'): 200, ('b', 'a', 'c'): 200, ('b', 'c', 'a'): 100, ('c', 'a', 'b'): 100, ('c', 'b', 'a'): 100}}
        self.assertEqual(res , res_true)


if __name__ == '__main__':
    unittest.main()
    
