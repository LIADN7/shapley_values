#!python3

"""
Explainable Shapley-Based Allocation
Based on:
Meir Nizri, Noam Hazon, Amos Azaria
["Explainable Shapley-Based Allocation (Student Abstract)"](https://www.aaai.org/AAAI22Papers/SA-00194-NizriM.pdf)
Programmer: Liad Nagi
See also:
Since:
"""



from itertools import combinations
import math
import string
import logging
import shapley_values
from shapley_values.shapley import shapley

logger = logging.getLogger(__name__)


class x_shapley():

    def x_shap(self, abc: dict(), agents: list[str]) -> list():
        """
        Create the division of the game into situations so that it is ETX (easy to explain).
        :param abc: Valuations of all the combination.
        :param agents: All the names of the agents.
        :return X: The division of the game.
        >>> # ex1
        >>> # ------
        >>> x_func = x_shapley()
        >>> abc = {"": 0,"a1": 0,"b1": 0,"c1": 100,"a1b1": 300,"a1c1": 200,"b1c1": 100,"a1b1c1": 500}
        >>> agents = ["a1","b1","c1"]
        >>> X = x_func.x_shap(abc, agents)
        >>> for i in X: print(i)
        {'': 0, 'a1': 0, 'b1': 0, 'c1': 100, 'a1b1': 0, 'a1c1': 100, 'b1c1': 100, 'a1b1c1': 100}
        {'': 0, 'a1': 0, 'b1': 0, 'c1': 0, 'a1b1': 300, 'a1c1': 0, 'b1c1': 0, 'a1b1c1': 300}
        {'': 0, 'a1': 0, 'b1': 0, 'c1': 0, 'a1b1': 0, 'a1c1': 100, 'b1c1': 0, 'a1b1c1': 100}
        >>> # ex2
        >>> # ------
        >>> abc = {"": 0,"a1": 10,"a2": 10, "a1a2": 15}
        >>> agents = ["a1","a2"]
        >>> X = x_func.x_shap(abc, agents)
        >>> for i in X: print(i)
        {'': 0, 'a1': 10, 'a2': 0, 'a1a2': 10}
        {'': 0, 'a1': 0, 'a2': 10, 'a1a2': 10}
        {'': 0, 'a1': 0, 'a2': 0, 'a1a2': -5}
        >>> # ex3
        >>> # ------
        >>> abc = {"": 0,"a": 10}
        >>> agents = ["a"]
        >>> X = x_func.x_shap(abc, agents)
        >>> for i in X: print(i)
        {'': 0, 'a': 10}
        >>> # ex4
        >>> # ------
        >>> abc = {"": 0,"a": 100,"b": 150,"c": 250,"ab": 200,"ac": 250,"bc": 300,"abc": 370}
        >>> agents = ["a", "b", "c"]
        >>> X = x_func.x_shap(abc, agents)
        >>> for i in X: print(i)
        {'': 0, 'a': 100, 'b': 0, 'c': 0, 'ab': 100, 'ac': 100, 'bc': 0, 'abc': 100}
        {'': 0, 'a': 0, 'b': 150, 'c': 0, 'ab': 150, 'ac': 0, 'bc': 150, 'abc': 150}
        {'': 0, 'a': 0, 'b': 0, 'c': 250, 'ab': 0, 'ac': 250, 'bc': 250, 'abc': 250}
        {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': -50, 'ac': 0, 'bc': 0, 'abc': -50}
        {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': -100, 'bc': 0, 'abc': -100}
        {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 0, 'bc': -100, 'abc': -100}
        {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 0, 'bc': 0, 'abc': 120}
        """
        shap_func = shapley()
        abc = shap_func.fix_abc(abc, agents)
        # print(abc)
        n = len(agents)
        len_abc = len(abc)
        X = []
        accum = {}
        for key, val in abc.items():
            accum[key] = 0

        # all the combinations in abc 
        arr_per = [l for i in range(len(agents)) for l in combinations(agents, i+1)]       
        for i in range(n): #for each i in len n
            for j in arr_per: # j is comb_list = list of abc in len i from a,b,c to ['a','b','c']
                if(len(j)==i+1): # check a1a2a3 == 3
                    st1="".join(j) # build a string of abc by order -> ['a1','a2']to "a1a2"
                    if(abc[st1]!=accum[st1]): # if abc['a1a2']!=accum['a1a2']
                        x = {}
                        for key, val in abc.items(): # x = [0,0,...,0]
                            x[key] = 0
                        for k in arr_per: # build scenario x
                            if(shap_func.contain_str(j , k)):
                                st2="".join(k)

                                x[st2] = abc[st1] - accum[st1]
                        X.append(x)        
                        for key, val in abc.items(): # add x to accum
                            accum[key] += x[key]
        return X


    def get_one_explanation(self, i: dict(), agents: list[str]):
        """
        >>> # ex1
        >>> # ------
        >>> x_func = x_shapley()
        >>> agents = ["a","b","c"]
        >>> X = {'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 0, 'ac': 100, 'bc': 100, 'abc': 100}
        >>> res = x_func.get_one_explanation(X, agents)
        >>> check_st = str("In this scenario, a, b do not contribute anything. The entire revenue is contributed by c alone. Therefore, the total revenue, which is $100.0, should solely go to c, and thus, the fair division is a : $0.0, b : $0.0, c : $100.0,")
        >>> print(x_func.compare_str(res,check_st))
        True
        >>> agents = ["a","b","c"]
        >>> X = {'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 200, 'ac': 100, 'bc': 100, 'abc': 100}
        >>> res = x_func.get_one_explanation(X, agents)
        >>> check_st = str("This scenario is not easy to axplaine")
        >>> print(x_func.compare_str(res,check_st))
        True
        """

        if not self.easy_to_explain(i):
            return "This scenario is not easy to axplaine"
        shap_func = shapley()
        st_temp = "In this scenario, "
        temp_shap = shap_func.values(abc = i , agents= agents)
        ziros_val = list()
        divide_val = list()

        for i1,i2 in temp_shap.items(): # get all the zeros items and divides items 
            if (i2 == 0):
                ziros_val.append(i1)
            else:
                divide_val.append(i1)
        val = temp_shap[divide_val[0]]
        total_val = val*len(divide_val); 

        if(len(ziros_val)>0): # if have zeros items
            for j in range(len(ziros_val)-1):
                st_temp+=ziros_val[j]+", "
            st_temp+=ziros_val[len(ziros_val)-1]+" do not contribute anything.\n"

        if(len(divide_val)==1): # add by how many divides
            st_temp+="The entire revenue is contributed by "+str(divide_val[len(divide_val)-1])+" alone.\n"
        else:
            for j in range(len(divide_val)-1):
                st_temp+=divide_val[j]+", "
            st_temp+=divide_val[len(divide_val)-1]+" are identical and always contribute the same.\n"
        st_temp+="Therefore, the total revenue, which is $"+str(total_val)+", "

        if(len(divide_val)==1):
            st_temp+="should solely go to "+divide_val[len(divide_val)-1]+",\n"
        else:
            st_temp+= "should be equally divided between "
            for j in range(len(divide_val)-1):
                st_temp+=divide_val[j]+", "
            st_temp+=divide_val[len(divide_val)-1]+",\n"
        st_temp+="and thus, the fair division is\n"
        for i1,i2 in temp_shap.items():
            st_temp+=i1+" : $"+str(i2)+", "
        st_temp+="\n"
        return st_temp

    def get_explanation(self, X: list(), agents: list[str]):
        """
        Creates an explanation based on the division of the game we received from the "x_shap" algorithm
        :param X: The division of the game.
        :param agents: All the names of the agents.
        :return res: An easy explanation.
        >>> # ex1
        >>> # ------
        >>> x_func = x_shapley()
        >>> agents = ["a","b","c"]
        >>> X = [{'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 0, 'ac': 100, 'bc': 100, 'abc': 100},{'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 300, 'ac': 0, 'bc': 0, 'abc': 300},{'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 100, 'bc': 0, 'abc': 100}]
        >>> res = x_func.get_explanation(X, agents)
        >>> check_st = str("Numbers of scenarios is 3 - (1) This scenario is: {'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 0, 'ac': 100, 'bc': 100, 'abc': 100} In this scenario, a, b do not contribute anything. The entire revenue is contributed by c alone. Therefore, the total revenue, which is $100.0, should solely go to c, and thus, the fair division is a : $0.0, b : $0.0, c : $100.0, (2) This scenario is: {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 300, 'ac': 0, 'bc': 0, 'abc': 300} In this scenario, c do not contribute anything. a, b are identical and always contribute the same. Therefore, the total revenue, which is $300.0, should be equally divided between a, b, and thus, the fair division is a : $150.0, b : $150.0, c : $0.0, (3) This scenario is: {'': 0, 'a': 0, 'b': 0, 'c': 0, 'ab': 0, 'ac': 100, 'bc': 0, 'abc': 100} In this scenario, b do not contribute anything. a, c are identical and always contribute the same. Therefore, the total revenue, which is $100.0, should be equally divided between a, c, and thus, the fair division is a : $50.0, b : $0.0, c : $50.0,")
        >>> print(x_func.compare_str(res,check_st))
        True
        >>> # ex2
        >>> # ------
        >>> agents = ["a","b"]
        >>> X = [{'': 0, 'a': 10, 'b': 0, 'ab': 10},{'': 0, 'a': 0, 'b': 10, 'ab': 10},{'': 0, 'a': 0, 'b': 0, 'ab': -5}]
        >>> res = x_func.get_explanation(X, agents)
        >>> check_st = str("Numbers of scenarios is 3 - (1) This scenario is: {'': 0, 'a': 10, 'b': 0, 'ab': 10} In this scenario, b do not contribute anything. The entire revenue is contributed by a alone. Therefore, the total revenue, which is $10.0, should solely go to a, and thus, the fair division is a : $10.0, b : $0.0, (2) This scenario is: {'': 0, 'a': 0, 'b': 10, 'ab': 10} In this scenario, a do not contribute anything. The entire revenue is contributed by b alone. Therefore, the total revenue, which is $10.0, should solely go to b, and thus, the fair division is a : $0.0, b : $10.0, (3) This scenario is: {'': 0, 'a': 0, 'b': 0, 'ab': -5} In this scenario, a, b are identical and always contribute the same. Therefore, the total revenue, which is $-5.0, should be equally divided between a, b, and thus, the fair division is a : $-2.5, b : $-2.5,")
        >>> print(x_func.compare_str(res,check_st))
        True
        """

        res = str()
        senario_num=1
        res+="\nNumbers of scenarios is "+str(len(X))+" - \n\n"
        for i in X:
            res+= "("+str(senario_num)+") This scenario is:\n"+str(i)+"\n"
            res+=self.get_one_explanation(i ,agents)+"\n"
            senario_num+=1

            
        return res


    def get_explanation_with_threads(self, X: list(), agents: list[str]):
        """
        Creates an explanation based on the division of the game with threads
        :param X: The division of the game.
        :param agents: All the names of the agents.
        :return res: An easy explanation.
        """
        import concurrent.futures

        res = str()
        senario_num=1
        res+="\nNumbers of scenarios is "+str(len(X))+" - \n\n"
        f = []
        #build all the explantion with pool threads
        with concurrent.futures.ThreadPoolExecutor() as exect:
            f = [exect.submit(self.get_one_explanation , i, agents) for i in X]
            for k in concurrent.futures.as_completed(f):
                res+= "("+str(senario_num)+") This scenario is:\n"+str(X[senario_num-1])+"\n"
                res+=k.result()+"\n"
                senario_num+=1       
        return res



    def easy_to_explain(self, X):
        """
        Check if easy to explane
        :param X: The division of the game.
        :return: True if easy explanation.
        >>> # ex1
        >>> # ------
        >>> x_func = x_shapley()
        >>> X = [{'': 0, 'a': 10, 'b': 10, 'ab': 0}]
        >>> print(x_func.easy_to_explain(X))
        True
        >>> X = [{'': 0, 'a': 10, 'b': 10, 'c': 10, 'ab': 0, 'ac': 10, 'bc': 10, 'abc': 10}]
        >>> print(x_func.easy_to_explain(X))
        True
        >>> X = [{'': 0, 'a': 10, 'b': 10, 'c': 10, 'ab': 0, 'ac': 0, 'bc': 0, 'abc': 10}, {'': 0, 'a': 10, 'b': 10, 'ab': 0}]
        >>> print(x_func.easy_to_explain(X))
        True
        >>> X = [{'': 0, 'a': 11, 'b': 10, 'ab': 20}]
        >>> print(x_func.easy_to_explain(X))
        False
        >>> X = [{'': 0, 'a': 11, 'b': 10, 'ab': 20}, {'': 0, 'a': 10, 'b': 10, 'ab': 0}]
        >>> print(x_func.easy_to_explain(X))
        False
        >>> X = [{'': 0, 'a': 10, 'b': 10, 'ab': 20}, {'': 0, 'a': 11, 'b': 10, 'ab': 0}]
        >>> print(x_func.easy_to_explain(X))
        False
        """
        if(not isinstance(X, list)):
            X = [X]
        for i in X: # for every game i in X
            val=0
            flag =True
            for j,k in i.items(): # check if all val equals or 0
                if k!=0:
                    if flag:
                        val = k
                        flag=False
                    if val!=k:
                        return False
        return True
                    
    def compare_str(self, st1:str , st2: str)->bool:
        """
        Check if st1 equals to st2 without ('.\n ,\t') 
        :param st1: String to compare.
        :param st2: String to compare.
        :return: True if equals.
        >>> # ex1
        >>> # ------
        >>> x_func = x_shapley()
        >>> a = "aa aa"
        >>> b = "aaaa"
        >>> print(x_func.compare_str(a,b))
        True
        >>> a = "a  a a,,,a..."
        >>> b = "a,aa,a,"
        >>> print(x_func.compare_str(a,b))
        True
        >>> a = "a  a a,,,a..."
        >>> b = "aa bb"
        >>> print(x_func.compare_str(a,b))
        False
        >>> a = "(1) a. (2) a, a a."
        >>> b = "(1)a. (2)a, aa."
        >>> print(x_func.compare_str(a,b))
        True
        """
        remove_from_st = ".\n ,\t"
        for char in remove_from_st:
            st1 = st1.replace(char, "")
            st2 = st2.replace(char, "")
        return (st1 == st2)





if __name__ == "__main__":
    import doctest
    import sys
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    # doctest.run_docstring_examples(x_shapley.fix_abc, globals())

    # import time 
    # x_func = x_shapley()
    # agents = ["a","b","c"]
    # X = [{'': 0, 'a': 0, 'b': 0, 'c': 100, 'ab': 0, 'ac': 100, 'bc': 100, 'abc': 100}]
    # for i in range(30000):
    #     X.append(X[0])
    # # print(X)
    # print("explation of len(X) = 30001")
    # print("get_explanation_with_threads end in:")
    # start = time.perf_counter()
    # x_func.get_explanation_with_threads(X, agents)
    # end = time.perf_counter()
    # print(f'{round(end-start,2)} second(s)')
    # x_func.get_explanation(X, agents)
    # start = time.perf_counter()
    # print("get_explanation end in:")
    # print(f'{round(start-end,2)} second(s)')
