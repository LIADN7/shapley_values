import unittest
from x_shapley import x_shapley



class test_shapley(unittest.TestCase):
    
    def setUp(self):
        self.x_shap = x_shapley()

    def tearDown(self):
        pass

    def test_compare_str(self):
        a = "aa aa"
        b = "aaaa"
        self.assertEqual(self.x_shap.compare_str(a,b),True)
        
        a = "a  a a,,,a..."
        b = "a,aa,a,"
        self.assertEqual(self.x_shap.compare_str(a,b),True)

        a = "a  a a,,,a..."
        b = "aa bb"
        self.assertEqual(self.x_shap.compare_str(a,b),False)

        a = "(1) a. (2) a, a a."
        b = "(1)a. (2)a, aa."
        self.assertEqual(self.x_shap.compare_str(a,b),True)


    def test_easy_to_explain(self):
        X = {'': 0, 'a': 100}
        self.assertEqual(self.x_shap.easy_to_explain(X),True)

        X = {'': 0, 'a': 10, 'b': 10, 'ab': 0}
        self.assertEqual(self.x_shap.easy_to_explain(X),True)

        X = {'': 0, 'a': -10, 'b': 10, 'ab': 0}
        self.assertEqual(self.x_shap.easy_to_explain(X),False)

        X = {'': 0, 'a': -10, 'b': -10, 'ab': 0}
        self.assertEqual(self.x_shap.easy_to_explain(X),True)

        X = {'': 0, 'a': -10, 'b': -11, 'ab': 0}
        self.assertEqual(self.x_shap.easy_to_explain(X),False)

        X = {'': 0, 'a': 10, 'b': 10, 'c': 10, 'ab': 0, 'ac': 10, 'bc': 10, 'abc': 10}
        self.assertEqual(self.x_shap.easy_to_explain(X),True)

        X = [{'': 0, 'a': 10, 'b': 10, 'c': 10, 'ab': 0, 'ac': 0, 'bc': 0, 'abc': 10}, {'': 0, 'a': 10, 'b': 10, 'ab': 0}]
        self.assertEqual(self.x_shap.easy_to_explain(X),True)

        X = {'': 0, 'a': 11, 'b': 10, 'ab': 20}
        self.assertEqual(self.x_shap.easy_to_explain(X),False)

        X = [{'': 0, 'a': 11, 'b': 10, 'ab': 20}, {'': 0, 'a': 10, 'b': 10, 'ab': 0}]
        self.assertEqual(self.x_shap.easy_to_explain(X),False)

        X = [{'': 0, 'a': 10, 'b': 10, 'ab': 20}, {'': 0, 'a': 11, 'b': 10, 'ab': 0}]
        self.assertEqual(self.x_shap.easy_to_explain(X),False)


    def test_get_one_explanation(self):
        agents = ["a","b","c"]
        X = {'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 0, 'ac': 100, 'bc': 100, 'abc': 100}
        res = self.x_shap.get_one_explanation(X, agents)
        check_st = str("In this scenario, a, b do not contribute anything. The entire revenue is contributed by c alone. Therefore, the total revenue, which is $100.0, should solely go to c, and thus, the fair division is a : $0.0, b : $0.0, c : $100.0,")
        self.assertEqual(self.x_shap.compare_str(res,check_st),True)
        
        agents = ["a","b","c"]
        X = {'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 200, 'ac': 100, 'bc': 100, 'abc': 100}
        res = self.x_shap.get_one_explanation(X, agents)
        check_st = str("This scenario is not easy to axplaine")
        self.assertEqual(self.x_shap.compare_str(res,check_st),True)

    def test_get_explanation(self):
        agents = ["a","b","c"]
        X = [{'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 0, 'ac': 100, 'bc': 100, 'abc': 100},{'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 300, 'ac': 0, 'bc': 0, 'abc': 300},{'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 100, 'bc': 0, 'abc': 100}]
        res = self.x_shap.get_explanation(X, agents)
        check_st = str("Numbers of scenarios is 3 - (1) This scenario is: {'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 0, 'ac': 100, 'bc': 100, 'abc': 100} In this scenario, a, b do not contribute anything. The entire revenue is contributed by c alone. Therefore, the total revenue, which is $100.0, should solely go to c, and thus, the fair division is a : $0.0, b : $0.0, c : $100.0, (2) This scenario is: {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 300, 'ac': 0, 'bc': 0, 'abc': 300} In this scenario, c do not contribute anything. a, b are identical and always contribute the same. Therefore, the total revenue, which is $300.0, should be equally divided between a, b, and thus, the fair division is a : $150.0, b : $150.0, c : $0.0, (3) This scenario is: {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 100, 'bc': 0, 'abc': 100} In this scenario, b do not contribute anything. a, c are identical and always contribute the same. Therefore, the total revenue, which is $100.0, should be equally divided between a, c, and thus, the fair division is a : $50.0, b : $0.0, c : $50.0,")
        self.assertEqual(self.x_shap.compare_str(res,check_st), True)
        
        agents = ["a","b"]
        X = [{'': 0, 'a': 10, 'b': 0, 'ab': 10},{'': 0, 'a': 0, 'b': 10, 'ab': 10},{'': 0, 'a': 0, 'b': 0, 'ab': -5}]
        res = self.x_shap.get_explanation(X, agents)
        check_st = str("Numbers of scenarios is 3 - (1) This scenario is: {'': 0, 'a': 10, 'b': 0, 'ab': 10} In this scenario, b do not contribute anything. The entire revenue is contributed by a alone. Therefore, the total revenue, which is $10.0, should solely go to a, and thus, the fair division is a : $10.0, b : $0.0, (2) This scenario is: {'': 0, 'a': 0, 'b': 10, 'ab': 10} In this scenario, a do not contribute anything. The entire revenue is contributed by b alone. Therefore, the total revenue, which is $10.0, should solely go to b, and thus, the fair division is a : $0.0, b : $10.0, (3) This scenario is: {'': 0, 'a': 0, 'b': 0, 'ab': -5} In this scenario, a, b are identical and always contribute the same. Therefore, the total revenue, which is $-5.0, should be equally divided between a, b, and thus, the fair division is a : $-2.5, b : $-2.5,")
        self.assertEqual(self.x_shap.compare_str(res,check_st), True)
        
    def test_x_shap(self):
        x_func = x_shapley()
        abc = {"": 0,"a1": 0,"b1": 0,"c1": 100,"a1b1": 300,"a1c1": 200,"b1c1": 100,"a1b1c1": 500}
        agents = ["a1","b1","c1"]
        X = x_func.x_shap(abc, agents)
        res_true = [{'': 0, 'a1': 0, 'b1': 0, 'c1': 100, 'a1b1': 0, 'a1c1': 100, 'b1c1': 100, 'a1b1c1': 100},
                   {'': 0, 'a1': 0, 'b1': 0, 'c1': 0, 'a1b1': 300, 'a1c1': 0, 'b1c1': 0, 'a1b1c1': 300},
                   {'': 0, 'a1': 0, 'b1': 0, 'c1': 0, 'a1b1': 0, 'a1c1': 100, 'b1c1': 0, 'a1b1c1': 100}]
        for i,j in zip(X,res_true):
            self.assertEqual(i, j)

        abc = {"": 0,"a1": 10,"a2": 10, "a1a2": 15}
        agents = ["a1","a2"]
        X = x_func.x_shap(abc, agents)
        res_true = [{'': 0, 'a1': 10, 'a2': 0, 'a1a2': 10},
                    {'': 0, 'a1': 0, 'a2': 10, 'a1a2': 10},
                    {'': 0, 'a1': 0, 'a2': 0, 'a1a2': -5}]
        for i,j in zip(X,res_true):
            self.assertEqual(i, j)
        
        abc = {"": 0,"a": 10}
        agents = ["a"]
        X = x_func.x_shap(abc, agents)
        res_true = [{'': 0, 'a': 10}]
        for i,j in zip(X,res_true):
            self.assertEqual(i, j)

        abc = {"": 0,"a": 100,"b": 150,"c": 250,"ab": 200,"ac": 250,"bc": 300,"abc": 370}
        agents = ["a", "b", "c"]
        X = x_func.x_shap(abc, agents)
        res_true = [{'': 0, 'a': 100, 'b': 0, 'c': 0, 'ab': 100, 'ac': 100, 'bc': 0, 'abc': 100},
                    {'': 0, 'a': 0, 'b': 150, 'c': 0, 'ab': 150, 'ac': 0, 'bc': 150, 'abc': 150},
                    {'': 0, 'a': 0, 'b': 0, 'c': 250, 'ab': 0, 'ac': 250, 'bc': 250, 'abc': 250},
                    {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': -50, 'ac': 0, 'bc': 0, 'abc': -50},
                    {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': -100, 'bc': 0, 'abc': -100},
                    {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 0, 'bc': -100, 'abc': -100},
                    {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 0, 'bc': 0, 'abc': 120}]
        for i,j in zip(X,res_true):
            self.assertEqual(i, j)
        






if __name__ == '__main__':
    unittest.main()
    
